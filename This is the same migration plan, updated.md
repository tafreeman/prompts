This is the same migration plan, updated to explicitly handle moving from a custom SAML middleware to Appian’s built-in SAML authentication on the Appian 25.2 server.

### Added assumptions and goals

- Current flow: users authenticate via an external/custom SAML middleware, which then passes an authenticated session or headers into Appian (Appian itself is not the SAML service provider today).[^3]
- Target flow: Appian 25.2 directly acts as the SAML service provider, configured in the Admin Console under Single Sign-On → SAML, with the IdP (e.g., Entra ID, Okta, JumpCloud, etc.) issuing SAML assertions directly to Appian.[^4][^2]
- During cutover, you need a safe fallback for local/Appian authentication (e.g., system administrator login) and a clean decommissioning path for the middleware.[^5][^3]

---

### Phase 1 – Discovery and pre-upgrade assessment (updated)

- In addition to platform inventory, document the current SAML and authentication flow: middleware URLs, IdP entity ID, SAML endpoints, claims/attributes, and how the middleware passes identity into Appian (headers, username, groups).[^6][^1]
- Confirm the IdP can support Appian as a direct SAML service provider and collect its SAML metadata (issuer, SSO URL, certificate, NameID format, attribute mappings).[^7][^1]
- Identify all user types: interactive users, service accounts, web API clients, and web-service users, since some must stay on Appian/native authentication instead of SAML.[^8][^3]

---

### Phase 2 – Target architecture and auth model (updated)

- Define the target identity and access architecture: Appian 25.2 as SAML SP, IdP as the single source of authentication, optional auto-provisioning and group sync, plus which accounts still use Appian or other auth types.[^2][^6]
- Decide hostname strategy up front, because Appian’s SAML configuration is tied to the service provider hostname and Assertion Consumer URL, and must be updated if the domain changes.[^9][^7]
- Design how users reach Appian post-migration (SP-initiated vs IdP-initiated SSO, bookmarks, internal portal links) and how any legacy middleware URLs will be retired or redirected.[^1][^3]

---

### Phase 3 – Install and configure Appian 25.2 (unchanged core)

- Install Appian 25.2 on the new host following the self-managed local installation guidance for 25.x, with required OS, Java, and app server pre-requisites.[^10][^11]
- Configure core platform components (engines, data directory, mail, logging) and confirm the environment is functional with Appian/native authentication before enabling SAML.[^11][^5]
- Ensure Java and crypto libraries are configured to support signed/encrypted SAML assertions if required by your security policy in the self-managed environment.[^12][^3]

---

### Phase 4 – SAML reimplementation on Appian (new dedicated phase)

- In the Admin Console, under Authentication → Single Sign-On, enable SAML and add a new SAML Identity Provider using the IdP metadata and the Appian site’s hostname as the service provider base URL.[^4][^2]
- Configure the Identifier (Entity ID) and Reply URL/Assertion Consumer Service endpoint in the IdP to point directly to the new Appian URL (for example, `https://<host>/suite/saml/AssertionConsumer`).[^7][^1]
- Map SAML attributes (NameID, email, first name, last name, group claims) to Appian user and group fields, enabling optional auto-provisioning and group synchronization for applications if desired.[^13][^6]

---

### Phase 5 – Coexistence strategy and admin access

- Configure the SAML users group and authentication options to allow a subset of users to log in via SAML while keeping Appian/native login available for administrators and technical accounts.[^14][^3]
- Use the “Use Identity Provider’s login page” and Identity Provider choices carefully so that normal users are redirected to the IdP while admins can still reach the native login page URL when needed.[^3][^2]
- Explicitly exclude web-service and technical users from the SAML group so process-model web services and other features that require Appian authentication keep working.[^8][^3]

---

### Phase 6 – SQL Server design and DB migration (same as before)

- Validate and provision the supported SQL Server version and configuration for Appian 25.2, including service accounts, collation, and connectivity from the new Appian host.[^15][^16]
- Move the Appian schema and application data to the new SQL Server instance using backup/restore, database copy, or replication depending on downtime tolerance.[^16][^15]
- Test database connectivity and basic Appian functionality with Appian/native auth before introducing SAML in non-prod.[^11][^16]

---

### Phase 7 – Appian application migration (unchanged, with auth checks)

- Export and import applications into a lower 25.2 environment, then validate that all login-dependent flows (e.g., “user context” rules, record filters by logged-in user) work correctly with the SAML user identities.[^17][^11]
- Confirm that any expressions that rely on usernames (for example, `loggedInUser()`) resolve the expected principal once users authenticate via SAML rather than middleware.[^2][^17]
- Validate security on groups and roles that are now potentially populated or synchronized from SAML attributes rather than the custom middleware or manual assignment.[^13][^6]

---

### Phase 8 – Third-party API and web-API considerations

- For inbound calls to Appian Web APIs, keep or configure appropriate authentication (API keys, basic auth, OAuth, or Appian header tokens) rather than SAML, which is browser-centric.[^18][^8]
- For outbound integrations from Appian to third-party APIs, the SAML change is generally transparent, but verify any flows that previously depended on middleware-injected headers or tokens.[^19][^2]
- Update documentation and runbooks so external teams understand the difference between user login (now SAML directly to Appian) and service/API authentication.[^5][^8]

---

### Phase 9 – Decommissioning the custom SAML middleware

- Once SAML is fully tested in non-prod, switch a pilot group of users in production from the middleware URL to the direct Appian URL and SAML configuration, while keeping the middleware accessible as a fallback.[^14][^1]
- Monitor SAML login behavior (success/fail rates, group mappings, user auto-provisioning) using logs and Admin Console diagnostics, tuning attribute mappings and group sync as needed.[^6][^5]
- When confidence is high, update DNS/bookmarks/portal links to point only to the Appian URL and retire or redirect the middleware endpoints, with a documented rollback plan.[^9][^1]

---

### Phase 10 – Cutover weekend runbook (SAML-aware)

1. Freeze deployments and configuration changes in the old environment, including IdP configuration and middleware settings, to keep SAML metadata consistent during the window.[^3]
2. Perform final database backup/restore or replication sync to the new SQL Server, and verify Appian 25.2 is healthy with Appian/native login.[^15][^16]
3. Enable SAML on the new Appian environment, configure the SAML IdP using the production hostname, and update the IdP to trust the new Appian service provider endpoints.[^4][^7]
4. Run SAML test logins for pilot users and confirm group membership mapping, access to key applications, and continued admin login via the Appian/native login page.[^3][^6]
5. Switch DNS or load balancer from the old environment (and middleware URL) to the new Appian host; monitor SAML and application logs closely and keep the old environment and middleware available for a defined rollback window.[^20][^9]

This version gives you a distinct SAML migration stream inside the overall EC2-to-new-host and 25.2 upgrade, while ensuring safe coexistence and rollback paths as you retire the custom middleware and rely solely on Appian’s built-in SAML support.[^2]

[^1]: <https://community.appian.com/discussions/f/general/39527/saml-configuration-for-appian-using-entra-id-azure-ad-application>
[^2]: <https://docs.appian.com/suite/help/25.3/Authentication.html>
[^3]: <https://community.appian.com/support/w/kb/370/kb-1153-saml-authentication-faq>
[^4]: <https://docs.appian.com/suite/help/25.3/SAML_for_Single_Sign-On.html>
[^5]: <https://docs.appian.com/suite/help/25.3/Appian_Administration_Console.html>
[^6]: <https://community.appian.com/discussions/f/general/39516/auto-provisioning-and-group-syncing-for-multiple-applications-in-appian>
[^7]: <https://learn.microsoft.com/en-us/entra/identity/saas-apps/appian-tutorial>
[^8]: <https://docs.appian.com/suite/help/25.3/Web_API_Authentication.html>
[^9]: <https://community.appian.com/support/w/kb/3548/kb-2343-transferring-saml-after-domain-change>
[^10]: <https://docs.appian.com/suite/help/25.2/sol-custom-overview.html>
[^11]: <https://docs.appian.com/suite/help/25.3/Appian_Documentation.html>
[^12]: <https://docs.appian.com/suite/help/25.2/rpa-9.19/java17-upgrade-guidance.html>
[^13]: <https://appian.rocks/2024/03/25/saml-group-sync/>
[^14]: <https://community.appian.com/discussions/f/administration/24505/saml-authentication-in-appian>
[^15]: <https://community.appian.com/discussions/f/general/38757/sql-server-2022-requirements>
[^16]: <https://docs.appian.com/suite/help/25.3/Configuring_Relational_Databases.html>
[^17]: <https://docs.appian.com/suite/help/25.3/backward-compatibility.html>
[^18]: <https://docs.appian.com/suite/help/25.3/connected_system_authentication.html>
[^19]: <https://community.appian.com/discussions/f/integrations/39530/sql-server-blob-to-appian-document-integration-format-incompatibility-issue>
[^20]: <https://community.appian.com/support/w/kb/3001/kb-2232-appian-platform-upgrade-path>
[^21]: <https://www.miniorange.com/iam/integrations/appian-single-sign-on-sso>
[^22]: <https://jumpcloud.com/support/integrate-with-appian>
[^23]: <https://community.appian.com/discussions/f/administration/38019/saml-dynamic-attribute-mapping>
[^24]: <https://docs.appian.com/suite/help/25.3/oauth_saml_bearer_assertion_flow.html>
[^25]: <https://community.appian.com/support/w/kb/778/kb-1461-how-to-update-saml-configurations-for-use-with-a-new-idp-signing-certificate>
[^26]: <https://docs.appian.com/suite/help/25.3/OpenID_Connect_User_Authentication.html>
