"""
Test scenarios for MARC system.
Defines realistic scenarios for testing multi-agent collaboration.
"""

# Scenario 1: Food Delivery App (from the MARC pamphlet)
FOOD_DELIVERY_SCENARIO = {
    "name": "Food Delivery Application",
    "description": "Building a food delivery app with multiple stakeholders",

    "stakeholder_inputs": {
        "customer": [
            "I want to track my order in real-time",
            "I need to be able to tip the driver",
            "The app should save my favorite restaurants",
            "I want to filter restaurants by cuisine type and dietary restrictions",
        ],

        "developer": [
            "Need to integrate with Google Maps API for delivery tracking",
            "Should we use WebSockets or polling for real-time updates?",
            "We need to handle payment processing securely",
            "Database schema must support restaurant menus with modifiers",
        ],

        "pm": [
            "Users should be able to schedule orders for later",
            "We need a rating system for restaurants and drivers",
            "The app must support promotions and discount codes",
            "Track metrics: order completion rate, average delivery time, customer satisfaction",
        ],

        "sales": [
            "Need a compelling value proposition for restaurants to join",
            "Should highlight lower commission than competitors",
            "Driver recruitment program essential for launch",
            "Marketing campaign around 'support local restaurants'",
        ],

        "shareholder": [
            "What's the unit economics per delivery?",
            "How quickly can we reach profitability in a new market?",
            "What's the customer acquisition cost?",
            "Need clear path to 1000 daily orders in 6 months",
        ],
    },

    "expected_conflicts": [
        {
            "conflict": "Feature complexity vs. Simple UX",
            "stakeholders": ["developer", "customer"],
            "description": "Developers want comprehensive features; customers want simple, fast app",
        },
        {
            "conflict": "Premium features vs. Cost control",
            "stakeholders": ["pm", "shareholder"],
            "description": "PM wants feature-rich app; shareholders want minimal costs",
        },
        {
            "conflict": "Fast launch vs. Quality",
            "stakeholders": ["sales", "developer"],
            "description": "Sales wants quick market entry; developers want robust, tested system",
        },
    ],

    "sample_synthesized_requirements": [
        {
            "id": "REQ-SYNTH-001",
            "title": "Real-time Order Tracking",
            "description": "The system shall provide real-time order tracking with <100ms update latency",
            "stakeholder_perspectives": {
                "customer": "Easy to see where my order is",
                "developer": "Implement with WebSockets for efficiency",
                "pm": "Track usage metrics to measure feature value",
                "shareholder": "Reduces support costs by 30%",
            },
            "trade_offs": "WebSocket implementation increases initial complexity but reduces long-term infrastructure costs",
        },
    ],
}

# Scenario 2: Healthcare Patient Portal
HEALTHCARE_PORTAL_SCENARIO = {
    "name": "Healthcare Patient Portal",
    "description": "Patient portal for viewing medical records and scheduling appointments",

    "stakeholder_inputs": {
        "customer": [
            "I want to see my test results as soon as they're available",
            "Scheduling appointments should be easy",
            "I need to be able to message my doctor",
            "The app must protect my privacy",
        ],

        "developer": [
            "Must comply with HIPAA regulations",
            "Need end-to-end encryption for messages",
            "Integration with existing EHR systems (Epic, Cerner)",
            "Require multi-factor authentication for security",
        ],

        "pm": [
            "Reduce no-show rates through automated reminders",
            "Enable telehealth appointments",
            "Track: appointment completion rate, patient engagement, portal adoption",
            "Support multiple languages for diverse patient population",
        ],

        "sales": [
            "Differentiate through superior UX compared to legacy systems",
            "Emphasize HIPAA compliance and security",
            "Target mid-size healthcare providers (50-500 doctors)",
            "Case studies showing reduced administrative burden",
        ],

        "shareholder": [
            "What's the Total Addressable Market?",
            "How do we compare to Epic's MyChart?",
            "What's the expected contract value per healthcare system?",
            "Path to $10M ARR in 24 months?",
        ],
    },

    "expected_conflicts": [
        {
            "conflict": "Security vs. Usability",
            "stakeholders": ["developer", "customer"],
            "description": "Security requirements (MFA, encryption) may complicate user experience",
        },
        {
            "conflict": "Feature scope vs. Compliance timeline",
            "stakeholders": ["pm", "developer"],
            "description": "PM wants rich features; developers need time for HIPAA compliance",
        },
    ],
}

# Scenario 3: E-Commerce Platform
ECOMMERCE_SCENARIO = {
    "name": "E-Commerce Platform",
    "description": "Building a new e-commerce platform for small businesses",

    "stakeholder_inputs": {
        "customer": [
            "I want to find products easily with good search",
            "Checkout should be fast and support Apple Pay / Google Pay",
            "I need order tracking and easy returns",
            "Product recommendations based on my browsing history",
        ],

        "developer": [
            "Need scalable architecture for Black Friday traffic spikes",
            "Implement search using Elasticsearch",
            "Payment processing via Stripe for PCI compliance",
            "CDN for product images to reduce load times",
        ],

        "pm": [
            "Abandoned cart recovery email campaign",
            "A/B testing framework for conversion optimization",
            "Loyalty program to increase repeat purchases",
            "Track: conversion rate, average order value, cart abandonment rate",
        ],

        "sales": [
            "Easy onboarding for merchant customers",
            "Pricing model: % of transaction vs. monthly subscription",
            "Competitive with Shopify but better customization",
            "Target: Shopify users wanting more control",
        ],

        "shareholder": [
            "What's our take rate and how does it compare to Shopify?",
            "Customer lifetime value vs. acquisition cost",
            "Path to 10,000 merchant customers",
            "When do we reach profitability?",
        ],
    },
}

# Test case for requirement synthesis
REQUIREMENT_SYNTHESIS_TEST_CASES = [
    {
        "name": "Authentication Requirement",
        "inputs": {
            "developer": "Implement OAuth2 with Google and GitHub providers",
            "customer": "I just want to log in easily without remembering another password",
            "pm": "Social login increases conversion by 20% according to industry benchmarks",
            "shareholder": "Keep implementation costs under $50K",
        },
        "expected_synthesis": {
            "core_requirement": "Social authentication with OAuth2",
            "balances": [
                "Easy login (customer) + Secure implementation (developer)",
                "Industry best practices (PM) + Cost control (shareholder)",
            ],
            "trade_offs": "OAuth2 is more complex initially but reduces long-term support costs",
        },
    },

    {
        "name": "Performance Requirement",
        "inputs": {
            "developer": "Need caching layer (Redis) to meet performance targets",
            "customer": "App should load instantly, no waiting",
            "pm": "Page load time under 1 second improves conversion by 7%",
            "shareholder": "What's the cost of Redis infrastructure?",
        },
        "expected_synthesis": {
            "core_requirement": "Page load time under 1 second",
            "implementation": "Redis caching with cost monitoring",
            "success_metrics": "Load time, conversion rate, infrastructure cost",
        },
    },
]
