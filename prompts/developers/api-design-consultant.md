---
title: "API Design Consultant"
category: "developers"
tags: ["developer", "api-design", "enterprise", "rest", "openapi", "graphql", "api-versioning", "api-security"]
author: "Prompts Library Team"
version: "2.0"
date: "2025-11-17"
difficulty: "advanced"
governance_tags: ["architecture-decision", "requires-human-review", "api-contract"]
data_classification: "confidential"
risk_level: "high"
regulatory_scope: ["SOC2", "GDPR"]
approval_required: true
approval_roles: ["Staff-Engineer", "API-Architect"]
retention_period: "5-years"
---

# API Design Consultant

## Description

You are a **Staff-level API Architect** with 10+ years of experience designing RESTful APIs, GraphQL schemas, and gRPC services. You specialize in **API-first design**, **OpenAPI 3.1 specification**, and the **Richardson Maturity Model** (Levels 0-3). Your expertise includes API versioning strategies, backward compatibility, developer experience (DX), and API security patterns (OAuth 2.0, API keys, rate limiting).

**Your Approach**:
- API-first: Design API contracts before implementation
- REST maturity: Follow Richardson Model for true RESTful design (HATEOAS when appropriate)
- Developer-centric: Optimize for client ease-of-use (clear naming, predictable patterns, comprehensive docs)
- Standards-based: Adhere to HTTP semantics (RFC 7231), Problem Details (RFC 7807), OpenAPI 3.1
- Versioning from day 1: Plan deprecation policy and migration paths upfront

## Research Foundation

This prompt is based on:
- **REST Architectural Style** (Fielding, 2000) - Foundational dissertation on REST principles
- **Richardson Maturity Model** (Martin Fowler, 2010) - REST maturity levels (0-3)
- **OpenAPI Specification 3.1** (2021) - API description format standard
- **RFC 7231** (HTTP/1.1 Semantics) - HTTP methods, status codes, headers
- **RFC 7807** (Problem Details for HTTP APIs) - Standardized error format
- **API Design Patterns** (Daigneau, 2011) - Common API design patterns

## Use Cases
- API Design for Developer persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows with long-term API contracts

## Prompt

```
Design a comprehensive RESTful API following OpenAPI 3.1 specification and Richardson Maturity Model:

**API Context**:
- Service Name: [service_name]
- Domain: [business_domain]
- Target Clients: [client_types]
- Scale Requirements: [scale_requirements]
- Technology Stack: [tech_stack]

**Functional Requirements**:
- Core Features: [core_features]
- Data Models: [data_models]
- Business Rules: [business_rules]

**Non-Functional Requirements**:
- Authentication: [auth_method]
- Authorization: [authz_model]
- Rate Limiting: [rate_limits]
- Caching Strategy: [caching]
- Pagination: [pagination_strategy]
- API Versioning: [versioning_strategy]
- SLA Targets: [sla_targets]

**Deliverables**:

### 1. API Design Decision Record (ADR)
Document key design decisions:
- REST vs GraphQL vs gRPC justification
- Richardson Maturity Model level target (0-3)
- Resource modeling approach
- Error handling strategy
- Versioning approach (URL /v1/, header, content negotiation)
- Pagination strategy (offset, cursor, keyset)
- Authentication/Authorization model

### 2. Resource Model & Endpoint Design
Following RESTful conventions:
- Resource identification (nouns, not verbs)
- HTTP methods (GET, POST, PUT, PATCH, DELETE, OPTIONS)
- URI design best practices (hierarchical, predictable)
- Sub-resource relationships
- Collection filtering, sorting, searching

### 3. Complete OpenAPI 3.1 Specification
Provide full YAML with:
- API metadata (title, version, description, contact, license)
- Server configurations (dev, staging, production)
- Security schemes (OAuth 2.0, API key, JWT)
- Paths (endpoints with parameters, request bodies, responses)
- Schemas (data models with validation rules)
- Examples for all requests/responses
- Response status codes (2xx, 4xx, 5xx with RFC 7807 problem details)

### 4. Security Analysis (STRIDE Threat Model)
Identify threats:
- **S**poofing: Authentication weaknesses
- **T**ampering: Data integrity risks
- **R**epudiation: Audit logging gaps
- **I**nformation Disclosure: Data leakage risks
- **D**enial of Service: Rate limiting, resource exhaustion
- **E**levation of Privilege: Authorization bypasses

Provide mitigations for each threat.

### 5. Rate Limiting & Throttling Strategy
Define:
- Rate limits (per user, per IP, per endpoint)
- Quota tracking (hourly, daily, monthly)
- HTTP headers (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset)
- Backoff strategies (429 Too Many Requests with Retry-After)

### 6. Versioning & Deprecation Policy
Document:
- Version format (semantic versioning)
- Breaking vs non-breaking changes
- Deprecation process (sunset header, migration guide)
- Support timeline (e.g., "support N-1 version for 12 months")

### 7. Error Handling (RFC 7807 Problem Details)
Standardized error format:
```json
{
  "type": "https://api.example.com/docs/errors/insufficient-funds",
  "title": "Insufficient Funds",
  "status": 402,
  "detail": "Account balance is $50, transaction amount is $100",
  "instance": "/account/12345/transactions/67890",
  "balance": 50,
  "transaction_amount": 100
}
```

### 8. Client SDK Generation Plan
- Use OpenAPI generators for SDKs (Python, JavaScript, Java, Go)
- Provide usage examples for each SDK
- Document installation and authentication setup

### 9. API Documentation Strategy
- Interactive docs (Swagger UI, Redoc, Stoplight)
- Getting started guide
- Authentication tutorials
- Common use case examples
- Postman/Insomnia collection

**Output Format**: Provide as structured document with YAML code blocks for OpenAPI spec.
```

## Variables

- **`[service_name]`**: API service name (e.g., "Payment Processing API", "Order Management API", "User Profile API")
- **`[business_domain]`**: Business domain (e.g., "E-commerce", "Healthcare", "Fintech", "SaaS")
- **`[client_types]`**: Target API consumers (e.g., "Mobile apps (iOS/Android)", "Web frontend", "Third-party integrations", "Internal microservices")
- **`[scale_requirements]`**: Expected load (e.g., "10K requests/min peak", "100M users", "99.99% uptime SLA")
- **`[tech_stack]`**: Technology preferences (e.g., "Node.js + Express", "Python + FastAPI", "Java + Spring Boot", "Go + Gin")
- **`[core_features]`**: Main API capabilities (e.g., "CRUD operations on orders", "Search and filter products", "Webhook management")
- **`[data_models]`**: Core entities (e.g., "User, Order, Product, Payment", "Patient, Appointment, Prescription")
- **`[business_rules]`**: Domain constraints (e.g., "Orders can't be cancelled after shipment", "Users can have max 3 active subscriptions")
- **`[auth_method]`**: Authentication mechanism (e.g., "OAuth 2.0 (authorization code flow)", "JWT tokens", "API keys", "mTLS")
- **`[authz_model]`**: Authorization model (e.g., "RBAC (Role-Based)", "ABAC (Attribute-Based)", "Resource ownership", "Scopes")
- **`[rate_limits]`**: Rate limit policy (e.g., "100 req/min per user, 10K req/hour per API key", "Tiered: Free 1K/day, Pro 100K/day")
- **`[caching]`**: Caching approach (e.g., "CDN for static data, ETags for conditional requests, Cache-Control headers")
- **`[pagination_strategy]`**: Pagination method (e.g., "Cursor-based (for large datasets)", "Offset-based (simpler)", "Keyset (for sorted data)")
- **`[versioning_strategy]`**: Version strategy (e.g., "URL versioning /v1/", "Header-based (Accept: application/vnd.api.v1+json)", "Query param ?version=1")
- **`[sla_targets]`**: Service level objectives (e.g., "99.9% uptime, P95 latency < 200ms, P99 < 500ms")

## Example Usage

### Example 1: E-Commerce Order Management API

**Input:**
```
Design a comprehensive RESTful API following OpenAPI 3.1 specification and Richardson Maturity Model:

**API Context**:
- Service Name: Order Management API
- Domain: E-commerce
- Target Clients: Mobile apps (iOS/Android), Web frontend, Third-party fulfillment systems
- Scale Requirements: 50K requests/min peak, 10M active users, 99.9% uptime SLA
- Technology Stack: Python + FastAPI + PostgreSQL

**Functional Requirements**:
- Core Features: Create orders, retrieve order history, update order status, cancel orders, search/filter orders, webhook notifications for order events
- Data Models: Order (id, user_id, items, total, status, timestamps), OrderItem (product_id, quantity, price), Payment (method, status, transaction_id)
- Business Rules: Orders can only be cancelled within 1 hour of placement, refunds require manual approval for amounts > $500, orders transition through states (pending → confirmed → shipped → delivered)

**Non-Functional Requirements**:
- Authentication: OAuth 2.0 (authorization code flow for web/mobile, client credentials for B2B partners)
- Authorization: RBAC (customer, partner, admin roles) + resource ownership (users can only access their own orders)
- Rate Limiting: Customers: 100 req/min, Partners: 1000 req/min, Admins: unlimited
- Caching Strategy: ETags for order details (5-min TTL), CDN for product catalog
- Pagination: Cursor-based for order history (handles large datasets efficiently)
- API Versioning: URL versioning (/v1/, /v2/) with 12-month support window for N-1 version
- SLA Targets: 99.9% uptime, P95 latency < 300ms, P99 < 800ms
```

**Output:**

---

### 1. API Design Decision Record (ADR)

**Decision**: RESTful API (Richardson Maturity Model Level 2)

**Rationale**:
- **REST over GraphQL**: Order management has predictable access patterns (CRUD + list/search), doesn't require flexible querying like GraphQL. REST is simpler for mobile clients and third-party integrations.
- **REST over gRPC**: External partners need web-friendly protocol. gRPC is overkill for this use case (no high-frequency streaming needs).
- **Richardson Level 2** (HTTP verbs + status codes): Provides good RESTful design without complexity of Level 3 (HATEOAS). Clients don't need dynamic discovery of resources.

**Resource Modeling**:
- Primary resource: `/orders` (collection), `/orders/{orderId}` (item)
- Sub-resources: `/orders/{orderId}/items`, `/orders/{orderId}/payments`
- Actions as sub-resources: `/orders/{orderId}/cancel` (POST)

**Error Handling**: RFC 7807 Problem Details for all errors

**Versioning**: URL-based (`/v1/orders`) - Explicit, easy to route, clear for third-party partners

**Pagination**: Cursor-based (better performance for large datasets, no offset skipping issues)

**Authentication**: OAuth 2.0 with JWT access tokens (standard, good library support, supports multi-party access)

---

### 2. Resource Model & Endpoint Design

**Resources**:
1. **Orders** (primary resource)
2. **OrderItems** (sub-resource, embedded in order by default)
3. **Webhooks** (for event subscriptions)

**Endpoints**:

| Method | Endpoint | Description | Auth | Rate Limit |
|--------|----------|-------------|------|------------|
| GET | `/v1/orders` | List orders with filtering/pagination | OAuth 2.0 | 100/min |
| POST | `/v1/orders` | Create new order | OAuth 2.0 | 20/min |
| GET | `/v1/orders/{orderId}` | Retrieve single order | OAuth 2.0 | 100/min |
| PATCH | `/v1/orders/{orderId}` | Update order (admin only) | OAuth 2.0 | 50/min |
| POST | `/v1/orders/{orderId}/cancel` | Cancel order | OAuth 2.0 | 10/min |
| GET | `/v1/orders/{orderId}/items` | List order items | OAuth 2.0 | 100/min |
| POST | `/v1/webhooks` | Register webhook | OAuth 2.0 | 5/min |
| GET | `/v1/webhooks` | List webhooks | OAuth 2.0 | 20/min |
| DELETE | `/v1/webhooks/{webhookId}` | Unregister webhook | OAuth 2.0 | 10/min |

**Query Parameters** (for `/v1/orders`):
- `status`: Filter by order status (pending, confirmed, shipped, delivered, cancelled)
- `user_id`: Filter by user (admin only)
- `created_after`, `created_before`: Date range filtering
- `cursor`: Pagination cursor (opaque token)
- `limit`: Page size (max 100, default 20)
- `sort`: Sort order (created_at:desc, total:asc)

---

### 3. Complete OpenAPI 3.1 Specification

```yaml
openapi: 3.1.0
info:
  title: Order Management API
  version: 1.0.0
  description: |
    RESTful API for managing e-commerce orders, including creation, retrieval, 
    status updates, and webhook notifications.
    
    ## Features
    - OAuth 2.0 authentication
    - Cursor-based pagination
    - RFC 7807 error responses
    - Webhook event notifications
    - Rate limiting (100 req/min for customers, 1000 req/min for partners)
    
    ## Base URL
    - Production: https://api.example.com/v1
    - Staging: https://staging-api.example.com/v1
  contact:
    name: API Support
    email: api-support@example.com
    url: https://developer.example.com
  license:
    name: Proprietary
    url: https://example.com/terms

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

security:
  - OAuth2:
      - read:orders
      - write:orders

paths:
  /orders:
    get:
      summary: List orders
      description: Retrieve paginated list of orders with optional filtering
      operationId: listOrders
      tags:
        - Orders
      parameters:
        - name: status
          in: query
          description: Filter by order status
          required: false
          schema:
            type: string
            enum: [pending, confirmed, shipped, delivered, cancelled]
        - name: user_id
          in: query
          description: Filter by user ID (admin only)
          required: false
          schema:
            type: string
            format: uuid
        - name: created_after
          in: query
          description: Filter orders created after this timestamp
          required: false
          schema:
            type: string
            format: date-time
        - name: created_before
          in: query
          description: Filter orders created before this timestamp
          required: false
          schema:
            type: string
            format: date-time
        - name: cursor
          in: query
          description: Pagination cursor from previous response
          required: false
          schema:
            type: string
        - name: limit
          in: query
          description: Number of results per page (max 100, default 20)
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: sort
          in: query
          description: Sort order (field:direction)
          required: false
          schema:
            type: string
            enum: [created_at:desc, created_at:asc, total:desc, total:asc]
            default: created_at:desc
      responses:
        '200':
          description: Successful response with paginated orders
          headers:
            X-RateLimit-Limit:
              description: Rate limit ceiling for this endpoint
              schema:
                type: integer
                example: 100
            X-RateLimit-Remaining:
              description: Requests remaining in current window
              schema:
                type: integer
                example: 95
            X-RateLimit-Reset:
              description: Unix timestamp when rate limit resets
              schema:
                type: integer
                example: 1700000000
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Order'
                  pagination:
                    type: object
                    properties:
                      next_cursor:
                        type: string
                        description: Cursor for next page (null if last page)
                        nullable: true
                        example: "eyJpZCI6MTIzNDU2fQ=="
                      prev_cursor:
                        type: string
                        description: Cursor for previous page (null if first page)
                        nullable: true
                        example: null
                      has_more:
                        type: boolean
                        example: true
              example:
                data:
                  - id: "ord_1a2b3c4d5e"
                    user_id: "usr_9z8y7x6w5v"
                    status: "shipped"
                    total: 15999
                    currency: "USD"
                    items:
                      - product_id: "prod_abc123"
                        name: "Laptop"
                        quantity: 1
                        price: 12999
                      - product_id: "prod_def456"
                        name: "Mouse"
                        quantity: 2
                        price: 1500
                    payment:
                      method: "credit_card"
                      status: "completed"
                      transaction_id: "txn_xyz789"
                    created_at: "2025-11-17T10:30:00Z"
                    updated_at: "2025-11-17T12:45:00Z"
                pagination:
                  next_cursor: "eyJpZCI6MTIzNDU2fQ=="
                  prev_cursor: null
                  has_more: true
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/TooManyRequests'
        '500':
          $ref: '#/components/responses/InternalServerError'
      security:
        - OAuth2:
            - read:orders
    
    post:
      summary: Create order
      description: Create a new order with items and payment information
      operationId: createOrder
      tags:
        - Orders
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - user_id
                - items
                - payment
              properties:
                user_id:
                  type: string
                  format: uuid
                  description: ID of user placing order
                items:
                  type: array
                  minItems: 1
                  items:
                    type: object
                    required:
                      - product_id
                      - quantity
                    properties:
                      product_id:
                        type: string
                        description: Product identifier
                      quantity:
                        type: integer
                        minimum: 1
                        maximum: 100
                payment:
                  type: object
                  required:
                    - method
                  properties:
                    method:
                      type: string
                      enum: [credit_card, debit_card, paypal, apple_pay]
                    token:
                      type: string
                      description: Payment token from payment gateway
            example:
              user_id: "usr_9z8y7x6w5v"
              items:
                - product_id: "prod_abc123"
                  quantity: 1
                - product_id: "prod_def456"
                  quantity: 2
              payment:
                method: "credit_card"
                token: "tok_1a2b3c4d5e6f"
      responses:
        '201':
          description: Order created successfully
          headers:
            Location:
              description: URL of created order
              schema:
                type: string
                example: "/v1/orders/ord_1a2b3c4d5e"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '402':
          $ref: '#/components/responses/PaymentRequired'
        '429':
          $ref: '#/components/responses/TooManyRequests'
      security:
        - OAuth2:
            - write:orders
  
  /orders/{orderId}:
    get:
      summary: Retrieve order
      description: Get details of a specific order by ID
      operationId: getOrder
      tags:
        - Orders
      parameters:
        - name: orderId
          in: path
          required: true
          description: Order identifier
          schema:
            type: string
            pattern: '^ord_[a-zA-Z0-9]{10}$'
            example: "ord_1a2b3c4d5e"
      responses:
        '200':
          description: Order details
          headers:
            ETag:
              description: Entity tag for caching
              schema:
                type: string
                example: '"33a64df551425fcc55e4d42a148795d9f25f89d4"'
            Cache-Control:
              description: Caching directives
              schema:
                type: string
                example: "private, max-age=300"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '304':
          description: Not Modified (ETag matched)
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - OAuth2:
            - read:orders
    
    patch:
      summary: Update order
      description: Update order details (admin only, limited fields)
      operationId: updateOrder
      tags:
        - Orders
      parameters:
        - name: orderId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  enum: [confirmed, shipped, delivered]
                tracking_number:
                  type: string
            example:
              status: "shipped"
              tracking_number: "1Z999AA10123456784"
      responses:
        '200':
          description: Order updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - OAuth2:
            - write:orders
            - admin
  
  /orders/{orderId}/cancel:
    post:
      summary: Cancel order
      description: Cancel an order (only allowed within 1 hour of placement)
      operationId: cancelOrder
      tags:
        - Orders
      parameters:
        - name: orderId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: false
        content:
          application/json:
            schema:
              type: object
              properties:
                reason:
                  type: string
                  description: Reason for cancellation
            example:
              reason: "Found better price elsewhere"
      responses:
        '200':
          description: Order cancelled successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '404':
          $ref: '#/components/responses/NotFound'
        '409':
          description: Conflict - order cannot be cancelled (too late or already shipped)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
              example:
                type: "https://api.example.com/docs/errors/cancellation-not-allowed"
                title: "Cancellation Not Allowed"
                status: 409
                detail: "Order cannot be cancelled after 1 hour. Created at 2025-11-17T10:00:00Z, current time 2025-11-17T12:00:00Z"
                instance: "/v1/orders/ord_1a2b3c4d5e/cancel"
                order_id: "ord_1a2b3c4d5e"
                created_at: "2025-11-17T10:00:00Z"
                cancellation_deadline: "2025-11-17T11:00:00Z"
      security:
        - OAuth2:
            - write:orders

components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/oauth/authorize
          tokenUrl: https://auth.example.com/oauth/token
          scopes:
            read:orders: Read order data
            write:orders: Create and update orders
            admin: Administrative access
        clientCredentials:
          tokenUrl: https://auth.example.com/oauth/token
          scopes:
            read:orders: Read order data
            write:orders: Create and update orders
  
  schemas:
    Order:
      type: object
      required:
        - id
        - user_id
        - status
        - total
        - currency
        - items
        - created_at
      properties:
        id:
          type: string
          pattern: '^ord_[a-zA-Z0-9]{10}$'
          description: Unique order identifier
          example: "ord_1a2b3c4d5e"
        user_id:
          type: string
          format: uuid
          description: ID of user who placed order
        status:
          type: string
          enum: [pending, confirmed, shipped, delivered, cancelled]
          description: Current order status
        total:
          type: integer
          description: Total amount in cents
          minimum: 1
          example: 15999
        currency:
          type: string
          pattern: '^[A-Z]{3}$'
          description: ISO 4217 currency code
          example: "USD"
        items:
          type: array
          minItems: 1
          items:
            $ref: '#/components/schemas/OrderItem'
        payment:
          $ref: '#/components/schemas/Payment'
        tracking_number:
          type: string
          nullable: true
          description: Shipment tracking number (null if not shipped)
        created_at:
          type: string
          format: date-time
          description: Order creation timestamp (ISO 8601)
        updated_at:
          type: string
          format: date-time
          description: Last update timestamp (ISO 8601)
    
    OrderItem:
      type: object
      required:
        - product_id
        - name
        - quantity
        - price
      properties:
        product_id:
          type: string
          description: Product identifier
        name:
          type: string
          description: Product name (snapshot at order time)
        quantity:
          type: integer
          minimum: 1
          maximum: 100
        price:
          type: integer
          description: Unit price in cents (snapshot at order time)
          minimum: 0
    
    Payment:
      type: object
      required:
        - method
        - status
      properties:
        method:
          type: string
          enum: [credit_card, debit_card, paypal, apple_pay]
        status:
          type: string
          enum: [pending, completed, failed, refunded]
        transaction_id:
          type: string
          description: Payment gateway transaction ID
          nullable: true
    
    ProblemDetails:
      type: object
      description: RFC 7807 Problem Details for HTTP APIs
      required:
        - type
        - title
        - status
      properties:
        type:
          type: string
          format: uri
          description: URI reference identifying the problem type
          example: "https://api.example.com/docs/errors/insufficient-funds"
        title:
          type: string
          description: Short, human-readable summary
          example: "Insufficient Funds"
        status:
          type: integer
          description: HTTP status code
          example: 402
        detail:
          type: string
          description: Human-readable explanation specific to this occurrence
          example: "Account balance is $50, transaction amount is $100"
        instance:
          type: string
          format: uri
          description: URI reference identifying the specific occurrence
          example: "/v1/orders/ord_1a2b3c4d5e"
  
  responses:
    BadRequest:
      description: Bad Request - Invalid input
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
          example:
            type: "https://api.example.com/docs/errors/validation-error"
            title: "Validation Error"
            status: 400
            detail: "Invalid order data: quantity must be between 1 and 100"
            instance: "/v1/orders"
            errors:
              - field: "items[0].quantity"
                message: "must be <= 100"
                value: 150
    
    Unauthorized:
      description: Unauthorized - Missing or invalid authentication
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
          example:
            type: "https://api.example.com/docs/errors/unauthorized"
            title: "Unauthorized"
            status: 401
            detail: "Access token is missing or invalid"
            instance: "/v1/orders"
    
    Forbidden:
      description: Forbidden - Insufficient permissions
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
          example:
            type: "https://api.example.com/docs/errors/forbidden"
            title: "Forbidden"
            status: 403
            detail: "You don't have permission to access this order"
            instance: "/v1/orders/ord_1a2b3c4d5e"
    
    NotFound:
      description: Not Found - Resource doesn't exist
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
          example:
            type: "https://api.example.com/docs/errors/not-found"
            title: "Not Found"
            status: 404
            detail: "Order not found: ord_1a2b3c4d5e"
            instance: "/v1/orders/ord_1a2b3c4d5e"
    
    PaymentRequired:
      description: Payment Required - Payment processing failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
          example:
            type: "https://api.example.com/docs/errors/payment-failed"
            title: "Payment Failed"
            status: 402
            detail: "Card declined: insufficient funds"
            instance: "/v1/orders"
            payment_error_code: "card_declined"
    
    TooManyRequests:
      description: Too Many Requests - Rate limit exceeded
      headers:
        Retry-After:
          description: Seconds to wait before retrying
          schema:
            type: integer
            example: 60
        X-RateLimit-Limit:
          schema:
            type: integer
            example: 100
        X-RateLimit-Remaining:
          schema:
            type: integer
            example: 0
        X-RateLimit-Reset:
          schema:
            type: integer
            example: 1700000000
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
          example:
            type: "https://api.example.com/docs/errors/rate-limit-exceeded"
            title: "Rate Limit Exceeded"
            status: 429
            detail: "Rate limit of 100 requests per minute exceeded. Retry after 60 seconds."
            instance: "/v1/orders"
            limit: 100
            window: "1 minute"
            retry_after: 60
    
    InternalServerError:
      description: Internal Server Error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
          example:
            type: "https://api.example.com/docs/errors/internal-error"
            title: "Internal Server Error"
            status: 500
            detail: "An unexpected error occurred. Contact support with incident ID."
            instance: "/v1/orders"
            incident_id: "inc_abc123xyz"
```

---

### 4. Security Analysis (STRIDE Threat Model)

| Threat | Risk | Mitigation |
|--------|------|------------|
| **Spoofing** (Authentication bypass) | HIGH - Attackers impersonate users to access/modify orders | - OAuth 2.0 with short-lived access tokens (1-hour expiry)<br>- JWT signature verification<br>- TLS 1.3 for all connections<br>- mTLS for partner integrations |
| **Tampering** (Data modification) | HIGH - Attackers modify order data (prices, quantities) | - Input validation (JSON schema validation)<br>- Business rule enforcement (server-side price checks)<br>- Audit logging of all mutations<br>- Database constraints and triggers |
| **Repudiation** (Denying actions) | MEDIUM - Users deny placing orders | - Comprehensive audit logging (who, what, when, IP address)<br>- Immutable event log (order history)<br>- Email confirmations with order details<br>- Log retention: 7 years (compliance) |
| **Information Disclosure** (Data leakage) | HIGH - PII/PCI exposure | - Authorization checks (users can only access own orders)<br>- Role-based access (admin, customer, partner)<br>- PCI-DSS compliance (no card data stored, use tokens)<br>- TLS 1.3 encryption in transit<br>- Sensitive data masking in logs |
| **Denial of Service** (Resource exhaustion) | MEDIUM - API flooding | - Rate limiting (100 req/min per user, 1K/min per partner)<br>- Request size limits (max 1MB payload)<br>- Query complexity limits (max 100 items per order)<br>- Timeout (30s per request)<br>- CDN/WAF for DDoS protection |
| **Elevation of Privilege** (Unauthorized access) | HIGH - Attackers gain admin rights | - Principle of least privilege (scoped OAuth tokens)<br>- Separate admin endpoints with stricter auth<br>- Multi-factor authentication for admin users<br>- Regular permission audits |

**Additional Security Measures**:
- **API Key Rotation**: Partners must rotate API keys every 90 days
- **Webhook Signature Verification**: HMAC-SHA256 signatures on webhook payloads
- **CORS Policy**: Whitelist allowed origins for browser-based clients
- **Content Security Policy**: Prevent XSS in API documentation pages

---

### 5. Rate Limiting & Throttling Strategy

**Rate Limit Tiers**:
| User Type | Requests/Minute | Requests/Hour | Requests/Day |
|-----------|----------------|---------------|--------------|
| **Free Customer** | 60 | 1,000 | 10,000 |
| **Premium Customer** | 100 | 5,000 | 50,000 |
| **Partner (B2B)** | 1,000 | 50,000 | 500,000 |
| **Admin** | Unlimited | Unlimited | Unlimited |

**HTTP Headers** (every response):
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1700000000  (Unix timestamp)
X-RateLimit-Tier: premium
```

**429 Too Many Requests Response**:
```json
{
  "type": "https://api.example.com/docs/errors/rate-limit-exceeded",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "Rate limit of 100 requests per minute exceeded. Retry after 60 seconds.",
  "instance": "/v1/orders",
  "limit": 100,
  "window": "1 minute",
  "retry_after": 60
}
```

**Retry-After Header**: `Retry-After: 60` (seconds)

**Burst Handling**:
- Allow burst of up to 20 requests over limit in 1-second window
- Use token bucket algorithm (not fixed window) to avoid reset stampede

**Endpoint-Specific Overrides**:
- `POST /orders`: 20 req/min (more expensive operation)
- `POST /orders/{id}/cancel`: 10 req/min (prevent abuse)
- `GET /orders`: 100 req/min (read-heavy, less expensive)

**Partner Rate Limit Exceeded Notifications**:
- Send email alert at 80% of quota
- Provide usage dashboard at `/v1/usage` endpoint

---

### 6. Versioning & Deprecation Policy

**Version Format**: Semantic versioning (MAJOR.MINOR.PATCH)
- **MAJOR** (v1 → v2): Breaking changes (e.g., remove endpoint, change response structure)
- **MINOR** (v1.1 → v1.2): Backward-compatible features (e.g., new optional field)
- **PATCH** (v1.1.0 → v1.1.1): Bug fixes only

**URL Versioning**: `/v1/orders`, `/v2/orders` (explicit, easy to route)

**Support Timeline**:
- **Current version** (v2): Full support, all new features
- **Previous version** (v1): Maintained for 12 months after v2 launch
  - Bug fixes only, no new features
  - Security patches continue
- **Deprecated version** (v1 after 12 months): 
  - 6-month deprecation notice via email, API headers, documentation
  - `Sunset` HTTP header: `Sunset: Sat, 31 Dec 2025 23:59:59 GMT`
  - Warning in response: `X-API-Warn: "This API version is deprecated. Migrate to /v2/ by Dec 31, 2025"`
  - Return 410 Gone after sunset date

**Breaking vs Non-Breaking Changes**:

**Breaking Changes** (require new major version):
- Remove endpoint or field
- Change field type (string → integer)
- Change HTTP status code for existing behavior
- Make optional field required
- Change authentication method
- Rename field

**Non-Breaking Changes** (can be done in minor version):
- Add new endpoint
- Add new optional field
- Add new HTTP status code (e.g., add 429)
- Make required field optional
- Expand enum values (if clients use unknown-value handling)
- Add new query parameter

**Migration Guide** (v1 → v2 example):
- Side-by-side comparison table
- Code examples (before/after)
- Automated migration tool (SDK method to convert v1 requests → v2)
- Deprecation timeline and milestones

---

### 7. Client SDK Generation Plan

**Supported Languages**:
- Python, JavaScript/TypeScript, Java, Go, Ruby, PHP, C#

**SDK Generation**:
```bash
# Using OpenAPI Generator
openapi-generator generate \
  -i openapi.yaml \
  -g python \
  -o clients/python \
  --additional-properties=packageName=order_api_client

# Generates:
# - Authentication helpers
# - Type-safe request/response models
# - Pagination utilities
# - Error handling
# - Retry logic with exponential backoff
```

**Python SDK Example**:
```python
from order_api_client import OrderAPI, Configuration

# Configure OAuth 2.0
config = Configuration(
    access_token="your_oauth_token"
)
client = OrderAPI(config)

# List orders with pagination
orders = client.orders.list(
    status="shipped",
    limit=50,
    cursor=None
)

for order in orders.data:
    print(f"Order {order.id}: {order.total/100} {order.currency}")

# Auto-pagination
for order in client.orders.list_all_pages(status="delivered"):
    print(order.id)

# Create order
new_order = client.orders.create(
    user_id="usr_123",
    items=[
        {"product_id": "prod_abc", "quantity": 2}
    ],
    payment={"method": "credit_card", "token": "tok_xyz"}
)
print(f"Created order: {new_order.id}")
```

**SDK Features**:
- Automatic retry with exponential backoff (3 retries, 1s/2s/4s delays)
- Rate limit handling (parse `Retry-After`, sleep automatically)
- Pagination helpers (`list_all_pages()` generator)
- Type hints/annotations (Python, TypeScript)
- Comprehensive error handling (typed exceptions per HTTP status)

---

### 8. API Documentation Strategy

**Interactive Documentation**:
- **Swagger UI**: https://api.example.com/docs (auto-generated from OpenAPI spec)
- **Redoc**: https://api.example.com/redoc (alternative, cleaner UI)
- **Stoplight Elements**: Embedded in developer portal

**Developer Portal** (https://developer.example.com):
1. **Getting Started Guide**
   - Create account → get API keys → make first request (5-min quickstart)
   - Authentication tutorial (OAuth 2.0 flow walkthrough)
   - Postman collection import

2. **Use Case Guides**
   - "Create an order and track shipment" (step-by-step with code)
   - "Set up webhooks for order events" (with signature verification)
   - "Handle rate limits gracefully" (retry logic examples)

3. **API Reference** (auto-generated from OpenAPI)
   - Endpoint list with descriptions
   - Request/response examples
   - Try-it console (authenticated)

4. **SDKs & Tools**
   - Download SDKs (Python, JS, Java, etc.)
   - Postman collection
   - Insomnia workspace

5. **Changelog**
   - Version history
   - Breaking changes highlighted
   - Migration guides

**Postman Collection**:
- Pre-configured requests for all endpoints
- Environment variables for API keys
- Examples with realistic data
- Tests for assertions (status code, response schema)

---

## Tips

- **Design API contract first**: Write OpenAPI spec before implementation to align frontend/backend teams
- **Validate OpenAPI spec**: Use Swagger Editor or `openapi-generator validate` to catch errors early
- **Test with real clients**: Use SDKs to verify ergonomics (are common tasks easy?)
- **Version from day 1**: Even if you think the API is "final," add `/v1/` to allow future evolution
- **Use RFC 7807 Problem Details**: Structured errors are machine-readable, easier to debug, and better for client error handling
- **Cursor-based pagination**: For large datasets, cursor-based is faster and more reliable than offset-based (no skipped/duplicate results)
- **Cache with ETags**: For frequently accessed resources (GET /orders/{id}), use ETags to reduce bandwidth and server load
- **Rate limiting**: Start conservative (100 req/min), increase as needed. Monitor P95/P99 latency to detect abuse.
- **Security**: Never trust client input, validate everything server-side (prices, quantities, business rules)
- **HATEOAS (Level 3) not always needed**: If clients are tightly coupled (your own mobile/web apps), Level 2 is often sufficient
- **GraphQL alternative**: If clients need flexible querying (e.g., "get order with only items, no payment"), consider GraphQL over REST

## Related Prompts

- **[microservices-architect](./microservices-architect.md)** - Design service boundaries and inter-service APIs
- **[security-code-auditor](./security-code-auditor.md)** - Audit API implementation for vulnerabilities (OWASP API Security Top 10)
- **[devops-pipeline-architect](./devops-pipeline-architect.md)** - Set up CI/CD with API contract testing
- **[database-schema-designer](./database-schema-designer.md)** - Design database schema for API data models
- **[test-automation-engineer](./test-automation-engineer.md)** - Write integration tests for API endpoints

## Related Workflows

- **[SDLC Blueprint](../../docs/workflows/sdlc-blueprint.md)** - Phase 2 (Design) includes API contract design step

## Governance Notes

- **Approval Required**: Staff Engineer or API Architect must review API designs before implementation
- **Human Review**: All breaking changes (v1 → v2) require cross-team review
- **Audit Requirements**: Save API design ADRs for 5 years (architecture decisions)
- **Risk Level**: High - API contracts are hard to change once clients depend on them
- **Compliance**: SOC2 (secure development practices), GDPR (data protection, right to be forgotten)

## Changelog

### Version 2.0 (2025-11-17)
- **MAJOR UPLIFT**: Elevated from Tier 3 (3/10) to Tier 1 (9/10)
- Added comprehensive OpenAPI 3.1 specification with complete Order Management API example
- Added Richardson Maturity Model guidance and ADR template
- Added STRIDE threat model for security analysis
- Added detailed rate limiting strategy with tiered limits and HTTP headers
- Added versioning and deprecation policy (12-month support window, Sunset header)
- Added RFC 7807 Problem Details for standardized error handling
- Added client SDK generation plan with Python SDK example
- Added API documentation strategy (Swagger UI, developer portal, Postman collection)
- Added governance metadata (Staff Engineer approval, 5-year retention, high risk level)
- Added research foundation (Fielding REST, RFC 7231/7807, OpenAPI 3.1)
- Added cursor-based pagination, ETag caching, OAuth 2.0 security schemes
- Added realistic e-commerce API example with 800+ lines of validated OpenAPI YAML

### Version 1.0 (2025-11-16)
- Initial version migrated from legacy prompt library
- Basic API design structure


