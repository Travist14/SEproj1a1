# Using Personas

Learn how to effectively use MARC's five stakeholder personas to generate comprehensive requirements.

## Overview

MARC simulates five distinct stakeholder perspectives, each bringing unique concerns and priorities to requirements engineering.

## The Five Personas

### Developer

**Focus**: Technical feasibility and implementation

**Key Concerns**:
- Implementation complexity
- Technical dependencies
- Security and performance
- Code maintainability
- Integration with existing systems

**Best For**:
- Technical requirements
- Architecture decisions
- Security and performance specs
- API and interface definitions

**Example Output**:
```
REQ-DEV-001: User Authentication System

Category: Security
Priority: High

Description:
Implement secure user authentication using email and password with
bcrypt hashing, JWT tokens, and rate limiting.

Rationale:
Secure authentication is critical for protecting user data and preventing
unauthorized access. Industry-standard encryption prevents common attacks.

Acceptance Criteria:
- Password hashing with bcrypt (10+ rounds)
- JWT tokens with 24-hour expiration
- Rate limiting: 5 failed attempts per 15 minutes
- HTTPS-only cookie for token storage

Dependencies:
- bcrypt library
- JWT library
- Redis for rate limiting

Verification Method:
- Unit tests for authentication logic
- Security audit for password handling
- Integration tests for login flow
```

---

### Product Manager

**Focus**: User value and business metrics

**Key Concerns**:
- User stories and value
- Business KPIs
- Feature prioritization
- Success metrics
- Competitive differentiation

**Best For**:
- User-centric requirements
- Business value definition
- Success criteria
- Product roadmap alignment

**Example Output**:
```
REQ-PM-001: User Authentication Feature

Category: Functional
Priority: High

Description:
Enable users to create accounts and securely log in to access personalized
features and data.

Rationale:
Authentication is table stakes for modern web applications. Enables
personalization, user retention, and data security. Competitive parity.

Acceptance Criteria:
- Users can register with email in < 1 minute
- Login success rate > 95%
- Password reset flow < 3 steps
- Social login option for convenience
- WCAG 2.1 AA accessibility compliance

Dependencies:
- Email service integration
- OAuth providers (Google, GitHub)

Verification Method:
- User testing with 10+ participants
- Analytics tracking for signup conversion
- A/B test social vs email signup
```

---

### Customer

**Focus**: Usability and user experience

**Key Concerns**:
- Ease of use
- Minimal friction
- Clear error messages
- Accessibility
- Mobile experience

**Best For**:
- UX requirements
- Accessibility needs
- User pain points
- Simplicity constraints

**Example Output**:
```
REQ-CUST-001: Easy Login Experience

Category: Usability
Priority: High

Description:
Provide a simple, intuitive login process that doesn't frustrate users
with complex requirements or confusing flows.

Rationale:
Complex authentication frustrates users and leads to abandonment. Users
value simplicity and speed over strict password policies.

Acceptance Criteria:
- Login form visible without scrolling
- Clear error messages ("Invalid password" not "Error 401")
- Password visibility toggle
- "Remember me" option
- Obvious "Forgot password?" link
- No CAPTCHA unless suspicious activity

Dependencies:
- Mobile-responsive design
- Clear copywriting

Verification Method:
- User testing sessions
- Usability heuristic evaluation
- Task completion time < 30 seconds
```

---

### Sales

**Focus**: Value proposition and competitive advantage

**Key Concerns**:
- Customer acquisition
- Selling points
- Competitive differentiation
- Demos and trials
- Customer objections

**Best For**:
- Market differentiation
- Sales enablement features
- Demo capabilities
- Customer-facing features

**Example Output**:
```
REQ-SAL-001: Enterprise Authentication Options

Category: Functional
Priority: Medium

Description:
Support enterprise SSO (Single Sign-On) via SAML and OAuth to enable
sales to large organizations requiring centralized authentication.

Rationale:
Enterprise customers demand SSO integration. This is often a deal-breaker
for sales to Fortune 500 companies. Competitive advantage over smaller
competitors.

Acceptance Criteria:
- SAML 2.0 support for enterprise SSO
- OAuth 2.0 for modern cloud providers
- Admin dashboard for authentication settings
- Audit logs for compliance
- Support for Active Directory integration

Dependencies:
- SAML library
- Enterprise sales collateral
- Support team training

Verification Method:
- Successfully integrate with 3+ enterprise IdPs
- Sales team demo capability
- Customer POC success
```

---

### Shareholder

**Focus**: Financial returns and strategic value

**Key Concerns**:
- Return on investment
- Cost vs benefit
- Strategic alignment
- Market opportunity
- Competitive positioning

**Best For**:
- Business case justification
- Cost-benefit analysis
- Strategic priorities
- Investment decisions

**Example Output**:
```
REQ-SH-001: Authentication Infrastructure Investment

Category: Strategic
Priority: Medium

Description:
Invest in robust, scalable authentication infrastructure that supports
current and future authentication methods with minimal ongoing costs.

Rationale:
One-time investment in proper authentication infrastructure prevents
costly rework and security breaches. Enables enterprise sales (higher
LTV customers). Reduces support costs through better UX.

Acceptance Criteria:
- Development cost < $50K
- Supports 100K+ concurrent users
- < 2% authentication-related support tickets
- Enables enterprise sales (average contract $100K+)
- Security audit certification

Dependencies:
- Cloud infrastructure budget
- Security team capacity

Verification Method:
- Financial analysis showing positive ROI within 12 months
- Enterprise sales pipeline growth
- Support ticket volume tracking
```

---

## Choosing the Right Persona

### Single Persona Selection

Choose based on your primary concern:

| Concern | Persona | Example |
|---------|---------|---------|
| How to build it? | Developer | "What tech stack?" |
| What's the value? | Product Manager | "Will users want this?" |
| Is it easy to use? | Customer | "Can my grandma use it?" |
| Can we sell it? | Sales | "What's the pitch?" |
| Is it worth it? | Shareholder | "What's the ROI?" |

### Multi-Persona Strategy

For comprehensive requirements, generate from multiple perspectives:

**Recommended Order**:
1. **Product Manager** - Define user value and business case
2. **Customer** - Identify usability requirements
3. **Developer** - Assess technical feasibility
4. **Sales** - Add competitive differentiation
5. **Shareholder** - Validate financial viability

**Synthesis**:
Compare outputs and look for:
- Conflicts (Developer: "Takes 6 months" vs Shareholder: "Need it in 1 month")
- Overlaps (All agree authentication is High priority)
- Gaps (No one mentioned mobile support)

## Tips for Better Results

### Be Specific

❌ Bad: "I need user management"
✅ Good: "I need user registration with email verification for a healthcare SaaS application"

### Add Context

❌ Bad: "Build payment processing"
✅ Good: "Build Stripe payment processing for subscription-based SaaS with monthly and annual plans"

### Include Constraints

❌ Bad: "Add search functionality"
✅ Good: "Add search functionality that returns results in < 100ms for datasets up to 1M records"

### Use Domain Language

❌ Bad: "Track stuff"
✅ Good: "Implement HIPAA-compliant patient record tracking for medical clinics"

## Examples by Domain

### E-commerce
```
Persona: Product Manager
Prompt: "Build a shopping cart with add/remove items, quantity adjustment,
and persistent cart across sessions for a fashion e-commerce site"
```

### Healthcare
```
Persona: Developer
Prompt: "Create HIPAA-compliant patient appointment scheduling system with
real-time availability, automated reminders, and EHR integration"
```

### Finance
```
Persona: Shareholder
Prompt: "Implement real-time stock portfolio tracking with alerts, risk
analysis, and SEC filing integration for retail investors"
```

### Education
```
Persona: Customer
Prompt: "Build online course platform with video lectures, quizzes, progress
tracking, and certificates for adult learners"
```

## Next Steps

- [Generating Requirements](requirements.md) - Best practices for prompting
- [Testing Guide](testing.md) - Validate your requirements
- [API Reference](../api/rest-api.md) - Automate requirement generation
