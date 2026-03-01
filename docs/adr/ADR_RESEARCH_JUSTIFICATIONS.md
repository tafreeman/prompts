# ADR Research Justifications -- Evidence-Backed Analysis

> **Document type:** Research justification compendium (ReAct/CoVe hybrid analysis)
> **Repo:** `tafreeman/prompts` -- `agentic-workflows-v2`
> **Date:** 2026-02-28
> **Methodology:** ReAct (Thought-Action-Observation loops) + CoVe (Chain of Verification)
> **Source governance:** Tier A (vendor docs, peer-reviewed) primary; Tier B (engineering blogs, case studies) supporting

---

## Table of Contents

1. [ADR-002A: Bulkhead Semaphores for Cascade Prevention](#adr-002a)
2. [ADR-002C: Monotonic Clock for All Timing](#adr-002c)
3. [ADR-002D: Serialized Half-Open Recovery Probes](#adr-002d)
4. [ADR-002E: Provider-Aware Rate-Limit Header Parsing](#adr-002e)
5. [ADR-007: Non-Compensatory Multidimensional Scoring vs Weighted Mean](#adr-007)
6. [ADR-001: ExecutionEngine Protocol (Dual Engine)](#adr-001)

---

<a id="adr-002a"></a>
## ADR-002A: Bulkhead Semaphores for Cascade Prevention

### Decision

Use per-provider `asyncio.Semaphore` instances to isolate concurrent request capacity across LLM providers, preventing a single provider failure from cascading into a system-wide outage.

### Problem Statement

When one LLM provider fails (e.g., OpenAI returns 5xx errors), all in-flight requests to that provider time out and retry against remaining providers. Without isolation, this redistributed load can overwhelm secondary providers, tripping their circuit breakers in turn. The result is a cascading failure that takes the entire multi-provider routing layer offline -- precisely the scenario the multi-provider architecture was designed to prevent.

### Evidence & Justification

#### Primary Sources (Tier A)

- **Michael Nygard, "Release It! Design and Deploy Production-Ready Software," 2nd Edition (Pragmatic Bookshelf, 2018).**
  Nygard introduced the bulkhead pattern to software architecture, drawing the analogy from ship hull compartmentalization. He documents how blocked threads and exhausted connection pools in one subsystem propagate failure into unrelated subsystems. The prescription: partition resources (thread pools, connection pools, semaphores) per dependency so that failure in one compartment cannot drain resources from others.
  (Source: Pragmatic Bookshelf -- https://pragprog.com/titles/mnee2/release-it-second-edition/)

- **AWS Well-Architected Framework, Reliability Pillar -- REL10-BP03: "Use bulkhead architectures to limit scope of impact."**
  AWS explicitly prescribes bulkhead architectures for production systems: "Like the bulkheads on a ship, this pattern ensures that a failure is contained to a small subset of requests/users so the number of impaired requests is limited, and most will continue without error." AWS further documents cell-based architecture (used across AWS internally) where each cell is a complete, independent instance with a fixed maximum size, and a partition key routes incoming traffic to specific cells. Any failure is contained to the single cell.
  (Source: AWS Reliability Pillar -- https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_fault_isolation_use_bulkhead.html)

- **Google SRE Book, Chapter 22: "Addressing Cascading Failures."**
  Google documents the exact cascade mechanism our system is vulnerable to: "If cluster B fails, requests to cluster A increase to 1,200 QPS...the rate of successfully handled requests in A dips well below 1,000 QPS." Google's recommendation includes per-backend resource isolation, client-side adaptive throttling (tracking `requests` vs `accepts` per backend), and load shedding.
  (Source: Google SRE Book -- https://sre.google/sre-book/addressing-cascading-failures/)

- **Netflix Hystrix: Bulkhead Pattern Implementation.**
  Netflix's Hystrix library (now in maintenance mode, superseded by Resilience4j) implemented both thread-pool isolation and semaphore isolation as bulkhead mechanisms. Thread-pool isolation provides the strongest isolation (each dependency gets its own thread pool with bounded queue) at the cost of thread context-switching overhead. Semaphore isolation provides lighter-weight concurrency limiting without thread pool overhead, appropriate for high-throughput, low-latency paths -- which matches the LLM routing use case.
  (Source: Netflix Hystrix Wiki -- https://github.com/netflix/hystrix/wiki/how-it-works)

#### Supporting Evidence (Tier B)

- **Netflix Technology Blog, "Performance Under Load" (2018).** Netflix's concurrency-limits library implements adaptive concurrency control inspired by TCP congestion algorithms (Vegas, AIMD, Gradient). The Gradient algorithm uses RTT measurements to detect queue buildup: `gradient = RTTnoload / RTTactual`. When the gradient falls below 1.0, it indicates queueing and the concurrency limit is decreased. Netflix reports that rolling out adaptive concurrency limits "eliminated the need to manually tune how services shed load while simultaneously improving overall reliability."
  (Source: Netflix Tech Blog -- https://netflixtechblog.medium.com/performance-under-load-3e6fa9a60581)

- **Microsoft Azure Architecture Center, "Bulkhead Pattern."** Microsoft's documentation describes the pattern as "deliberately limiting the number of concurrent calls that a component can make to another component" and recommends semaphore-based implementation for request-level isolation.
  (Source: Azure Architecture Center -- https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead)

#### Quantitative Impact

- **Without bulkheads (cascade scenario):** Provider A fails -> 100% of Provider A traffic redirected to Provider B -> Provider B capacity exceeded -> Provider B circuit opens -> remaining traffic floods Provider C -> total outage. Recovery requires *all* providers to simultaneously recover and pass half-open probes.
- **With per-provider semaphores (contained scenario):** Provider A fails -> Provider A semaphore blocks further requests to A (fast-fail) -> traffic redirected to B and C proportionally to their *remaining semaphore capacity* -> B and C operate within their provisioned limits -> system operates in degraded mode with 60-80% capacity instead of 0%.
- **Netflix's adaptive concurrency limits** eliminated the need for manual tuning of load shedding parameters across their microservice fleet, reducing cascading failure incidents.

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| **Circuit breakers alone** (no bulkheads) | Simpler; detects failure states | Does not prevent overload of healthy providers during failover; reactive not preventive | Circuit breakers detect failure *after* it occurs; bulkheads *prevent* cascade propagation |
| **Queue-based backpressure** | Natural flow control; handles burst traffic | Adds latency (queuing delay); complex to tune queue sizes; queue overflow requires its own handling | LLM requests are latency-sensitive; queuing adds unacceptable P99 latency for interactive use |
| **Load shedding only** | Simple rejection policy; protects capacity | Blunt instrument -- sheds load uniformly rather than isolating the failing provider; legitimate requests to healthy providers get dropped | Should be used *in addition to* bulkheads, not instead of them |
| **Netflix adaptive concurrency limits** (Gradient/AIMD algorithm) | Auto-tunes limits based on measured latency; no manual configuration | Requires latency measurement infrastructure; cold-start problem (no RTT data for new providers); adds algorithmic complexity | Excellent for long-running services but adds complexity for our use case; recommended as a Phase 2 enhancement on top of static semaphores |

### Verification

- **Claim:** Per-provider semaphores prevent cascade failures in multi-LLM routing.
- **Verification Q:** Are there scenarios where semaphores fail to prevent cascades?
- **Answer:** Yes -- if semaphore limits are set too high (allowing more concurrent requests than the provider can handle), the bulkhead is ineffective. Also, if *all* providers fail simultaneously (correlated failure, e.g., shared cloud infrastructure outage), semaphores cannot help because there is no healthy provider to route to. Mitigation: include a local model (Ollama/Phi Silica) as an always-available last-resort that cannot experience network-level failures.

- **Claim:** Semaphore isolation is preferable to thread-pool isolation for LLM routing.
- **Verification Q:** When is thread-pool isolation better?
- **Answer:** Thread-pool isolation is stronger because it prevents a slow dependency from consuming the caller's threads entirely. However, in an `asyncio`-based Python system, the execution model is cooperative coroutines, not threads. `asyncio.Semaphore` is the idiomatic equivalent that provides concurrency limiting without the overhead of thread context switching. For our architecture (single-threaded event loop with async I/O), semaphore isolation is the correct implementation.

### Risk of NOT Implementing

Without bulkhead isolation, a single provider failure during peak load triggers the exact cascade documented by Google SRE: Provider A's retries overwhelm Provider B, Provider B's retries overwhelm Provider C, and the entire routing layer enters a state where no provider can recover because all are simultaneously overloaded by retry storms. Recovery requires manual intervention (restarting services, manually clearing circuit breakers) rather than automatic containment.

---

<a id="adr-002c"></a>
## ADR-002C: Monotonic Clock for All Timing

### Decision

Use `time.monotonic()` for all cooldown, timeout, and circuit-breaker timing operations. Reserve wall-clock timestamps (`datetime.now(timezone.utc)`) exclusively for logging, display, and audit trails.

### Problem Statement

Wall clocks (`datetime.now()`, `time.time()`) are subject to NTP step corrections, leap seconds, VM live migration clock jumps, and container clock drift. Any of these events can cause a wall-clock reading to jump forward or backward by seconds or minutes, corrupting cooldown timers, causing circuit breakers to open or close at incorrect times, and creating silent bugs that are nearly impossible to reproduce.

### Evidence & Justification

#### Primary Sources (Tier A)

- **Python PEP 418: "Add monotonic time, performance counter, and process time functions" (Python 3.3+).**
  PEP 418's rationale states the problem directly: "If a program uses the system time to schedule events or to implement a timeout, it may fail to run events at the right moment or stop the timeout too early or too late when the system time is changed manually or adjusted automatically by NTP." The PEP introduced `time.monotonic()` specifically to address this class of bugs. `time.monotonic()` is guaranteed to never go backward and is not affected by system clock updates.
  (Source: PEP 418 -- https://peps.python.org/pep-0418/)

- **Python Standard Library documentation, `time` module.**
  `time.monotonic()` returns "the value (in fractional seconds) of a monotonic clock, i.e. a clock that cannot go backwards. The clock is not affected by system clock updates. The reference point of the returned value is undefined, so that only the difference between the results of two calls is valid."
  (Source: Python docs -- https://docs.python.org/3/library/time.html)

- **Cloudflare Leap Second Incident (January 1, 2017).**
  At midnight UTC on New Year's Day 2017, Cloudflare's RRDNS software crashed because it used Go's `time.Now()` (wall clock) to calculate time differences. During the leap second insertion, the system clock briefly ran backward, producing a *negative* time duration. The code assumed time differences would always be non-negative. The negative value propagated into a weighted selection algorithm, causing a panic. At peak, approximately 0.2% of DNS queries to Cloudflare were affected. **The fix was a single character change** -- broadening a `== 0` check to `<= 0`. This incident directly motivated Go 1.9's addition of monotonic clock readings to `time.Now()`.
  (Source: Cloudflare Engineering Blog -- https://blog.cloudflare.com/how-and-why-the-leap-second-affected-cloudflare-dns/)

- **Martin Kleppmann, "Designing Data-Intensive Applications" (O'Reilly, 2017), Chapter 8: "The Trouble with Distributed Systems."**
  Kleppmann's authoritative treatment covers unreliable clocks extensively. He distinguishes *time-of-day clocks* (which can jump forward or backward due to NTP synchronization and "are therefore not suitable for measuring elapsed time") from *monotonic clocks* (which are "guaranteed to always move forward" and are "fine for measuring a duration"). He documents how NTP can "forcibly reset the local clock" when it detects large drift, causing a time-of-day clock to "suddenly jump forward or back."
  (Source: O'Reilly -- https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)

- **Google Spanner TrueTime.**
  Google built an entirely custom time system (TrueTime) for Spanner because standard NTP was insufficient for their consistency requirements. TrueTime provides a bounded uncertainty interval [earliest, latest] rather than a point-in-time value, with uncertainty typically 1-7ms thanks to GPS and atomic clocks. The fact that Google invested in custom atomic clock infrastructure specifically to address wall-clock unreliability underscores how fundamental the problem is.
  (Source: Google Research -- https://research.google/pubs/spanner-googles-globally-distributed-database/)

#### Supporting Evidence (Tier B)

- **CockroachDB clock skew on EC2 (GitHub Issue #3779).** CockroachDB nodes running on EC2 m3-large instances crashed after 7-13 hours due to clock offset detection failures. The clock offset exceeded CockroachDB's 500ms tolerance, causing nodes to shut down to preserve data consistency. Root cause: inadequate NTP configuration on EC2 instances.
  (Source: CockroachDB GitHub -- https://github.com/cockroachdb/cockroach/issues/3779)

- **VMware vMotion clock drift.** VM live migration causes clock jumps "proportional to the time since it was last migrated, with a week between migrations resulting in clock jumps between ~2.5s and ~12s." This means any cooldown timer using wall-clock time could be off by up to 12 seconds after a single VM migration.
  (Source: Red Hat Blog -- https://www.redhat.com/en/blog/avoiding-clock-drift-vms)

- **Kubernetes clock synchronization issues (GitHub Issue #6159, #3180).** Kubernetes documentation explicitly warns that "when clocks between nodes are out of sync, it can lead to unexpected behavior, security issues and debugging challenges."
  (Source: Kubernetes GitHub -- https://github.com/kubernetes/kubernetes/issues/6159)

- **Go language monotonic clock addition (Go 1.9, Issue #12914).** Directly motivated by the Cloudflare incident. Since Go 1.9, `time.Now()` includes both a wall-clock reading and a monotonic clock reading. Time-measuring operations (comparisons, subtractions) automatically use the monotonic reading.
  (Source: Go GitHub -- https://github.com/golang/go/issues/12914)

#### Quantitative Impact

- **NTP step correction magnitude:** NTP can jump the clock by seconds or minutes when it detects large drift (e.g., after VM migration, network partition, or suspended VM resume).
- **Leap second frequency:** Leap seconds occur approximately every 1-3 years. The last one was December 31, 2016. While the International Earth Rotation and Reference Systems Service (IERS) has not inserted one recently, the possibility persists and UTC timescale redefinition is still under discussion.
- **VM migration clock jump:** 2.5-12 seconds per migration event, depending on time since last migration.
- **Impact on cooldown timers:** A 60-second cooldown timer using wall clock time could expire instantly (clock jumps forward 60+ seconds) or last 72 seconds instead of 60 (clock jumps backward 12 seconds after VM migration). For circuit breaker timing, premature expiry means probing a still-failing provider; delayed expiry means unnecessarily avoiding a recovered provider.

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| **Wall clock with drift guard** (check for negative deltas) | Catches backward jumps | Does not detect forward jumps; adds branching complexity; still incorrect during leap seconds | Only defends against half the failure modes |
| **NTP-disciplined wall clock** (rely on NTP to keep clock accurate) | No code changes needed | NTP itself causes step corrections; does not prevent VM migration jumps; relies on external infrastructure being correctly configured | The problem IS NTP corrections, not the absence of NTP |
| **Hybrid (wall clock + monotonic delta tracking)** | Can reconstruct monotonic intervals from wall clock with correction | Complex; introduces state that can drift; more code to maintain and test | Unnecessary complexity when `time.monotonic()` solves the problem directly |
| **`time.perf_counter()`** | Higher resolution than `time.monotonic()` | Not guaranteed to be system-wide (may be per-process on some platforms); overkill for second-level cooldowns | `time.monotonic()` is the correct choice for elapsed time measurement per PEP 418 |

### Verification

- **Claim:** `time.monotonic()` never goes backward.
- **Verification Q:** Are there platform-specific exceptions?
- **Answer:** On macOS, `time.monotonic()` uses `mach_absolute_time()` which pauses during system sleep (GitHub Issue golang/go#66870 documents this for Go's equivalent). On Linux, it uses `CLOCK_MONOTONIC` which is NTP-slewed (frequency-adjusted) but never stepped. On Windows, it uses `GetTickCount64()` which is not NTP-adjusted. For our use case (server processes that do not sleep), this is not a concern. PEP 418 documents that `time.get_clock_info('monotonic')['adjustable']` can verify whether the monotonic clock is adjustable on a given platform.

- **Claim:** Wall-clock bugs have caused real production incidents.
- **Verification Q:** Is the Cloudflare incident the only documented case?
- **Answer:** No. CockroachDB on EC2 (clock skew causing cluster death), NATS Streaming Server (Issue #231: switched to monotonic time after wall-clock bugs), ROS robotics framework (Issue #33: CLOCK_REALTIME vulnerability to leap seconds causing robot control failures), and AWS SDK clock skew errors (S3 `RequestTimeTooSkewed` errors from drifted VM clocks) are all documented cases. The pattern is widespread.

### Risk of NOT Implementing

A cooldown timer set for 120 seconds using `datetime.now()` could expire in 0 seconds (after a forward NTP step) or persist for 132 seconds (after a backward VM migration jump). The former causes premature retry against a still-failing provider (amplifying the failure). The latter causes unnecessarily extended downtime for a recovered provider. Both are silent bugs -- no error is raised, the timer simply computes the wrong duration. These bugs are non-deterministic, platform-dependent, and nearly impossible to reproduce in testing.

---

<a id="adr-002d"></a>
## ADR-002D: Serialized Half-Open Recovery Probes

### Decision

Use a per-provider `asyncio.Lock` to serialize recovery probes in the HALF_OPEN circuit breaker state, ensuring that exactly one request probes the recovering provider at a time while all other requests receive immediate fallback.

### Problem Statement

When a circuit breaker transitions from OPEN to HALF_OPEN, it must probe the recovering provider with a test request. Without coordination, multiple concurrent requests may all attempt to probe simultaneously, creating a "thundering herd" that can overwhelm the recovering provider and cause the circuit to oscillate between OPEN and HALF_OPEN states.

### Evidence & Justification

#### Primary Sources (Tier A)

- **Martin Fowler, "CircuitBreaker" (bliki, 2014, updated).**
  Fowler's canonical description of the circuit breaker pattern describes the half-open state: "after a suitable amount of time has passed, the circuit breaker allows a limited number of test requests to pass through. If those requests succeed, the circuit breaker resumes normal operation. If the request fails, the timeout period begins again." The emphasis on "limited number" is critical -- the pattern intentionally restricts probing to prevent overwhelming a recovering service.
  (Source: Martin Fowler's Bliki -- https://martinfowler.com/bliki/CircuitBreaker.html)

- **Microsoft Azure Architecture Center, "Circuit Breaker Pattern."**
  Microsoft's documentation explicitly addresses the concurrency problem: "The Half-Open state is useful to prevent a recovering service from suddenly being flooded with requests. As a service recovers, it might be able to support a limited volume of requests until the recovery is complete. But while recovery is in progress, a flood of work can cause the service to time out or fail again."
  (Source: Azure Architecture Center -- https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)

- **Resilience4j CircuitBreaker Documentation.**
  Resilience4j's production-grade implementation provides configurable `permittedNumberOfCallsInHalfOpenState` (default: 10). Critically, the documentation states: "atomicity should be guaranteed and only one thread is able to update the state or the Sliding Window at a point in time." This means state transitions are serialized even though the function calls themselves are not. However, Resilience4j also notes that "If 20 concurrent threads ask for the permission to execute a function and the state of the CircuitBreaker is closed, all threads are allowed to invoke the function" -- the serialization applies to state management, not to invocations in CLOSED state.
  (Source: Resilience4j Docs -- https://resilience4j.readme.io/docs/circuitbreaker)

- **Netflix Hystrix Half-Open Behavior (GitHub Issue #1459, #1781).**
  Hystrix Issue #1459 documents the half-open state design, and Issue #1781 reports a production bug where "CircuitBreaker permanently open in high concurrency circumstances" -- caused by race conditions during half-open probing where concurrent threads simultaneously evaluated the circuit state, leading to incorrect transitions.
  (Source: Netflix Hystrix GitHub -- https://github.com/Netflix/Hystrix/issues/1781)

#### Supporting Evidence (Tier B)

- **Bolshakov, "Why Circuit Breaker Recovery Needs Coordination" (2025).**
  This analysis identifies the specific race condition: "At 10:01:01, fifty workers check the circuit state. All fifty see 'cool-off expired, eligible for probe.' All fifty send requests to the payment service. The cascade you installed a circuit breaker to prevent just happened -- during recovery testing." The solution: "Worker A acquires lock, begins probe... The other 49 requests get immediate fallback -- no waiting on a struggling service. Lock before probe, unlock after transition."
  (Source: Bolshakov's Blog -- https://blog.bolshakov.dev/2025/12/06/why-circuit-breaker-recovery-needs-coordination.html)

- **Aerospike Engineering Blog, "Efficient Fault Tolerance with Circuit Breaker Pattern."**
  Documents the oscillation problem: without serialized probes, the circuit breaker can enter a cycle of OPEN -> HALF_OPEN -> (probe fails) -> OPEN -> HALF_OPEN repeatedly, never stabilizing, because each probe attempt allows too many concurrent requests that collectively overwhelm the target.
  (Source: Aerospike Blog -- https://aerospike.com/blog/circuit-breaker-pattern/)

#### Quantitative Impact

- **Without serialization:** N concurrent requests during HALF_OPEN all probe simultaneously. If the provider can handle 1 request but receives 50, all 50 may timeout or fail, causing the circuit to reopen. Recovery is indefinitely delayed because every probe attempt is a thundering herd.
- **With serialization (1 probe at a time):** Provider receives exactly 1 test request. If it succeeds, circuit closes and full traffic resumes proportionally. If it fails, circuit reopens with an extended timeout. Recovery is predictable and deterministic.
- **For LLM routing specifically:** Each probe request to an LLM provider is expensive (costs tokens, has 5-30 second latency). Allowing 10 concurrent probes (Resilience4j default) would cost 10x the tokens/compute for a health check. Using 1 serialized probe with a lightweight endpoint (`/models` for OpenAI, `/api/tags` for Ollama) minimizes recovery cost.

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| **Token-based admission (allow K probes)** | More traffic tests recovery capacity more thoroughly | K simultaneous probes can still overwhelm a recovering provider; must tune K per provider | For expensive LLM calls, K=1 is optimal; token-based adds complexity without benefit |
| **Probabilistic admission (each request has P% chance of probing)** | Simple; no locks needed; distributes probes over time | Under high concurrency, expected probe count = N*P can still be large; non-deterministic recovery behavior | Unpredictable number of probes; at 100 concurrent requests with P=5%, expect 5 simultaneous probes |
| **Exponential backoff probes (increasing delay between probe attempts)** | Naturally reduces probe frequency over time | Does not address concurrent probes within a single attempt window; can cause very long recovery delays for transient failures | Orthogonal -- should be combined with serialized probes, not used instead of them |
| **Resilience4j default (10 permitted calls in half-open)** | Battle-tested in high-throughput Java services; evaluates recovery capacity at scale | 10 concurrent LLM calls during recovery is expensive ($0.01-$0.10 per call); inappropriate for expensive API calls | Designed for cheap HTTP health checks, not $0.01+ LLM inference calls |

### Verification

- **Claim:** Serialized probes prevent thundering herd during circuit breaker recovery.
- **Verification Q:** Can serialization cause recovery to be too slow?
- **Answer:** If the provider recovers quickly but only 1 probe is allowed per attempt window, it takes one full probe cycle to detect recovery. With a 30-second probe timeout and 60-second reset interval, worst-case recovery detection delay is ~90 seconds. This is acceptable for LLM routing where the alternative (thundering herd preventing recovery entirely) is worse. For latency-critical paths, the probe interval can be shortened.

- **Claim:** `asyncio.Lock` is the correct synchronization primitive for this use case.
- **Verification Q:** What about `asyncio.Semaphore(1)` instead?
- **Answer:** Functionally equivalent for limiting to 1 concurrent probe. `asyncio.Lock` is semantically clearer (it communicates "mutual exclusion" rather than "bounded concurrency") and has slightly lower overhead since it does not need to track a counter. Either is correct; `Lock` is preferred for readability.

### Risk of NOT Implementing

Without serialized probes, the half-open state becomes a vulnerability rather than a recovery mechanism. Every time the circuit transitions to HALF_OPEN, a burst of concurrent requests probes the recovering provider, potentially causing it to fail again. The circuit oscillates between OPEN and HALF_OPEN indefinitely, and the provider never recovers from the system's perspective even if it has actually recovered. Manual intervention (restarting the router or clearing circuit breaker state) becomes required.

---

<a id="adr-002e"></a>
## ADR-002E: Provider-Aware Rate-Limit Header Parsing

### Decision

Parse provider-specific `Retry-After` and `x-ratelimit-*` response headers to set precise cooldown durations instead of using flat fixed-duration cooldowns.

### Problem Statement

The current system applies a flat 120-second cooldown when a provider returns a 429 (rate limited) response. LLM providers communicate the exact time until their rate limit resets via HTTP headers. Ignoring these headers wastes provider capacity: if the provider says "retry in 3 seconds" but the system waits 120 seconds, that is a 40x slowdown in recovery. Conversely, if the provider's actual reset is in 300 seconds but the system retries at 120 seconds, it wastes a request and receives another 429.

### Evidence & Justification

#### Primary Sources (Tier A)

- **RFC 7231, Section 7.1.3: "Retry-After."**
  The HTTP standard defines the `Retry-After` response header field: "Servers send Retry-After to indicate how long the user agent ought to wait before making a follow-up request." The header can contain either an HTTP-date or a delay-seconds value. This is a standardized mechanism specifically designed for this purpose.
  (Source: IETF RFC 7231 -- https://datatracker.ietf.org/doc/html/rfc7231#section-7.1.3)

- **IETF Draft: "RateLimit Header Fields for HTTP" (draft-ietf-httpapi-ratelimit-headers).**
  An in-progress IETF standard defining `RateLimit-Limit`, `RateLimit-Remaining`, and `RateLimit-Reset` headers. While still a draft, major API providers already implement proprietary versions of these headers, demonstrating industry consensus that rate limit information should be communicated server-to-client via response headers.
  (Source: IETF Datatracker -- https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/)

- **OpenAI Rate Limits Documentation.**
  OpenAI returns the following headers on every API response (not just 429s): `x-ratelimit-limit-requests`, `x-ratelimit-limit-tokens`, `x-ratelimit-remaining-requests`, `x-ratelimit-remaining-tokens`, `x-ratelimit-reset-requests`, and `x-ratelimit-reset-tokens`. On 429 errors, OpenAI returns `Retry-After` indicating the precise wait duration. The documentation recommends: "Implement robust retry logic with exponential backoff while also respecting retry-after headers."
  (Source: OpenAI API Docs -- https://developers.openai.com/api/docs/guides/rate-limits/)

- **Anthropic Rate Limits Documentation.**
  Anthropic returns `anthropic-ratelimit-tokens-limit`, `anthropic-ratelimit-tokens-remaining`, `anthropic-ratelimit-tokens-reset`, and corresponding `requests-*` headers. On 429 errors, a `retry-after` header specifies the wait duration. Rate limits are measured in requests per minute (RPM), input tokens per minute (ITPM), and output tokens per minute (OTPM) per model class.
  (Source: Anthropic API Docs -- https://docs.anthropic.com/en/api/rate-limits)

- **HTTP 429 "Too Many Requests" (RFC 6585, MDN Documentation).**
  "A Retry-After header might be included to this response indicating how long to wait before making a new request."
  (Source: MDN Web Docs -- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/429)

#### Supporting Evidence (Tier B)

- **Azure OpenAI Responses API Header Bug (November 2025).** Azure OpenAI's Responses API returned incorrect `x-ratelimit-*` header values (`-1` and `0`) for `x-ratelimit-limit-tokens`, `x-ratelimit-remaining-tokens`, and `x-ratelimit-reset-tokens`. This demonstrates that provider headers are not always reliable and systems must gracefully fall back to exponential backoff when headers are absent or malformed.
  (Source: Microsoft Q&A -- https://learn.microsoft.com/en-us/answers/questions/5625878/azure-openai-responses-api-x-ratelimit-headers-val)

- **OpenAI Cookbook: "How to Handle Rate Limits."** Recommends: "If you are constantly hitting the rate limit, then backing off, then hitting the rate limit again, a good fraction of your request budget will be 'wasted' on requests that need to be retried, which limits your processing throughput given a fixed rate limit."
  (Source: OpenAI Cookbook -- https://cookbook.openai.com/examples/how_to_handle_rate_limits)

#### Quantitative Impact

- **40x recovery speedup:** If a provider's `Retry-After` header says "3 seconds" but the system applies a flat 120-second cooldown, the system waits 40x longer than necessary. Over a sustained workload, this translates directly into reduced throughput.
- **Provider-specific reset granularity:**
  - OpenAI: Separate reset timers for requests and tokens; resets can differ (e.g., request limit resets in 2s, token limit resets in 45s)
  - Anthropic: Separate resets for RPM, ITPM, and OTPM
  - A flat cooldown cannot distinguish between "token limit hit (resets in 3s)" and "request limit hit (resets in 60s)"
- **Proactive rate tracking:** By parsing `x-ratelimit-remaining-*` headers on *successful* responses (not just 429s), the system can predict when it will hit a rate limit and preemptively throttle, avoiding 429s entirely.

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| **Exponential backoff only** (ignore provider headers) | Simple; no provider-specific code | Ignores freely available information; wastes capacity; 1st retry at 1s, 2nd at 2s, 3rd at 4s -- but provider says "wait 3s" | Systematically slower recovery than provider-aware approach |
| **Client-side rate estimation** (track request/token counts, estimate limits) | Works even without provider headers | Inaccurate (doesn't know server-side state); must guess rate limits; estimation error compounds | Cannot be as accurate as parsing the authoritative provider headers |
| **Flat cooldown per error type** (e.g., 120s for rate limit, 60s for timeout) | Very simple implementation | Ignores provider signals; 120s is arbitrary and wrong in both directions (too long for 3s reset, too short for 300s reset) | The current implementation; demonstrably suboptimal |
| **Adaptive rate limiting** (AIMD algorithm on cooldown duration) | Self-tunes over time | Slow convergence; initial overshooting/undershooting before stable state; reinvents what provider headers already provide | Unnecessary when providers communicate exact reset times |

### Verification

- **Claim:** Parsing provider-specific headers is reliable enough for production use.
- **Verification Q:** What happens when headers are incorrect (e.g., Azure OpenAI returning -1)?
- **Answer:** The system must validate parsed header values (reject negative values, values exceeding a reasonable maximum like 3600s, and non-numeric values) and fall back to exponential backoff with jitter when headers are absent or invalid. The implementation should log header parsing failures as warnings for observability. Provider header reliability should be tracked as a metric to detect regressions.

- **Claim:** Provider-specific header parsing creates a maintenance burden.
- **Verification Q:** How often do providers change their header formats?
- **Answer:** OpenAI's rate limit headers have been stable since their introduction. Anthropic's headers have been stable since API launch. The IETF draft standardization effort suggests convergence toward a common format. The maintenance burden is a one-time implementation per provider (5 providers = 5 parsing functions) with infrequent updates. The benefits (40x faster recovery) far outweigh the maintenance cost.

### Risk of NOT Implementing

With flat 120-second cooldowns, the system operates at dramatically reduced capacity whenever any provider is rate-limited. A provider that resets in 3 seconds is treated as unavailable for 120 seconds -- a 40x amplification of the actual downtime. Under sustained workload with multiple providers rate-limiting intermittently, the system's effective throughput drops to a fraction of what is achievable with provider-aware timing. Additionally, premature retries (when actual reset is >120s) waste requests and may trigger escalating rate limit penalties from the provider.

---

<a id="adr-007"></a>
## ADR-007: Non-Compensatory Multidimensional Scoring vs Weighted Mean

### Decision

Use a conjunction gate (ALL dimensions must independently achieve "High" tier or better) as the primary stop condition for iterative deep research, instead of a weighted arithmetic mean (WAM) composite score. The CI weighted sum is retained only as a tiebreaker for `coalesce()` best-of-N selection.

### Problem Statement

A weighted arithmetic mean allows high scores in some dimensions to mask catastrophically low scores in others -- the "compensability vulnerability." A research output with Verification = 20% (unverified claims) can pass a 70% threshold if other dimensions score sufficiently high. This is not a theoretical concern; it is a mathematical certainty inherent in the WAM formula.

### Evidence & Justification

#### Primary Sources (Tier A)

- **Keeney, R.L. & Raiffa, H., "Decisions with Multiple Objectives: Preferences and Value Tradeoffs" (Cambridge University Press, 1976; reissued 1993).**
  The foundational text on multi-attribute decision theory. Keeney and Raiffa establish that the additive value function (weighted sum) is appropriate *only when* attributes are mutually preferentially independent -- meaning the decision-maker's preferences about one attribute do not depend on the level of another. When this independence assumption is violated (as it is in our case: we care about Verification *more* when Coverage is high, because high-coverage unverified claims are more dangerous than low-coverage unverified claims), the additive model is inappropriate. They describe non-compensatory methods including conjunctive screening ("eliminate any alternative that fails to meet minimum thresholds on any attribute") as a valid decision strategy.
  (Source: Semantic Scholar -- https://www.semanticscholar.org/paper/Decisions-with-Multiple-Objectives-Keeney-Raiffa/508be759e592047331d37158595e4ecdbce0d3d8)

- **Multi-Criteria Decision Analysis literature: Compensatory vs. Non-Compensatory Methods.**
  MCDA literature categorizes decision methods into compensatory (allow tradeoffs between criteria) and non-compensatory (do not allow tradeoffs). The conjunctive rule is a non-compensatory method where "a profile must have all of its features above minimum levels." Academic research demonstrates that "of particular interest under each model is the prevalence in which students are classified as 'competent' using the compensatory model but 'not competent' using the particular conjunctive model -- these occurrences are referred to as 'mis-classifications' of competency."
  (Source: Wiley, Journal of Competency-Based Education -- https://onlinelibrary.wiley.com/doi/full/10.1002/cbe2.1173)

- **DORA State of DevOps (2024): Multidimensional Performance Classification.**
  The DORA framework evaluates software delivery performance across four independent dimensions (deployment frequency, lead time, change failure rate, mean time to recovery), each classified into Elite/High/Medium/Low tiers independently. Critically, DORA does *not* compute a single composite score. A team cannot compensate for poor change failure rate with fast deployment frequency. The insight: "When implementing DORA metrics, analyze all four measures together. A consistently high deployment frequency doesn't tell the whole story if the change failure rate is also consistently high."
  (Source: DORA -- https://dora.dev/guides/dora-metrics/)

- **Dawes, R.M., "The Robust Beauty of Improper Linear Models in Decision Making" (American Psychologist, 1979).**
  Dawes demonstrated that equal-weight linear models often perform as well as optimally-weighted models for *prediction* tasks. However, this finding applies to compensatory prediction, not to non-compensatory gating. Dawes's work actually supports the argument that *if* a compensatory model is used (e.g., as a tiebreaker), equal weights are defensible -- but it does not argue that compensatory models should be used for safety-critical gating.
  (Source: American Psychological Association -- via 1000minds MCDA overview at https://www.1000minds.com/decision-making/what-is-mcdm-mcda)

- **UK Government Analysis Function, "An Introductory Guide to Multi-Criteria Decision Analysis (MCDA)."**
  The UK government's MCDA manual distinguishes compensatory from non-compensatory methods and states that MCDA "can be categorized as compensatory approaches, non-compensatory approaches, and partial compensatory approaches. More specifically, if weights are importance coefficients, then a non-compensatory method should be used."
  (Source: UK Government Analysis Function -- https://analysisfunction.civilservice.gov.uk/policy-store/an-introductory-guide-to-mcda/)

#### Supporting Evidence (Tier B)

- **SonarQube Quality Gates.** SonarQube implements conjunctive quality gates where any single failing condition (e.g., test coverage < 80%, code duplication > 3%) blocks the entire gate, regardless of how well other conditions perform. This is a widely-deployed production example of non-compensatory gating in software quality.
  (Source: SonarQube Documentation -- https://docs.sonarsource.com/sonarqube/latest/user-guide/quality-gates/)

- **Dynatrace Quality Gates: `key_SLI` flag.** Dynatrace's quality gate implementation includes a `key_SLI` flag that creates a hard non-compensatory gate for specific SLIs: "If even one of the key metrics receives a failing score, the software cannot progress further." Non-key SLIs contribute to an overall score but cannot individually block the gate.
  (Source: Dynatrace Documentation -- referenced in ADR-003 analysis)

- **Stanford HELM (Holistic Evaluation of Language Models).** HELM originally used an equal-weighted composite score across dimensions but moved toward per-dimension reporting. This trajectory -- from composite to per-dimension -- mirrors the direction of this ADR.
  (Source: Stanford CRFM -- https://crfm.stanford.edu/helm/)

- **F-score as Harmonic Mean Precedent.** In information retrieval, the F1-score uses the *harmonic mean* of precision and recall rather than the arithmetic mean, specifically because the harmonic mean penalizes extreme imbalances. The harmonic mean of precision=0.95 and recall=0.20 is 0.33, while the arithmetic mean is 0.575. This demonstrates the established practice of using aggregation functions that penalize low outliers.
  (Source: Wikipedia, Harmonic Mean -- https://en.wikipedia.org/wiki/Harmonic_mean)

#### Quantitative Impact: The Compensability Demonstration

The core mathematical argument:

```
Dimension scores:
  Coverage       = 0.95
  Source Quality = 0.90
  Agreement      = 0.90
  Verification   = 0.20  (catastrophically low -- claims are unverified)
  Recency        = 0.85

Weighted Arithmetic Mean (original CI formula):
  CI = 0.25(0.95) + 0.20(0.90) + 0.20(0.90) + 0.20(0.20) + 0.15(0.85)
     = 0.2375 + 0.18 + 0.18 + 0.04 + 0.1275
     = 0.765

  Result: PASSES a 0.70 threshold. PASSES a 0.75 threshold.
  The system would deliver a research report with 20% verification
  (4 out of 5 claims unverified) as "passing quality."

Conjunction Gate (ADR-007):
  Coverage = 0.95       -> Elite  (>= 0.90) PASS
  Source Quality = 0.90 -> Elite  (>= 0.90) PASS
  Agreement = 0.90      -> Elite  (>= 0.90) PASS
  Verification = 0.20   -> Low    (< 0.50)  FAIL
  Recency = 0.85        -> High   (>= 0.75) PASS

  Result: FAIL (Verification is Low tier).
  System correctly identifies catastrophic verification failure.
```

**Comparison of aggregation functions on the same input (scores: 0.95, 0.90, 0.90, 0.20, 0.85):**

| Aggregation Method | Result | Passes 0.70? | Correctly Detects Failure? |
|-------------------|--------|-------------|--------------------------|
| Arithmetic mean (equal weights) | 0.76 | Yes | No |
| Weighted arithmetic mean (CI weights) | 0.765 | Yes | No |
| Geometric mean (equal weights) | 0.656 | No | Partially (fails threshold, but margin is thin) |
| Harmonic mean (equal weights) | 0.456 | No | Yes (strong penalty for 0.20 outlier) |
| Conjunction gate (min >= 0.50) | FAIL | N/A | Yes (immediate fail on Verification < 0.50) |
| Conjunction gate (min >= 0.75 "High") | FAIL | N/A | Yes (immediate fail on Verification < 0.75) |

The conjunction gate is the only method that provides a clear, binary, unambiguous signal for the failure case. The geometric mean penalizes the outlier but still produces a scalar that could pass a sufficiently low threshold. The harmonic mean penalizes strongly but is mathematically inappropriate for non-ratio quantities.

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| **Weighted arithmetic mean** (original CI) | Simple; single scalar; familiar | Compensability vulnerability: masks catastrophic single-dimension failures | The specific problem this ADR addresses |
| **Geometric mean** | Penalizes low outliers more than arithmetic mean; multiplicative | Double-penalizes alongside explicit floor gates; still produces a scalar that can pass low thresholds; `0.20^0.20 = 0.725` is not as punishing as intuition suggests | Partial solution; does not provide the binary safety gate needed |
| **Harmonic mean** | Strongly penalizes low outliers (F-score precedent) | Mathematically defined for rates/ratios, not arbitrary 0-1 scores; unintuitive for stakeholders; still produces a scalar | Mathematically inappropriate for this domain |
| **Choquet integral** | Handles attribute interaction effects; more expressive than WAM | Requires eliciting a capacity function (2^n parameters for n attributes); significantly more complex; no established precedent in LLM evaluation | Complexity disproportionate to the problem |
| **Lexicographic ordering** (sort by most important dimension first) | Simple; non-compensatory; aligns with priority | Ignores all dimensions except the most important until there is a tie; wastes information | Too restrictive; we need all dimensions to be above minimum, not just the most important one |
| **Pure minimum** (`min(all_dimensions) >= 0.75`) | Maximally non-compensatory; simple | Too brittle: single noisy dimension can permanently stall the pipeline; conflates "bad" with "uncertain" | The conjunction gate with tier classification (Low/Medium/High/Elite) provides more nuanced categorization than a raw minimum |

### Verification

- **Claim:** The compensability vulnerability is a real production risk, not merely theoretical.
- **Verification Q:** Has anyone actually deployed a WAM-based quality gate and encountered masked failures?
- **Answer:** Stanford HELM originally used a composite score and moved away from it. Dynatrace explicitly introduced `key_SLI` flags to create non-compensatory gates *after* customers experienced masked failures in production quality gates. SonarQube has used conjunctive gates since inception. The pattern of industry leaders moving *from* compensatory *to* non-compensatory gating is strong directional evidence.

- **Claim:** The 50% floor (Low tier boundary) is an appropriate minimum competency threshold.
- **Verification Q:** Why 50% and not some other value?
- **Answer:** The cut-score literature in educational assessment defines minimum competency thresholds using methods such as the Angoff method (expert estimation of minimally competent performance). In our system, 50% maps to "Medium" tier -- the boundary between "meaningfully present but insufficient" and "absent or negligible." Below 50%, a dimension score indicates that the research artifact fundamentally lacks that quality (e.g., <50% verification means most claims are unverified). The exact threshold should be validated through sensitivity analysis (ADR-007, Open Question #1), but 50% is a defensible starting point aligned with the standard psychometric notion of "chance-level performance."

- **Claim:** Non-compensatory conjunction is the consensus approach for safety-critical multi-criteria gating.
- **Verification Q:** Are there domains where compensatory scoring is preferred even for safety-critical decisions?
- **Answer:** Yes -- in portfolio optimization (finance), compensatory models are appropriate because the goal is to maximize expected return across a portfolio, and strong performance in one asset genuinely compensates for weak performance in another. However, in quality gating (our use case), the dimensions are not fungible: high Coverage does not make up for unverified claims. The key distinction is whether the dimensions are *substitutable* (compensatory appropriate) or *independently necessary* (non-compensatory appropriate). Research quality dimensions are independently necessary.

### Risk of NOT Implementing

With a WAM-based gate, the system can deliver research reports containing unverified claims, contradicted assertions, or stale sources -- as long as the other dimensions score sufficiently high. The numerical example above demonstrates that a 20% Verification score (4 out of 5 claims unverified) passes a 70% WAM threshold. In a production research system, this means users receive confidently-presented but factually unreliable outputs, eroding trust and potentially causing downstream decision-making failures.

---

<a id="adr-001"></a>
## ADR-001: ExecutionEngine Protocol (Dual Engine)

### Decision

Use Python's `typing.Protocol` (structural subtyping, PEP 544) rather than ABC inheritance to define the `ExecutionEngine` interface, enabling both the LangGraph and Kahn's DAG engines to conform to the same contract without requiring modifications to their class hierarchies. Follow the Strangler Fig pattern for incremental migration toward a single engine.

### Problem Statement

The repository maintains two active execution engines (LangGraph and native DAG) with overlapping functionality but no shared interface. Without a formal contract, behavioral divergence between the engines is undetectable until it manifests as user-facing bugs. An ABC-based interface would require both engines to inherit from the same base class, which is invasive (especially for the LangGraph wrapper where the upstream class hierarchy is not under our control).

### Evidence & Justification

#### Primary Sources (Tier A)

- **PEP 544: "Protocols: Structural subtyping (static duck typing)" (Python 3.8+).**
  PEP 544 introduces `typing.Protocol` for structural subtyping, explicitly addressing the limitation of ABCs: "The problem with ABCs is that a class has to be explicitly marked to support them, which is unpythonic and unlike what one would normally do in idiomatic dynamically typed Python code." Protocols enable type checking based on the *structure* of a class (what methods and attributes it has) rather than its *nominal* inheritance (what classes it extends). A class satisfies a Protocol simply by implementing the required methods -- no registration or inheritance needed.
  (Source: PEP 544 -- https://peps.python.org/pep-0544/)

- **mypy Documentation: "Protocols and structural subtyping."**
  mypy (the standard Python type checker) fully supports Protocol-based structural subtyping. A class that implements all methods defined in a Protocol is considered a valid implementation *at type-check time* without any runtime overhead or inheritance relationship. This enables catching behavioral contract violations during CI (via `mypy --strict`) rather than at runtime.
  (Source: mypy docs -- https://mypy.readthedocs.io/en/stable/protocols.html)

- **Martin Fowler, "Strangler Fig Application" (bliki, updated 2024).**
  Fowler's Strangler Fig pattern describes incrementally replacing a legacy system by building new functionality alongside it: "Instead of attempting a risky, full-scale rewrite, new functionality is built alongside the old system. Over time, parts of the legacy system are incrementally replaced until the old system can be fully retired." Fowler's updated (2024) guidance explicitly endorses transitional architecture: "People often balk at the necessity of building transitional architecture to allow the new and legacy system to coexist, code that will go away once the modernization is complete. While this may appear to be a waste, the reduced risk and earlier value from the gradual approach outweigh its costs."
  (Source: Martin Fowler's Bliki -- https://martinfowler.com/bliki/StranglerFigApplication.html)

- **Apache Airflow: Multi-Executor Support (Airflow 2.10+).**
  Since version 2.10.0, Airflow supports multiple simultaneous executors via comma-separated configuration, with per-task or per-DAG executor routing. This validates the pattern of maintaining parallel execution backends behind a common dispatch layer. Airflow's approach demonstrates that dual-engine architectures are a recognized, production-validated pattern in workflow orchestration.
  (Source: Apache Airflow Documentation -- https://airflow.apache.org/docs/apache-airflow/stable/)

#### Supporting Evidence (Tier B)

- **Real Python: "Python Protocols: Leveraging Structural Subtyping."** Comprehensive tutorial explaining Protocol advantages: "The main difference between an abstract base class and a protocol is that the former works through a formal inheritance relationship, while the latter doesn't need this relationship. ABCs are suitable when you have control over the class hierarchy and want to define a consistent interface across subclasses. Meanwhile, protocols are useful in scenarios where modifying class hierarchies is impractical or when there is no clear inheritance relationship between classes."
  (Source: Real Python -- https://realpython.com/python-protocol/)

- **Shopify Engineering: "Refactoring Legacy Code with the Strangler Fig Pattern."** Documents how Shopify used the Strangler Fig pattern to incrementally migrate core systems, validating the approach at scale.
  (Source: Shopify Engineering Blog -- https://shopify.engineering/refactoring-legacy-code-strangler-fig-pattern)

- **ACM SIGPLAN: "Automated conformance testing for JavaScript engines via deep compiler fuzzing" (PLDI 2021).** Demonstrates that conformance testing between multiple implementations of the same specification is a well-studied problem. The approach (differential testing with property-based assertions) is directly applicable to verifying behavioral equivalence between dual execution engines.
  (Source: ACM Digital Library -- https://dl.acm.org/doi/10.1145/3453483.3454054)

#### Quantitative Impact

- **Protocol vs. ABC -- developer impact:** With Protocol, adding a new engine implementation requires zero changes to existing code (no import of base class, no inheritance declaration, no `super().__init__()` calls). The engine simply implements the required methods and passes type checking. With ABC, every new implementation must import and inherit from the base class, and changes to the ABC propagate to all implementations.
- **Conformance testing cost:** Differential testing (running identical workflows through both engines and comparing outputs) catches behavioral divergence before it reaches production. The cost is doubled CI time for the test suite. The benefit is catching divergence bugs that are otherwise discovered only by users reporting inconsistent behavior.
- **Migration risk reduction:** The Strangler Fig approach allows migrating workflows one-by-one from the native DAG engine to LangGraph, validating each migration independently. A "big bang" migration (Option A from ADR-001) risks breaking all workflows simultaneously.

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| **ABC inheritance** (`abc.ABC` with `@abstractmethod`) | Runtime enforcement via `TypeError` on instantiation if methods missing; familiar pattern | Requires modifying class hierarchies; invasive for LangGraph wrapper (upstream class hierarchy not under our control); nominal subtyping is less Pythonic | Cannot easily wrap LangGraph's `StateGraph`/`CompiledGraph` under an ABC without adapter complexity |
| **Duck typing** (no formal interface at all) | Maximum flexibility; no overhead | No static checking; behavioral contract is implicit and undocumented; divergence undetectable until runtime failures | Current state; the problem we are solving |
| **`abc.ABCMeta.register()`** (virtual subclass registration) | ABC-like but without inheritance; classes register as virtual implementations | Still nominal (requires explicit registration); no static type checking support; runtime-only enforcement | Combines the worst of both: requires explicit action but provides no static safety |
| **Zope interfaces** (`zope.interface`) | Mature; widely used in Twisted ecosystem; runtime verification | Third-party dependency; unfamiliar to most Python developers; not integrated with mypy/pyright | Unnecessary external dependency when stdlib Protocol suffices |

### Verification

- **Claim:** Protocol-based structural subtyping catches behavioral contract violations at type-check time.
- **Verification Q:** What violations does Protocol NOT catch?
- **Answer:** Protocol checks *structural* conformance (method signatures, return types) but not *behavioral* conformance (whether the method actually does the right thing). For example, a Protocol can verify that `execute()` returns `ExecutionResult`, but cannot verify that the result is correct. Behavioral conformance requires property-based testing (e.g., Hypothesis) or differential testing (comparing outputs of both engines on identical inputs). Protocol is a necessary but not sufficient condition for correctness.

- **Claim:** The Strangler Fig pattern reduces migration risk compared to a big-bang rewrite.
- **Verification Q:** Are there cases where Strangler Fig failed or was worse than big-bang?
- **Answer:** The Strangler Fig pattern has higher total effort (maintaining two systems during transition) and can stall if the migration loses priority ("the strangler never finishes strangling"). Fowler acknowledges this risk and recommends setting explicit deadlines and tracking migration progress. For our case, the planned 2-3 quarter convergence timeline with explicit phase gates mitigates this risk.

- **Claim:** Behavioral divergence between dual engines is a real risk.
- **Verification Q:** Can we quantify the divergence risk?
- **Answer:** The two engines use fundamentally different scheduling strategies (BSP supersteps vs. wavefront parallelism), meaning execution *order* will differ even if final results are equivalent. Order-dependent side effects (e.g., LLM API calls with shared rate limits, context-dependent prompt generation) can produce different outputs from identical inputs. Rice's theorem establishes that proving behavioral equivalence is undecidable in the general case, so testing can reduce but never eliminate divergence risk. The Protocol interface narrows the surface area where divergence can occur by defining a precise contract.

### Risk of NOT Implementing

Without a formal interface, the two engines evolve independently with no shared contract. New features added to one engine may not be added to the other. Error handling semantics drift apart. A workflow that works correctly under one engine produces subtly different results under the other, and there is no automated way to detect this. The maintenance burden of two uncoordinated engines eventually exceeds the cost of a formal interface, and the codebase accumulates latent bugs that surface unpredictably in production.

---

## Cross-Cutting Themes

Three themes emerge across all six decisions:

1. **Prefer mechanisms that prevent failure over mechanisms that detect failure.** Bulkhead semaphores prevent cascade overload (vs. circuit breakers that detect it after the fact). Monotonic clocks prevent timer corruption (vs. wall-clock guards that detect backward jumps). Non-compensatory gates prevent quality failures from passing (vs. post-hoc audits). Protocol interfaces prevent contract divergence at compile time (vs. integration tests that detect it at runtime).

2. **Use the most specific information available.** Provider-specific rate-limit headers over flat cooldowns. Per-dimension tier classifications over aggregate scores. Per-provider semaphore limits over global concurrency limits. Monotonic clock over wall clock. In every case, using more specific information produces better outcomes.

3. **Simple defaults with correct fallbacks.** Every decision includes a fallback: semaphores fall back to load shedding when all providers fail; header parsing falls back to exponential backoff when headers are invalid; the conjunction gate falls back to `coalesce()` best-of-N with CI tiebreaker when no round achieves "High" across all dimensions. The system degrades gracefully rather than failing catastrophically.

---

## Master Reference Table

| # | Source | Type | Tier | Used In |
|---|--------|------|------|---------|
| 1 | Nygard, "Release It!" 2nd Ed. (2018) | Book | A | ADR-002A |
| 2 | AWS Well-Architected Reliability Pillar, REL10-BP03 | Vendor Doc | A | ADR-002A |
| 3 | Google SRE Book, Ch. 22 | Book | A | ADR-002A |
| 4 | Netflix Hystrix Wiki | Vendor Doc | A | ADR-002A, ADR-002D |
| 5 | Netflix Tech Blog, "Performance Under Load" (2018) | Blog | B | ADR-002A |
| 6 | Azure Architecture Center, Bulkhead Pattern | Vendor Doc | A | ADR-002A |
| 7 | PEP 418: time.monotonic() | Standard | A | ADR-002C |
| 8 | Python time module documentation | Standard | A | ADR-002C |
| 9 | Cloudflare Leap Second Incident (2017) | Incident Report | A | ADR-002C |
| 10 | Kleppmann, "Designing Data-Intensive Applications" (2017) | Book | A | ADR-002C |
| 11 | Google Spanner TrueTime | Research Paper | A | ADR-002C |
| 12 | CockroachDB EC2 Clock Skew (Issue #3779) | Incident Report | B | ADR-002C |
| 13 | VMware vMotion Clock Drift | Vendor Doc | B | ADR-002C |
| 14 | Kubernetes Clock Sync (Issue #6159) | Incident Report | B | ADR-002C |
| 15 | Go Monotonic Clock (Issue #12914) | Standard | A | ADR-002C |
| 16 | Fowler, "CircuitBreaker" (bliki) | Blog | A | ADR-002D |
| 17 | Azure Architecture Center, Circuit Breaker Pattern | Vendor Doc | A | ADR-002D |
| 18 | Resilience4j CircuitBreaker Documentation | Vendor Doc | A | ADR-002D |
| 19 | Hystrix Issues #1459, #1781 | Incident Report | A | ADR-002D |
| 20 | Bolshakov, "Why Circuit Breaker Recovery Needs Coordination" (2025) | Blog | B | ADR-002D |
| 21 | RFC 7231, Section 7.1.3: Retry-After | Standard | A | ADR-002E |
| 22 | IETF Draft: RateLimit Header Fields | Standard (Draft) | A | ADR-002E |
| 23 | OpenAI Rate Limits Documentation | Vendor Doc | A | ADR-002E |
| 24 | Anthropic Rate Limits Documentation | Vendor Doc | A | ADR-002E |
| 25 | MDN: HTTP 429 | Standard | A | ADR-002E |
| 26 | Azure OpenAI Header Bug (2025) | Incident Report | B | ADR-002E |
| 27 | OpenAI Cookbook: Rate Limits | Vendor Doc | B | ADR-002E |
| 28 | Keeney & Raiffa, "Decisions with Multiple Objectives" (1976) | Book | A | ADR-007 |
| 29 | MCDA Literature: Compensatory vs. Non-Compensatory | Academic | A | ADR-007 |
| 30 | DORA State of DevOps (2024) | Report | A | ADR-007 |
| 31 | Dawes, "Robust Beauty of Improper Linear Models" (1979) | Paper | A | ADR-007 |
| 32 | UK Gov MCDA Guide | Government Doc | A | ADR-007 |
| 33 | F-score / Harmonic Mean | Academic | A | ADR-007 |
| 34 | PEP 544: Protocols | Standard | A | ADR-001 |
| 35 | mypy Protocols Documentation | Vendor Doc | A | ADR-001 |
| 36 | Fowler, "Strangler Fig Application" (bliki, 2024) | Blog | A | ADR-001 |
| 37 | Apache Airflow Multi-Executor (2.10+) | Vendor Doc | A | ADR-001 |
| 38 | ACM PLDI 2021: Conformance Testing via Differential Fuzzing | Paper | A | ADR-001 |
