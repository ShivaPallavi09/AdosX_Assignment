# Architectural Decisions

### 1. Ingestion Strategy: Raw Storage vs. Eager Validation
- **Decision:** Store all fields as `CharField` (text) in the database and handle normalization in the comparison logic.
- **Alternative:** Use integer/decimal database fields and strict foreign key constraints between systems.
- **Reasoning:** The provided CSV exports contain malformed IDs, unparseable numbers, and missing references; strict database constraints would silently drop rows during ingestion, violating the core requirement.

### 2. Multi-Tenancy Enforcement Layer
- **Decision:** Enforce multi-tenant isolation at the API service layer by requiring and filtering against an `org_id` query parameter on every read.
- **Alternative:** Separate database schemas per tenant or complex row-level database security.
- **Reasoning:** The assignment explicitly requested to skip authentication while maintaining strict boundary safety; query-layer scoping is concise, testable, and prevents accidental data leaks without over-engineering.

### 3. Comparison Compute: Domain Service vs. Database SQL Joins
- **Decision:** Perform data reconciliation using an in-memory Python service with dictionary mappings (`O(N)` time complexity).
- **Alternative:** Execute complex SQL `FULL OUTER JOIN` queries with database-specific regex normalization functions.
- **Reasoning:** With the dataset size constrained (120 rows), in-memory Python reconciliation runs instantly, is easily unit-tested without a live test database, and separates business logic from infrastructure.