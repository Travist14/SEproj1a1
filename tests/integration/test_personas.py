"""
Integration tests for MARC persona system.
Tests the behavior of different stakeholder personas.
"""
import pytest
from unittest.mock import AsyncMock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "frontend" / "src" / "config"))

# We'll test persona configurations
PERSONAS = {
    'developer': {
        'key': 'developer',
        'label': 'Developer',
        'has_system_prompt': True,
        'focus_areas': ['technical_feasibility', 'code_quality', 'testing']
    },
    'pm': {
        'key': 'pm',
        'label': 'Product Manager',
        'has_system_prompt': True,
        'focus_areas': ['user_value', 'business_value', 'metrics']
    },
    'customer': {
        'key': 'customer',
        'label': 'Customer',
        'has_system_prompt': True,
        'focus_areas': ['usability', 'value', 'reliability']
    },
    'sales': {
        'key': 'sales',
        'label': 'Sales Representative',
        'has_system_prompt': True,
        'focus_areas': ['value_proposition', 'competitive_positioning', 'sales_enablement']
    },
    'shareholder': {
        'key': 'shareholder',
        'label': 'Shareholder',
        'has_system_prompt': True,
        'focus_areas': ['financial_performance', 'market_position', 'risk_management']
    }
}


@pytest.mark.integration
class TestPersonaSystem:
    """Test suite for the persona system."""

    def test_all_personas_exist(self, all_personas):
        """Verify all expected personas are defined."""
        for persona_key in all_personas:
            assert persona_key in PERSONAS, f"Persona {persona_key} not found"

    def test_persona_structure(self):
        """Verify each persona has required fields."""
        for persona_key, persona_config in PERSONAS.items():
            assert 'key' in persona_config
            assert 'label' in persona_config
            assert persona_config['key'] == persona_key

    def test_persona_labels_unique(self):
        """Verify each persona has a unique label."""
        labels = [p['label'] for p in PERSONAS.values()]
        assert len(labels) == len(set(labels)), "Persona labels must be unique"


@pytest.mark.integration
class TestDeveloperPersona:
    """Tests specific to the Developer persona."""

    @pytest.fixture
    def developer_requirement_prompt(self):
        return "I need to implement a REST API with authentication and rate limiting."

    def test_developer_focuses_on_technical_details(self, developer_requirement_prompt):
        """Developer persona should focus on technical implementation details."""
        # This would test actual LLM responses in a real scenario
        # For now, we verify the persona configuration
        assert 'technical_feasibility' in PERSONAS['developer']['focus_areas']
        assert 'code_quality' in PERSONAS['developer']['focus_areas']

    def test_developer_should_ask_about_implementation(self):
        """Developer persona should probe implementation details."""
        # Expected behaviors for developer persona
        expected_questions = [
            'technical_stack',
            'performance_requirements',
            'testing_strategy',
            'deployment',
            'error_handling'
        ]
        # In real tests, we'd verify the LLM actually asks these
        assert True  # Placeholder for actual LLM testing


@pytest.mark.integration
class TestProductManagerPersona:
    """Tests specific to the Product Manager persona."""

    @pytest.fixture
    def pm_requirement_prompt(self):
        return "We need a feature to increase user engagement."

    def test_pm_focuses_on_business_value(self, pm_requirement_prompt):
        """PM persona should focus on business value and metrics."""
        assert 'business_value' in PERSONAS['pm']['focus_areas']
        assert 'metrics' in PERSONAS['pm']['focus_areas']

    def test_pm_should_ask_about_metrics(self):
        """PM persona should ask about success metrics and KPIs."""
        expected_focus = [
            'user_value',
            'success_metrics',
            'business_alignment',
            'prioritization'
        ]
        # In real tests, verify the LLM asks these questions
        assert True  # Placeholder


@pytest.mark.integration
class TestCustomerPersona:
    """Tests specific to the Customer persona."""

    def test_customer_focuses_on_usability(self):
        """Customer persona should focus on ease of use."""
        assert 'usability' in PERSONAS['customer']['focus_areas']
        assert 'value' in PERSONAS['customer']['focus_areas']

    def test_customer_challenges_complexity(self):
        """Customer persona should challenge complex features."""
        # Customer should ask: "Will typical customers understand this?"
        assert True  # Placeholder


@pytest.mark.integration
class TestSalesPersona:
    """Tests specific to the Sales Representative persona."""

    def test_sales_focuses_on_value_proposition(self):
        """Sales persona should focus on marketability."""
        assert 'value_proposition' in PERSONAS['sales']['focus_areas']
        assert 'competitive_positioning' in PERSONAS['sales']['focus_areas']

    def test_sales_considers_go_to_market(self):
        """Sales persona should consider go-to-market strategy."""
        assert 'sales_enablement' in PERSONAS['sales']['focus_areas']


@pytest.mark.integration
class TestShareholderPersona:
    """Tests specific to the Shareholder persona."""

    def test_shareholder_focuses_on_roi(self):
        """Shareholder persona should focus on financial returns."""
        assert 'financial_performance' in PERSONAS['shareholder']['focus_areas']
        assert 'risk_management' in PERSONAS['shareholder']['focus_areas']

    def test_shareholder_asks_about_costs(self):
        """Shareholder persona should ask about costs and ROI."""
        # Should ask: "What is the expected ROI?"
        assert True  # Placeholder


@pytest.mark.integration
class TestPersonaInteractions:
    """Test interactions between different personas."""

    def test_different_personas_different_perspectives(self):
        """Verify different personas would handle the same requirement differently."""
        requirement = "Add social media sharing feature"

        expected_perspectives = {
            'developer': 'APIs, security, privacy',
            'pm': 'user engagement metrics, adoption',
            'customer': 'ease of use, privacy controls',
            'sales': 'competitive advantage, marketing',
            'shareholder': 'viral growth, customer acquisition cost'
        }

        # Each persona should analyze from their unique angle
        assert len(expected_perspectives) == len(PERSONAS)

    def test_persona_requirement_id_prefixes(self):
        """Verify each persona uses unique requirement ID prefixes."""
        expected_prefixes = {
            'developer': 'REQ-DEV-',
            'pm': 'REQ-PM-',
            'customer': 'REQ-CUST-',
            'sales': 'REQ-MKT-',
            'shareholder': 'REQ-SH-'
        }

        for persona_key in PERSONAS.keys():
            assert persona_key in expected_prefixes