# Quick Start Guide

Get MARC up and running in under 5 minutes and generate your first requirement!

## Prerequisites

Make sure you've completed the [Installation Guide](installation.md) before proceeding.

## Starting MARC

### Step 1: Start the Backend

Open a terminal and run:

```bash
cd src/backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

You should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

The backend is now available at `http://localhost:8001`

### Step 2: Start the Frontend

Open a **new terminal** and run:

```bash
cd src/frontend
npm run dev
```

You should see:
```
  VITE v5.1.0  ready in 423 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

The frontend is now available at `http://localhost:5173`

## Generating Your First Requirement

### Step 3: Select a Persona

1. Open your browser to `http://localhost:5173`
2. You'll see the MARC login screen with 5 persona options:
   - **Developer** - Technical perspective
   - **Product Manager** - Business value perspective
   - **Customer** - User experience perspective
   - **Sales** - Value proposition perspective
   - **Shareholder** - Financial perspective

3. Click on **"Developer"** to start with a technical perspective

### Step 4: Enter a Requirement Prompt

In the message input box at the bottom, enter a requirement description:

```
I need user authentication with email and password
```

Press Enter or click the **Generate** button.

### Step 5: Watch the AI Generate Requirements

You'll see the AI generate a structured requirement in real-time:

```
REQ-DEV-001: User Authentication System

Category: Security
Priority: High

Description:
Implement secure user authentication using email and password credentials
with industry-standard encryption and session management.

Rationale:
User authentication is fundamental for securing user data and providing
personalized experiences. Email/password authentication is widely understood
and accepted by users.

Acceptance Criteria:
- Users can register with valid email and strong password
- Passwords are hashed using bcrypt with minimum 10 rounds
- Failed login attempts are rate-limited (max 5 per 15 minutes)
- Session tokens expire after 24 hours of inactivity
- Password reset functionality via email verification

Dependencies:
- Email service (SMTP or SendGrid)
- Database with user table
- JWT token generation library

Verification Method:
- Unit tests for authentication logic
- Integration tests for registration/login flows
- Security audit for password hashing and session management
- Manual testing of rate limiting
```

### Step 6: Try Different Personas

Click **"Switch Role"** in the top-right corner and try the same prompt with different personas:

**Product Manager:**
```
I need user authentication with email and password
```

Will generate requirements focused on:
- User value and business metrics
- Success criteria (e.g., 95% successful login rate)
- User stories and acceptance criteria

**Customer:**
```
I need user authentication with email and password
```

Will generate requirements focused on:
- Usability and simplicity
- Pain points and user concerns
- Minimal friction in the login process

## Example Prompts to Try

### E-commerce Features
```
Build a shopping cart with add to cart and checkout functionality
```

### Healthcare Systems
```
Create a patient appointment scheduling system
```

### Financial Applications
```
Implement real-time stock price monitoring and alerts
```

### Mobile Features
```
Add push notifications for order status updates
```

## Understanding the Output

Each generated requirement follows IEEE 29148 standards with these sections:

- **REQ-ID**: Unique identifier (format: REQ-{PERSONA}-{NUMBER})
- **Category**: Type of requirement (Functional, Non-functional, Performance, Security)
- **Priority**: Importance level (High, Medium, Low)
- **Description**: Clear, unambiguous requirement statement
- **Rationale**: Why this requirement is needed
- **Acceptance Criteria**: Testable conditions for completion
- **Dependencies**: Related systems or requirements
- **Verification Method**: How to test/verify the requirement

## Next Steps

Now that you've generated your first requirement, explore:

- **[Using Personas](../guide/personas.md)** - Learn how to leverage different stakeholder perspectives
- **[Generating Requirements](../guide/requirements.md)** - Best practices for prompting
- **[API Reference](../api/rest-api.md)** - Integrate MARC into your workflow
- **[Architecture](../architecture/overview.md)** - Understand how MARC works under the hood

## Tips for Better Requirements

1. **Be Specific**: Instead of "user management", try "user registration with email verification"
2. **Add Context**: Mention the domain (e-commerce, healthcare, finance)
3. **Include Constraints**: Specify performance needs, security requirements, or scale
4. **Use Multiple Personas**: Generate requirements from all 5 perspectives for comprehensive coverage

## Troubleshooting

### Backend Not Responding
```bash
# Check if backend is running
curl http://localhost:8001/health

# Expected output:
{"status":"ok","model":"Qwen/Qwen3-4B","engine_ready":true}
```

### Frontend Can't Connect
Check that:
1. Backend is running on port 8001
2. No firewall is blocking connections
3. CORS settings allow localhost:5173

### Generation Takes Too Long
- First generation may take 30-60 seconds while the model loads
- Subsequent generations should be faster (2-5 seconds)
- Consider using a GPU for faster inference

## Getting Help

- Check the [Testing Guide](../guide/testing.md) for debugging
- Review [Configuration](configuration.md) for customization options
- See [Common Issues](installation.md#common-installation-issues) in the installation guide
