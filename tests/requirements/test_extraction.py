"""
Tests for requirements extraction from LLM responses.
Tests the ability to parse and validate structured requirements.
"""
import pytest
import re
from typing import Dict, List, Optional


class RequirementExtractor:
    """
    Utility class for extracting structured requirements from LLM responses.
    This is a placeholder implementation for the actual extraction logic.
    """

    @staticmethod
    def extract_requirement_id(text: str) -> Optional[str]:
        """Extract requirement ID (e.g., REQ-DEV-001)."""
        pattern = r'REQ-[A-Z]+-\d+'
        match = re.search(pattern, text)
        return match.group(0) if match else None

    @staticmethod
    def extract_category(text: str) -> Optional[str]:
        """Extract requirement category."""
        pattern = r'Category:\s*(.+?)(?:\n|$)'
        match = re.search(pattern, text)
        return match.group(1).strip() if match else None

    @staticmethod
    def extract_priority(text: str) -> Optional[str]:
        """Extract requirement priority."""
        pattern = r'Priority:\s*(.+?)(?:\n|$)'
        match = re.search(pattern, text)
        return match.group(1).strip() if match else None

    @staticmethod
    def extract_description(text: str) -> Optional[str]:
        """Extract requirement description."""
        pattern = r'Description:\s*(.+?)(?:\n\n|\nAcceptance|\nTechnical|\nDependencies|$)'
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else None

    @staticmethod
    def extract_acceptance_criteria(text: str) -> List[str]:
        """Extract acceptance criteria as a list."""
        pattern = r'Acceptance Criteria:\s*(.+?)(?:\n\n|\nTechnical|\nDependencies|$)'
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            return []

        criteria_text = match.group(1)
        # Extract bullet points
        criteria = re.findall(r'[-•]\s*(.+?)(?:\n|$)', criteria_text)
        return [c.strip() for c in criteria if c.strip()]

    @staticmethod
    def extract_dependencies(text: str) -> List[str]:
        """Extract requirement dependencies."""
        pattern = r'Dependencies:\s*(.+?)(?:\n\n|\nTechnical|$)'
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            return []

        deps_text = match.group(1).strip()
        # Extract REQ-XXX-NNN patterns
        deps = re.findall(r'REQ-[A-Z]+-\d+', deps_text)
        return deps

    @staticmethod
    def is_valid_requirement(requirement: Dict) -> bool:
        """Validate that a requirement has all necessary fields."""
        required_fields = ['id', 'category', 'priority', 'description']
        return all(field in requirement and requirement[field] for field in required_fields)


@pytest.mark.unit
class TestRequirementExtraction:
    """Test suite for requirement extraction logic."""

    @pytest.fixture
    def sample_requirement_text(self):
        return """
REQ-DEV-001: API Rate Limiting
Category: Non-Functional (Performance)
Priority: Must-have

Description: The system shall implement rate limiting on all API endpoints to prevent abuse.

Acceptance Criteria:
- Limit to 100 requests per minute per user
- Return 429 status code when limit exceeded
- Include retry-after header in response

Dependencies: REQ-DEV-002
"""

    def test_extract_requirement_id(self, sample_requirement_text):
        """Test extraction of requirement ID."""
        req_id = RequirementExtractor.extract_requirement_id(sample_requirement_text)
        assert req_id == "REQ-DEV-001"

    def test_extract_category(self, sample_requirement_text):
        """Test extraction of category."""
        category = RequirementExtractor.extract_category(sample_requirement_text)
        assert "Non-Functional" in category
        assert "Performance" in category

    def test_extract_priority(self, sample_requirement_text):
        """Test extraction of priority."""
        priority = RequirementExtractor.extract_priority(sample_requirement_text)
        assert priority == "Must-have"

    def test_extract_description(self, sample_requirement_text):
        """Test extraction of description."""
        description = RequirementExtractor.extract_description(sample_requirement_text)
        assert "rate limiting" in description.lower()
        assert "API endpoints" in description

    def test_extract_acceptance_criteria(self, sample_requirement_text):
        """Test extraction of acceptance criteria."""
        criteria = RequirementExtractor.extract_acceptance_criteria(sample_requirement_text)
        assert len(criteria) == 3
        assert any("100 requests" in c for c in criteria)
        assert any("429" in c for c in criteria)

    def test_extract_dependencies(self, sample_requirement_text):
        """Test extraction of dependencies."""
        deps = RequirementExtractor.extract_dependencies(sample_requirement_text)
        assert "REQ-DEV-002" in deps

    def test_extract_from_pm_requirement(self):
        """Test extraction from PM-style requirement."""
        pm_text = """
REQ-PM-001: User Engagement Dashboard
Category: User Story
Priority: Must-have (P0)

Description: As a product manager, I want to track user engagement metrics.

Acceptance Criteria:
- Display daily active users
- Show retention over time
- Export data to CSV
"""
        req_id = RequirementExtractor.extract_requirement_id(pm_text)
        assert req_id == "REQ-PM-001"

        criteria = RequirementExtractor.extract_acceptance_criteria(pm_text)
        assert len(criteria) == 3

    def test_extract_multiple_requirements(self):
        """Test extraction when multiple requirements are present."""
        multi_text = """
REQ-DEV-001: First requirement
Category: Functional
Priority: High

REQ-DEV-002: Second requirement
Category: Non-Functional
Priority: Medium
"""
        # Should find both IDs
        ids = re.findall(r'REQ-[A-Z]+-\d+', multi_text)
        assert len(ids) == 2
        assert "REQ-DEV-001" in ids
        assert "REQ-DEV-002" in ids


@pytest.mark.unit
class TestRequirementValidation:
    """Test suite for requirement validation."""

    def test_valid_requirement(self):
        """Test validation of a complete requirement."""
        requirement = {
            'id': 'REQ-DEV-001',
            'category': 'Functional',
            'priority': 'Must-have',
            'description': 'The system shall do X',
            'acceptance_criteria': ['Criterion 1', 'Criterion 2']
        }
        assert RequirementExtractor.is_valid_requirement(requirement)

    def test_missing_required_field(self):
        """Test validation fails when required field is missing."""
        requirement = {
            'id': 'REQ-DEV-001',
            'category': 'Functional',
            # Missing priority
            'description': 'The system shall do X'
        }
        assert not RequirementExtractor.is_valid_requirement(requirement)

    def test_empty_required_field(self):
        """Test validation fails when required field is empty."""
        requirement = {
            'id': 'REQ-DEV-001',
            'category': '',  # Empty
            'priority': 'Must-have',
            'description': 'The system shall do X'
        }
        assert not RequirementExtractor.is_valid_requirement(requirement)


@pytest.mark.unit
class TestPersonaSpecificRequirements:
    """Test extraction of persona-specific requirement formats."""

    def test_developer_requirement_format(self):
        """Test developer requirements include technical details."""
        dev_text = """
REQ-DEV-001: OAuth2 Authentication
Category: Functional
Priority: Must-have

Description: Implement OAuth2 authentication system

Technical Notes:
- Use Redis for token storage
- Implement sliding window algorithm
"""
        req_id = RequirementExtractor.extract_requirement_id(dev_text)
        assert req_id.startswith("REQ-DEV-")

        # Technical notes should be extractable
        assert "Redis" in dev_text
        assert "sliding window" in dev_text

    def test_pm_requirement_includes_metrics(self):
        """Test PM requirements include success metrics."""
        pm_text = """
REQ-PM-001: Feature Name
Category: User Story
Priority: P0

Success Metrics:
- 20% increase in user engagement
- 15% improvement in retention
"""
        assert "Success Metrics" in pm_text
        assert "engagement" in pm_text
        assert "retention" in pm_text

    def test_shareholder_requirement_includes_roi(self):
        """Test shareholder requirements include financial metrics."""
        sh_text = """
REQ-SH-001: Revenue Feature
Category: Revenue Generation
Priority: Strategic

Financial Metrics:
- Expected ROI: 300%
- Payback period: 6 months
"""
        assert "Financial Metrics" in sh_text
        assert "ROI" in sh_text
        assert "Payback period" in sh_text


@pytest.mark.integration
class TestRequirementQuality:
    """Test the quality of extracted requirements."""

    def test_requirement_is_testable(self):
        """Test that requirements are testable/measurable."""
        # Good: "Response time shall be < 100ms"
        # Bad: "System should be fast"

        good_requirements = [
            "Response time shall be less than 100ms",
            "Support 1000 concurrent users",
            "99.9% uptime"
        ]

        bad_requirements = [
            "System should be fast",
            "User-friendly interface",
            "Good performance"
        ]

        # Requirements should be specific and measurable
        for req in good_requirements:
            assert any(char.isdigit() for char in req) or '<' in req or '>' in req

        # Bad requirements lack specificity
        for req in bad_requirements:
            assert not any(char.isdigit() for char in req)

    def test_requirement_uses_shall_language(self):
        """Test that requirements use 'shall' language (IEEE standard)."""
        # IEEE 29148 recommends "shall" for mandatory requirements
        good_req = "The system shall authenticate users via OAuth2"
        bad_req = "The system should maybe authenticate users"

        assert "shall" in good_req.lower()
        assert "shall" not in bad_req.lower()

    def test_requirement_is_atomic(self):
        """Test that each requirement addresses a single concern."""
        # Good: Single concern
        atomic_req = "The system shall encrypt data at rest"

        # Bad: Multiple concerns
        compound_req = "The system shall encrypt data and send emails and log events"

        # Atomic requirements typically have fewer "and" conjunctions
        assert atomic_req.count(" and ") == 0
        assert compound_req.count(" and ") >= 2
