# Multi-Agent System Architecture

This document outlines the planned multi-agent collaboration system for MARC.

## Current Status

**Version 1.0**: Single-agent (persona) interactions
- Users select one persona at a time
- Each persona generates requirements independently
- No cross-persona collaboration

**Future Versions**: Multi-agent collaboration
- Orchestrator coordinates multiple personas
- Agents discuss and refine requirements
- Conflict detection and resolution
- Synthesized, unified requirements

## Planned Architecture

### Multi-Agent Workflow

```
User Input: "Build user authentication system"
                    ↓
        ┌───────────────────────┐
        │  Orchestrator Agent   │
        │  - Breaks down task   │
        │  - Assigns to agents  │
        │  - Synthesizes results│
        └───────────┬───────────┘
                    │
    ┌───────────────┴───────────────┐
    │                               │
    ↓         ↓         ↓          ↓         ↓
┌─────────┬────────┬─────────┬────────┬────────────┐
│Developer│Product │Customer │Sales   │Shareholder │
│         │Manager │         │        │            │
└────┬────┴───┬────┴────┬────┴───┬────┴──────┬─────┘
     │        │         │        │           │
     ↓        ↓         ↓        ↓           ↓
  REQ-DEV  REQ-PM   REQ-CUST  REQ-SAL   REQ-SH
     │        │         │        │           │
     └────────┴─────────┴────────┴───────────┘
                      │
                      ↓
        ┌─────────────────────────┐
        │   Conflict Detector     │
        │   - Find contradictions │
        │   - Identify overlaps   │
        │   - Prioritize conflicts│
        └────────────┬────────────┘
                     │
                     ↓
        ┌─────────────────────────┐
        │  Discussion Round       │
        │  - Agents negotiate     │
        │  - Refine requirements  │
        │  - Reach consensus      │
        └────────────┬────────────┘
                     │
                     ↓
        ┌─────────────────────────┐
        │  Requirement Synthesizer│
        │  - Merge compatible reqs│
        │  - Resolve conflicts    │
        │  - Generate final doc   │
        └────────────┬────────────┘
                     │
                     ↓
          IEEE 29148 Compliant
         Requirements Document
```

## Agent Types

### 1. Orchestrator Agent

**Role**: Coordinate multi-agent requirement generation

**Responsibilities**:
- Parse user input and understand intent
- Determine which personas should participate
- Assign specific aspects to each agent
- Collect and synthesize agent outputs
- Ensure completeness and consistency

**Example**:
```
User: "Build user authentication"

Orchestrator:
- Developer: Focus on implementation, security, tech stack
- Product Manager: Define user stories, acceptance criteria
- Customer: Address usability, simplicity concerns
- Shareholder: Analyze cost, ROI, strategic value
```

### 2. Specialist Agents (Personas)

**Current Personas**:
- Developer
- Product Manager
- Customer
- Sales
- Shareholder

**Capabilities**:
- Generate requirements from their perspective
- Critique other agents' requirements
- Propose refinements
- Negotiate conflicts

### 3. Conflict Detector

**Role**: Identify contradictions and overlaps

**Detection Types**:

**Direct Contradiction**:
```
Developer: "Use bcrypt for password hashing"
Product Manager: "Use MD5 for faster performance"
Conflict: Security vs Performance
```

**Implicit Conflict**:
```
Customer: "One-click login without password"
Developer: "Strong password requirements with 2FA"
Conflict: Convenience vs Security
```

**Priority Conflict**:
```
Product Manager: "Authentication is High priority"
Shareholder: "Authentication is Low priority, focus on features"
Conflict: Different priority assessments
```

### 4. Discussion Facilitator

**Role**: Enable agents to negotiate and refine

**Process**:
1. Present conflict to relevant agents
2. Allow each agent to explain rationale
3. Facilitate negotiation rounds
4. Reach consensus or escalate
5. Document resolution reasoning

**Example Discussion**:
```
Facilitator: "Developer suggests bcrypt, PM suggests MD5. Discuss."

Developer: "MD5 is cryptographically broken. Bcrypt is industry standard."

PM: "Understood. Security is more important than marginal performance gain."

Resolution: "Use bcrypt for password hashing"
```

### 5. Requirement Synthesizer

**Role**: Merge compatible requirements and resolve conflicts

**Synthesis Strategies**:

**Merging**:
Combine non-conflicting requirements:
```
Developer: "Hash passwords with bcrypt"
Customer: "Simple login form"
→ REQ-001: Simple login form with bcrypt password hashing
```

**Prioritization**:
Resolve by importance:
```
Developer: "Strong password requirements"
Customer: "Easy password entry"
→ REQ-002: Balanced password policy (8+ chars, but no special char requirement)
```

**Decomposition**:
Split conflicting requirements:
```
PM: "Social login OR email/password"
Customer: "Want both options"
→ REQ-003: Email/password authentication
→ REQ-004: Social login integration (OAuth)
```

## Collaboration Protocols

### Protocol 1: Sequential Generation

Agents generate requirements in sequence, building on previous outputs.

```python
orchestrator.prompt_agent("developer", user_input)
dev_req = developer.generate()

orchestrator.prompt_agent("product_manager", user_input, context=dev_req)
pm_req = product_manager.generate()

# Continue for all agents...
```

### Protocol 2: Parallel Generation

All agents generate independently, then synthesize.

```python
tasks = [
    developer.generate(user_input),
    product_manager.generate(user_input),
    customer.generate(user_input),
    sales.generate(user_input),
    shareholder.generate(user_input)
]

requirements = await asyncio.gather(*tasks)
synthesized = synthesizer.merge(requirements)
```

### Protocol 3: Iterative Refinement

Multiple rounds of generation and critique.

```python
round_1 = [agent.generate(user_input) for agent in agents]

for iteration in range(3):
    critiques = [
        agent.critique(other_requirements)
        for agent in agents
    ]

    refinements = [
        agent.refine(own_requirement, critiques)
        for agent in agents
    ]
```

## Data Models

### Requirement

```python
class Requirement:
    id: str  # REQ-{PERSONA}-{NUMBER}
    persona: str
    category: str  # Functional, Non-functional, etc.
    priority: str  # High, Medium, Low
    description: str
    rationale: str
    acceptance_criteria: List[str]
    dependencies: List[str]
    verification_method: str
    conflicts: List[str]  # IDs of conflicting requirements
```

### Conflict

```python
class Conflict:
    id: str
    type: str  # contradiction, priority, implicit
    req_ids: List[str]
    description: str
    severity: str  # critical, major, minor
    resolution: Optional[str]
    resolved_by: Optional[str]  # agent that resolved
```

### Discussion

```python
class Discussion:
    id: str
    conflict_id: str
    participants: List[str]  # agent personas
    messages: List[Message]
    resolution: Optional[str]
    consensus_reached: bool
```

## Implementation Roadmap

### Phase 1: Basic Multi-Agent (v1.1)

- [ ] Orchestrator that calls multiple personas
- [ ] Parallel requirement generation
- [ ] Simple concatenation of outputs
- [ ] UI to display all persona requirements side-by-side

### Phase 2: Conflict Detection (v1.2)

- [ ] Implement conflict detector
- [ ] Pattern matching for contradictions
- [ ] Highlight conflicts in UI
- [ ] Manual conflict resolution by user

### Phase 3: Agent Discussion (v1.3)

- [ ] Discussion protocol implementation
- [ ] Multi-turn agent conversations
- [ ] Negotiation strategies
- [ ] Automated conflict resolution (simple cases)

### Phase 4: Advanced Synthesis (v2.0)

- [ ] Intelligent requirement merging
- [ ] Priority-based resolution
- [ ] Requirement decomposition
- [ ] IEEE 29148 compliant unified document

### Phase 5: RAG Integration (v2.1)

- [ ] Requirement database
- [ ] Vector embeddings for similarity search
- [ ] Retrieve similar past requirements
- [ ] Learn from historical data

## Technical Challenges

### Challenge 1: Context Window Limits

**Problem**: Multiple agent outputs may exceed LLM context
**Solutions**:
- Summarization agents
- Hierarchical processing
- Streaming synthesis

### Challenge 2: Consistency

**Problem**: Agents may generate incompatible formats
**Solutions**:
- Strict prompt engineering
- Output validation
- Post-processing normalization

### Challenge 3: Infinite Discussion Loops

**Problem**: Agents may never reach consensus
**Solutions**:
- Maximum iteration limits
- Escalation to user
- Voting mechanisms

### Challenge 4: Latency

**Problem**: Multiple agents = longer wait times
**Solutions**:
- Parallel generation
- Caching common requirements
- Progressive disclosure (show results as they arrive)

## Next Steps

- [Overview](overview.md) - System architecture overview
- [Backend Architecture](backend.md) - Backend implementation
- [API Reference](../api/rest-api.md) - API documentation
