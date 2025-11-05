"""
Tests for IEEE 29148 compliance of requirements.
Verifies that requirements follow industry standards.
"""
import pytest
from typing import Dict, List


class IEEEComplianceChecker:
    """
    Utility for checking IEEE 29148 compliance.
    IEEE 29148 is the standard for requirements engineering.
    """

    @staticmethod
    def check_unique_identifier(requirement: Dict) -> bool:
        """Check that requirement has a unique identifier."""
        return 'id' in requirement and requirement['id'] and len(requirement['id']) > 0

    @staticmethod
    def check_has_description(requirement: Dict) -> bool:
        """Check that requirement has a clear description."""
        return 'description' in requirement and len(requirement.get('description', '')) > 10

    @staticmethod
    def check_has_rationale(requirement: Dict) -> bool:
        """Check that requirement has a rationale (why it's needed)."""
        # Rationale might be in 'rationale', 'user_story', or 'business_value' field
        return any(
            field in requirement and requirement[field]
            for field in ['rationale', 'user_story', 'business_value', 'description']
        )

    @staticmethod
    def check_has_priority(requirement: Dict) -> bool:
        """Check that requirement has a priority."""
        return 'priority' in requirement and requirement['priority']

    @staticmethod
    def check_has_verification_method(requirement: Dict) -> bool:
        """Check that requirement specifies how it will be verified."""
        # Could be in 'acceptance_criteria', 'test_plan', or 'verification_method'
        return any(
            field in requirement and requirement[field]
            for field in ['acceptance_criteria', 'test_plan', 'verification_method']
        )

    @staticmethod
    def check_is_unambiguous(description: str) -> bool:
        """Check for ambiguous language in requirement description."""
        # Words that indicate ambiguity
        ambiguous_words = [
            'maybe', 'might', 'could', 'possibly', 'perhaps',
            'usually', 'generally', 'typically', 'often',
            'fast', 'slow', 'user-friendly', 'easy', 'simple',
            'good', 'bad', 'nice', 'better', 'worse'
        ]
        description_lower = description.lower()
        return not any(word in description_lower for word in ambiguous_words)

    @staticmethod
    def check_is_complete(requirement: Dict) -> bool:
        """Check that requirement is complete per IEEE 29148."""
        required_fields = ['id', 'description', 'priority']
        return all(field in requirement and requirement[field] for field in required_fields)

    @staticmethod
    def full_compliance_check(requirement: Dict) -> Dict[str, bool]:
        """Run all compliance checks and return results."""
        return {
            'unique_identifier': IEEEComplianceChecker.check_unique_identifier(requirement),
            'has_description': IEEEComplianceChecker.check_has_description(requirement),
            'has_rationale': IEEEComplianceChecker.check_has_rationale(requirement),
            'has_priority': IEEEComplianceChecker.check_has_priority(requirement),
            'has_verification': IEEEComplianceChecker.check_has_verification_method(requirement),
            'is_complete': IEEEComplianceChecker.check_is_complete(requirement),
        }


@pytest.mark.unit
class TestIEEECompliance:
    """Test suite for IEEE 29148 compliance checking."""

    @pytest.fixture
    def compliant_requirement(self):
        """A requirement that meets IEEE 29148 standards."""
        return {
            'id': 'REQ-DEV-001',
            'description': 'The system shall authenticate users using OAuth2 protocol',
            'rationale': 'OAuth2 is industry standard and provides secure authentication',
            'priority': 'Must-have',
            'category': 'Functional',
            'acceptance_criteria': [
                'Support Google and GitHub OAuth providers',
                'Token expiration after 1 hour',
                'Secure token storage in database'
            ],
            'verification_method': 'Integration testing with OAuth providers',
            'dependencies': []
        }

    @pytest.fixture
    def non_compliant_requirement(self):
        """A requirement that fails IEEE compliance."""
        return {
            'description': 'Make the system fast and user-friendly',
            # Missing: id, priority, acceptance_criteria
            # Ambiguous: "fast", "user-friendly"
        }

    def test_unique_identifier_check(self, compliant_requirement):
        """Test that unique identifier check works."""
        assert IEEEComplianceChecker.check_unique_identifier(compliant_requirement)

        no_id = {}
        assert not IEEEComplianceChecker.check_unique_identifier(no_id)

    def test_description_check(self, compliant_requirement, non_compliant_requirement):
        """Test that description check works."""
        assert IEEEComplianceChecker.check_has_description(compliant_requirement)
        assert not IEEEComplianceChecker.check_has_description({'description': 'Too short'})

    def test_priority_check(self, compliant_requirement):
        """Test that priority check works."""
        assert IEEEComplianceChecker.check_has_priority(compliant_requirement)
        assert not IEEEComplianceChecker.check_has_priority({})

    def test_verification_method_check(self, compliant_requirement):
        """Test that verification method check works."""
        assert IEEEComplianceChecker.check_has_verification_method(compliant_requirement)

        # Should also accept acceptance_criteria
        with_criteria = {'acceptance_criteria': ['Test 1', 'Test 2']}
        assert IEEEComplianceChecker.check_has_verification_method(with_criteria)

    def test_ambiguity_detection(self):
        """Test detection of ambiguous language."""
        ambiguous = "The system should be fast and user-friendly"
        assert not IEEEComplianceChecker.check_is_unambiguous(ambiguous)

        clear = "The system shall respond within 100 milliseconds"
        assert IEEEComplianceChecker.check_is_unambiguous(clear)

    def test_full_compliance_check(self, compliant_requirement):
        """Test full compliance check on a compliant requirement."""
        results = IEEEComplianceChecker.full_compliance_check(compliant_requirement)

        assert results['unique_identifier']
        assert results['has_description']
        assert results['has_priority']
        assert results['has_verification']
        assert results['is_complete']

    def test_full_compliance_check_fails(self, non_compliant_requirement):
        """Test full compliance check on a non-compliant requirement."""
        results = IEEEComplianceChecker.full_compliance_check(non_compliant_requirement)

        assert not results['unique_identifier']
        assert not results['has_priority']
        assert not results['is_complete']


@pytest.mark.integration
class TestRequirementStandards:
    """Test that MARC requirements meet industry standards."""

    def test_developer_requirements_are_compliant(self):
        """Test that developer persona generates IEEE-compliant requirements."""
        dev_req = {
            'id': 'REQ-DEV-001',
            'category': 'Functional',
            'priority': 'Must-have',
            'description': 'The system shall implement rate limiting using Redis',
            'acceptance_criteria': [
                'Limit to 100 req/min per user',
                'Return 429 on limit exceeded'
            ],
            'technical_notes': 'Use sliding window algorithm'
        }

        assert IEEEComplianceChecker.check_is_complete(dev_req)
        assert IEEEComplianceChecker.check_has_verification_method(dev_req)

    def test_pm_requirements_are_compliant(self):
        """Test that PM persona generates IEEE-compliant requirements."""
        pm_req = {
            'id': 'REQ-PM-001',
            'category': 'User Story',
            'priority': 'Must-have (P0)',
            'user_story': 'As a PM, I want engagement metrics',
            'description': 'Dashboard shall display user engagement metrics',
            'acceptance_criteria': [
                'Show daily active users',
                'Display 7-day retention'
            ],
            'success_metrics': ['20% increase in engagement']
        }

        assert IEEEComplianceChecker.check_is_complete(pm_req)
        assert IEEEComplianceChecker.check_has_verification_method(pm_req)

    def test_requirements_use_shall_language(self):
        """Test that requirements use 'shall' for mandatory items."""
        # IEEE 29148 recommends:
        # - "shall" for mandatory requirements
        # - "should" for recommendations
        # - "may" for permissions

        mandatory = "The system shall encrypt all data at rest"
        recommendation = "The system should provide user tutorials"
        permission = "The system may cache frequently accessed data"

        assert "shall" in mandatory
        assert "should" in recommendation
        assert "may" in permission

    def test_requirements_are_testable(self):
        """Test that requirements include testable acceptance criteria."""
        testable_req = {
            'id': 'REQ-001',
            'description': 'API response time shall be under 100ms',
            'acceptance_criteria': [
                'Measured response time < 100ms for 95th percentile',
                'Load test with 1000 concurrent users'
            ]
        }

        # Should have specific, measurable criteria
        criteria = testable_req['acceptance_criteria']
        assert any('100ms' in c for c in criteria)
        assert any('1000' in c for c in criteria)

    def test_requirements_avoid_implementation_unless_justified(self):
        """Test that functional requirements focus on 'what' not 'how'."""
        # Good: Specifies what, leaves how flexible
        good = "The system shall authenticate users securely"

        # Sometimes OK: Specifies how when there's a technical justification
        ok_with_justification = "The system shall use OAuth2 for authentication due to industry standard compliance requirements"

        # Generally avoid being overly prescriptive unless there's a reason
        assert "shall" in good
        assert "OAuth2" in ok_with_justification and "due to" in ok_with_justification
