"""
Mock LLM responses for testing MARC personas.
These responses simulate what each persona would generate.
"""

DEVELOPER_RESPONSES = {
    "authentication_requirement": """
Thank you for sharing that requirement. Let me help you formalize it from a developer perspective.

REQ-DEV-001: OAuth2 Authentication System
Category: Functional
Priority: Must-have

Description: The system shall implement OAuth2 authentication to securely authenticate users.

Acceptance Criteria:
- Support OAuth2 authorization code flow
- Integrate with at least two providers (Google, GitHub)
- Secure token storage using encrypted database fields
- Session management with JWT tokens
- Token refresh mechanism for expired sessions
- Proper error handling for failed authentication attempts

Technical Notes:
- Use industry-standard OAuth2 library (e.g., Authlib, OAuthLib)
- Implement PKCE for enhanced security
- Store tokens with AES-256 encryption
- Rate limit authentication attempts to prevent brute force
- Implement proper logging for security auditing
- Consider Redis for session storage to improve performance

Dependencies:
- REQ-DEV-002 (User Database Schema)
- REQ-DEV-003 (HTTPS Configuration)

Questions for clarification:
1. What is the expected authentication latency threshold?
2. Do we need to support single sign-on (SSO)?
3. What is our token expiration policy?
4. How do we handle account lockout after failed attempts?
""",

    "api_rate_limiting": """
REQ-DEV-002: API Rate Limiting
Category: Non-Functional (Performance & Security)
Priority: Must-have

Description: The system shall implement rate limiting on all API endpoints to prevent abuse and ensure fair resource allocation.

Acceptance Criteria:
- Implement 100 requests per minute limit per authenticated user
- Implement 20 requests per minute limit per IP for unauthenticated requests
- Return HTTP 429 status code when limit is exceeded
- Include Retry-After header in 429 responses
- Provide clear error messages indicating limit and reset time
- Allow configuration of rate limits per endpoint

Technical Notes:
- Use Redis with sliding window algorithm for distributed rate limiting
- Implement rate limit middleware in API gateway
- Add monitoring for rate limit violations
- Consider tiered rate limits for premium users
- Cache rate limit state with 1-second TTL

Dependencies: REQ-DEV-004 (Redis Infrastructure)

Performance Considerations:
- Rate limit check should add < 5ms latency
- Redis should handle 10,000 checks per second
""",
}

PM_RESPONSES = {
    "engagement_dashboard": """
I appreciate you sharing this requirement. Let's make sure we capture the user value clearly.

REQ-PM-001: User Engagement Analytics Dashboard
Category: User Story
Priority: Must-have (P0)

User Story: As a product manager, I want to view user engagement metrics in a centralized dashboard so that I can make data-driven decisions about product improvements and identify areas needing attention.

Description: The system shall provide a comprehensive dashboard displaying key user engagement metrics with filtering and export capabilities.

Acceptance Criteria:
- Display daily active users (DAU) for the last 30 days
- Show weekly active users (WAU) and monthly active users (MAU)
- Display 7-day and 30-day retention curves
- Show feature adoption rates for key features
- Allow filtering by user segment and date range
- Enable export to CSV and PDF formats
- Update metrics in near real-time (< 5 minute delay)
- Display comparative metrics (week-over-week, month-over-month)

Success Metrics:
- Product team uses dashboard at least 3x per week
- Decision cycle time reduces by 30%
- 90% of stakeholders rate dashboard as "useful" or "very useful"
- Data export feature used at least weekly

Business Value:
- Enables faster, data-driven product decisions
- Reduces time spent on manual data gathering
- Improves visibility into product performance
- Supports quarterly business reviews with concrete metrics

Dependencies:
- REQ-DEV-010 (Analytics Data Pipeline)
- REQ-PM-002 (User Segmentation)

Open Questions:
1. Which user segments are highest priority to track?
2. Do we need predictive analytics or just historical data?
3. Should we support custom metric definitions?
4. What level of drill-down detail is needed?
""",

    "social_sharing": """
REQ-PM-002: Social Media Sharing Feature
Category: Feature
Priority: Should-have (P1)

User Story: As a user, I want to share my achievements on social media so that I can engage with my network and increase awareness of the platform.

Description: Users shall be able to share content and achievements to major social media platforms directly from the application.

Acceptance Criteria:
- Support sharing to Facebook, Twitter, and LinkedIn
- Include pre-populated share text with customization option
- Attach relevant images or screenshots automatically
- Track share events in analytics
- Require user consent before sharing
- Display preview before posting
- Handle share failures gracefully with retry option

Success Metrics:
- 10% of users share at least once per month
- 15% of new user acquisition attributed to social shares
- Viral coefficient increases by 0.2
- Social shares grow 25% month-over-month

Market Context:
- Competitor A has basic sharing, Competitor B has advanced sharing with templates
- User research shows 40% of users interested in sharing achievements
- Industry benchmarks suggest 8-12% share rate

Go-to-Market Considerations:
- Feature launch coordinated with marketing campaign
- Press release highlighting social integration
- Email campaign to existing users promoting the feature

Dependencies: REQ-DEV-015 (Social Media API Integration)
""",
}

CUSTOMER_RESPONSES = {
    "password_reset": """
Thank you for considering this feature. Let me share the customer perspective.

REQ-CUST-001: Password Reset Functionality
Category: Usability
Priority: Must-have

Customer Story: As a customer, I need to reset my password when I forget it so that I can regain access to my account without frustration or delay.

Description: The system shall provide a simple, secure password reset process that customers can complete independently.

Acceptance Criteria:
- Password reset link on login page is clearly visible
- Reset process requires only email address (no security questions to forget)
- Reset email arrives within 1 minute
- Reset link remains valid for 24 hours
- Clear instructions in email with single-click reset link
- Password requirements clearly displayed on reset page
- Confirmation message after successful reset
- Option to contact support if email not received
- Works on mobile devices without issues

Customer Impact:
- Reduces frustration from locked accounts
- Minimizes support tickets for password resets
- Enables self-service account recovery
- Builds trust through secure, transparent process

Pain Points Addressed:
- Customers forget passwords regularly (major pain point)
- Waiting for support to reset password is frustrating
- Security questions are often forgotten
- Email delays cause anxiety about account security

Usability Notes:
- Use plain language, avoid technical jargon
- Provide estimated wait time for email
- Explain why link expires (security, not punishment)
- Offer alternative contact method prominently
- Mobile-friendly email and reset page essential

Accessibility:
- Reset page must be screen-reader compatible
- High contrast text for visibility
- Large, tappable buttons for mobile

Dependencies: REQ-DEV-020 (Email Service Integration)
""",

    "complex_feature": """
I have some concerns about this from a customer perspective.

This feature sounds complex and might be difficult for typical customers to understand. Let me ask some clarifying questions:

1. Will customers immediately understand what this feature does and why they need it?
2. How many steps will it take for a customer to use this feature?
3. Can we accomplish the same goal in a simpler way?
4. What happens if customers make mistakes while using this?
5. Will customers need training or extensive help documentation?

From a customer viewpoint, I'm concerned about:

Complexity: If this requires technical knowledge, most customers will struggle
Learning Curve: Customers want to accomplish tasks quickly, not learn new systems
Error Potential: Complex features often lead to user errors and frustration
Support Burden: This might generate many support tickets from confused customers

Customer Perspective Recommendations:
- Provide 3-4 simple presets instead of 50 configuration options
- Use wizards or guided workflows for complex tasks
- Include inline help and tooltips throughout
- Offer a "recommended" or "most popular" default option
- Make it possible to undo or reset to defaults easily
- Test with actual customers before building

Could we explore a simpler alternative that solves the core customer problem without the complexity?
""",
}

SALES_RESPONSES = {
    "enterprise_features": """
Let me evaluate this from a sales and marketing perspective.

REQ-MKT-001: Enterprise Security Features
Category: Competitive Differentiation
Priority: Must-have (for enterprise segment)

Value Proposition: "Enterprise-grade security that gives IT teams complete control and compliance peace of mind, positioning us as a credible enterprise solution."

Description: The system shall provide comprehensive enterprise security features including SSO, audit logging, and role-based access control to meet enterprise buyer requirements.

Target Audience:
- Enterprise IT decision makers
- Security and compliance officers
- Large organizations (500+ employees)

Competitive Positioning:
- Competitor A has basic SSO, no audit logs
- Competitor B has full enterprise security suite (our target)
- This brings us to competitive parity with market leaders
- Differentiates us from smaller competitors lacking enterprise features

Messaging Framework:
- Primary Message: "Enterprise security without enterprise complexity"
- Key Benefits:
  * Meet compliance requirements (SOC 2, GDPR, HIPAA)
  * Reduce security risks and IT burden
  * Scale confidently across large organizations
- Proof Points:
  * "Bank-grade encryption and access controls"
  * "Audit every action for complete visibility"
  * "Deploy in minutes with SSO integration"

Sales Enablement Needs:
- Security whitepaper for IT buyers
- Compliance checklist document
- Demo script focusing on admin portal
- Competitive battlecard vs. Competitor B
- ROI calculator showing reduced security incidents
- Case study from enterprise pilot customer

Go-to-Market Strategy:
- Launch at enterprise IT security conference
- PR campaign positioning as enterprise-ready
- Email campaign to enterprise segment
- Sales team training on enterprise buyer personas
- Partner with security consultants for referrals

Sales Impact:
- Unblocks 35% of enterprise deals currently lost to competitors
- Increases average deal size by $50K (enterprise premium pricing)
- Reduces enterprise sales cycle from 6 months to 4 months
- Improves win rate vs. Competitor B from 30% to 50%

Objection Handling:
- "Too expensive": ROI calculator shows cost of security breaches
- "Too complex": Emphasize "security without complexity" positioning
- "Not enough features": Highlight roadmap of upcoming capabilities

Dependencies: REQ-DEV-025 (SSO Integration), REQ-MKT-002 (Security Whitepaper)

Questions:
1. What is our pricing strategy for enterprise tier?
2. Do we have enterprise reference customers?
3. What's our competitive response if Competitor B undercuts us?
""",
}

SHAREHOLDER_RESPONSES = {
    "new_market_expansion": """
Let me evaluate this from a shareholder value perspective.

REQ-SH-001: International Market Expansion
Category: Market Expansion
Priority: Strategic

Business Case: Expand to European market to diversify revenue streams and capitalize on underserved market opportunity.

Financial Metrics:
- Total Addressable Market (Europe): $250M
- Expected Market Share (Year 1): 0.5% = $1.25M revenue
- Expected Market Share (Year 3): 3% = $7.5M revenue
- Implementation Cost: $800K (localization, infrastructure, legal)
- Ongoing Operational Cost: $200K/year
- Expected ROI: 300% over 3 years
- Payback Period: 18 months
- NPV (at 10% discount rate): $2.1M

Market Opportunity:
- European market growing 35% year-over-year
- Limited competition from US vendors due to GDPR complexity
- Strong demand from enterprise segment
- Premium pricing opportunity (20% higher than US)

Risk Assessment:
High Risks:
- Regulatory compliance (GDPR, data residency) - Mitigation: Legal counsel, compliance automation
- Currency fluctuation - Mitigation: Hedging strategy, EUR-denominated pricing
- Cultural/language barriers - Mitigation: Local partnerships, native speakers on team

Medium Risks:
- Longer sales cycles in Europe - Mitigation: Patient capital allocation, local sales team
- Competition from local vendors - Mitigation: Differentiation through superior technology

Low Risks:
- Technical infrastructure challenges - Mitigation: Proven cloud providers (AWS, Azure) available

Strategic Value:
- Reduces dependency on US market (currently 95% of revenue)
- Establishes foothold for further international expansion
- Attracts international investors
- Improves company valuation multiple (international = higher multiples)
- Provides competitive moat through global presence

Capital Allocation Analysis:
Alternative Uses of $800K:
1. US market expansion: Lower risk, but limited upside (market saturated)
2. Product development: Important, but not mutually exclusive
3. This investment: Higher risk, highest potential return

Recommendation: Proceed - risk-adjusted return superior to alternatives

Governance & Compliance:
- Quarterly board updates on European performance
- Key metrics: Revenue, customer acquisition cost, churn rate
- Decision point at 12 months: Continue, scale, or exit

Success Criteria:
- 100 paying customers by end of Year 1
- $1M ARR by end of Year 1
- Customer acquisition cost < $5K
- Net revenue retention > 90%
- Positive contribution margin by Month 18

Exit Strategy:
If underperforming at 12-month review:
- Wind down operations
- Pivot to partnership model
- Total sunk cost: $1M (acceptable loss within risk tolerance)

Dependencies: REQ-SH-002 (GDPR Compliance), REQ-SH-003 (European Infrastructure)

Board Questions to Address:
1. What is our go-to-market strategy in Europe?
2. Do we have local partnerships secured?
3. What is the competitive response risk?
4. How does this affect our path to profitability?
""",
}

STREAMING_RESPONSES = {
    "chunked_requirement": [
        "Based on ",
        "your requirement, ",
        "let me help ",
        "formalize it.\n\n",
        "REQ-DEV-001: ",
        "User Authentication\n",
        "Category: ",
        "Functional\n",
        "Priority: ",
        "Must-have\n\n",
        "Description: ",
        "The system shall ",
        "implement OAuth2 ",
        "authentication.\n",
    ],
}

ERROR_RESPONSES = {
    "vague_requirement": """
I need some clarification before I can formalize this requirement. Your statement is quite vague, and I want to make sure we capture the true need.

Questions:
1. What specific problem are you trying to solve?
2. Who are the users of this feature?
3. What does "fast" mean in measurable terms?
4. What does success look like?

Could you provide more details so we can create a testable, specific requirement?
""",

    "conflicting_requirement": """
I notice this requirement conflicts with REQ-DEV-003 (which prioritizes simplicity and fast load times).

Conflict Details:
- This requirement adds significant complexity and processing overhead
- REQ-DEV-003 requires < 100ms response time
- Adding this feature could increase response time to 300-500ms

Recommendations:
1. Prioritize one requirement over the other
2. Find a middle ground (e.g., make this feature optional/async)
3. Increase performance budget and adjust REQ-DEV-003

Let's discuss which approach aligns with our project goals.
""",
}
