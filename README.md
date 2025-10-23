# Jira to SQLite

Downloads a Jira project to a SQLite database file using modern Python tools.

## Setup

This project uses `uv` for dependency management and virtual environments.

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd jira-to-sqlite
```

2. Create virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

Alternatively, use uv sync for a complete setup:
```bash
uv sync
```

## Configuration

Set the following environment variables:

```bash
export JIRA_SERVER_URL="https://your-company.atlassian.net"
export JIRA_USERNAME="your-email@company.com"
export JIRA_API_TOKEN="your-api-token"
export JIRA_PROJECT_KEY="PROJ"
```

### Getting a Jira API Token

1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a label and copy the generated token

## Usage

Run the script:
```bash
python main.py
```

Or if installed as a package:
```bash
uv run jira-to-sqlite
```

The script will:
1. Connect to your Jira instance
2. Fetch all issues from the specified project
3. Store them in a SQLite database (`jira_issues.db`)

## Database Schema

The SQLite database contains a `jira_issues` table with the following fields:

- `key`: Jira issue identifier (e.g., PROJ-123)
- `title`: Issue title/summary
- `description`: Issue description text
- `status`: Current issue status
- `assignee`: Person assigned to the issue
- `creator`: Person who created the issue
- `creation_time`: When the issue was created
- `fix_version`: Target fix version for the issue

## Development

Install development dependencies:
```bash
uv sync --group dev
```

Run tests:
```bash
uv run pytest
```

Format code:
```bash
uv run black .
```

Type checking:
```bash
uv run mypy main.py
```
