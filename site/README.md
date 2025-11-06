# MARC Documentation

This directory contains the static HTML documentation for MARC, built with MkDocs.

## Viewing the Documentation

### Local Viewing

Simply open `index.html` in your web browser:

**On Linux/macOS:**
```bash
xdg-open index.html  # Linux
open index.html      # macOS
```

**On Windows:**
```bash
start index.html
```

**Or drag and drop** `index.html` into your browser.

### Serve Locally

For the best experience with search and navigation:

```bash
# From the project root
mkdocs serve
```

Then open http://localhost:8000 in your browser.

## Documentation Structure

```
site/
├── index.html                    # Home page
├── getting-started/
│   ├── installation.html         # Installation guide
│   ├── quickstart.html          # Quick start tutorial
│   └── configuration.html        # Configuration options
├── architecture/
│   ├── overview.html             # System architecture
│   ├── backend.html              # Backend design
│   ├── frontend.html             # Frontend design
│   └── multi-agent.html          # Multi-agent architecture (planned)
├── api/
│   ├── rest-api.html             # REST API reference
│   ├── backend.html              # Backend API docs
│   └── frontend.html             # Frontend component docs
├── guide/
│   ├── personas.html             # Using personas
│   ├── requirements.html         # Generating requirements
│   └── testing.html              # Testing guide
└── development/
    ├── contributing.html         # Contributing guidelines
    ├── testing.html              # Development testing
    └── standards.html            # Code standards
```

## Rebuilding Documentation

To rebuild the documentation from source:

```bash
# Install dependencies
pip install mkdocs mkdocs-material pymdown-extensions mkdocstrings mkdocstrings-python

# Build
mkdocs build

# The site/ directory will be regenerated
```

## Need Help?

- **Source Files**: Documentation source is in `docs/` directory
- **Configuration**: See `mkdocs.yml` for MkDocs settings
- **Issues**: Report documentation issues on GitHub

---

**MARC** - Multi-Agent Requirement Collaboration
