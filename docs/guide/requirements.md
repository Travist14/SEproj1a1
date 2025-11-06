# Generating Requirements

Best practices and techniques for generating high-quality requirements with MARC.

## Effective Prompting

### The SPARK Framework

Use **SPARK** to write effective requirement prompts:

- **S**pecific: Clear, unambiguous feature description
- **P**urpose: Why this is needed
- **A**udience: Who will use it
- **R**equirements: Any constraints or must-haves
- **K**ontext: Domain, scale, environment

### Examples

**Basic**:
```
Build user authentication
```

**Using SPARK**:
```
Build email/password authentication for a healthcare SaaS application
serving 10K+ users. Must be HIPAA-compliant, support 2FA, and integrate
with existing MySQL database. Target: hospital administrators and medical staff.
```

## IEEE 29148 Compliance

MARC generates requirements following IEEE 29148 standards. Every requirement includes:

### Required Sections

**REQ-ID**: Unique identifier
```
Format: REQ-{PERSONA}-{NUMBER}
Example: REQ-DEV-001
```

**Category**: Requirement type
- Functional
- Non-functional
- Performance
- Security
- Usability

**Priority**: Importance level
- High: Critical, must-have
- Medium: Important, should-have
- Low: Nice-to-have

**Description**: Clear statement of what is required

**Rationale**: Why this requirement exists

**Acceptance Criteria**: Testable conditions for completion

**Dependencies**: Related requirements or systems

**Verification Method**: How to test/validate

## Common Patterns

### Pattern 1: CRUD Operations

```
Create a REST API for managing products in an e-commerce system.
Support Create, Read, Update, Delete operations with pagination and filtering.
```

### Pattern 2: Integration

```
Integrate with Stripe payment API to process credit card transactions
with webhook support for asynchronous payment confirmations.
```

### Pattern 3: Dashboard/Reporting

```
Build analytics dashboard showing user engagement metrics with real-time
updates, exportable reports, and role-based access control.
```

### Pattern 4: Authentication/Authorization

```
Implement OAuth 2.0 authentication with role-based access control (RBAC)
supporting Admin, Editor, and Viewer roles.
```

### Pattern 5: Data Processing

```
Create background job processor for processing CSV files up to 1GB,
with progress tracking, error handling, and email notifications.
```

## Iterative Refinement

### Step 1: Initial Generation

Start broad:
```
Build a blog system
```

### Step 2: Review Output

Look for gaps in the generated requirement.

### Step 3: Add Details

Refine your prompt:
```
Build a blog system with markdown support, image uploads, comments,
tags, and RSS feed generation for a technical documentation site.
```

### Step 4: Persona Switching

Try different personas for different aspects:
- Developer: Technical implementation
- Customer: User experience
- Product Manager: Business value

## Quality Checklist

### Good Requirements Are:

✅ **Unambiguous**: One clear interpretation
❌ Bad: "The system should be fast"
✅ Good: "API responses should complete within 200ms for 95% of requests"

✅ **Testable**: Can verify completion
❌ Bad: "Users should find it easy to use"
✅ Good: "90% of users complete signup within 2 minutes without assistance"

✅ **Necessary**: Actually needed
❌ Bad: "Support 1 billion concurrent users" (for a startup MVP)
✅ Good: "Support 10K concurrent users with horizontal scaling capability"

✅ **Feasible**: Technically possible
❌ Bad: "AI that reads user's mind"
✅ Good: "AI that suggests features based on usage patterns"

✅ **Traceable**: Linked to business need
❌ Bad: "Use microservices because it's trendy"
✅ Good: "Use microservices to enable independent team scaling"

## Domain-Specific Tips

### Healthcare/HIPAA

Always mention:
- Compliance requirements (HIPAA, GDPR)
- Data sensitivity
- Audit trail needs
- Access control

```
Build patient record system with HIPAA-compliant encryption, audit logging,
role-based access, and automatic session timeout.
```

### Finance/PCI-DSS

Always mention:
- Security standards (PCI-DSS)
- Transaction handling
- Fraud prevention
- Regulatory reporting

```
Implement payment processing system compliant with PCI-DSS, supporting
fraud detection, chargeback handling, and regulatory reporting.
```

### E-commerce

Always mention:
- Scale (users, products, transactions)
- Payment methods
- Inventory management
- Order fulfillment

```
Build shopping cart for 100K+ products, supporting multiple payment methods,
real-time inventory, and integration with ShipStation for fulfillment.
```

### SaaS/Multi-tenant

Always mention:
- Tenancy model
- Data isolation
- Per-tenant customization
- Billing/metering

```
Create multi-tenant SaaS platform with tenant data isolation, customizable
branding, usage-based billing, and admin dashboard per tenant.
```

## Advanced Techniques

### Technique 1: Negative Requirements

Specify what should NOT happen:

```
Build file upload system that accepts images up to 10MB. Do NOT allow
executable files, scripts, or files with double extensions.
```

### Technique 2: Performance Targets

Include specific metrics:

```
Implement search functionality returning results within 100ms for
datasets up to 1M records, supporting fuzzy matching and filters.
```

### Technique 3: Edge Cases

Mention unusual scenarios:

```
Build checkout system handling partial payment failures, inventory
depletion during checkout, and concurrent purchase attempts.
```

### Technique 4: Evolution Path

Indicate future scalability:

```
Build authentication system starting with email/password, but
architected to easily add social login, SSO, and biometric auth later.
```

## Troubleshooting

### Issue: Vague Requirements

**Problem**: Generated requirements lack detail

**Solution**: Add more context to your prompt
```
Before: "Add search"
After: "Add full-text search across products, categories, and brands with
autocomplete, filters, and sorting options"
```

### Issue: Wrong Persona Focus

**Problem**: Technical requirements from Customer persona

**Solution**: Use Developer persona for technical specs

### Issue: Missing Sections

**Problem**: No acceptance criteria generated

**Solution**: Explicitly request: "Include specific, testable acceptance criteria"

### Issue: Unrealistic Requirements

**Problem**: Requirements that can't be built

**Solution**: Add constraints: "Build MVP version for 1K users in 2-month timeline"

## Next Steps

- [Using Personas](personas.md) - Choose the right perspective
- [Testing Guide](testing.md) - Validate your requirements
- [API Reference](../api/rest-api.md) - Automate the workflow
