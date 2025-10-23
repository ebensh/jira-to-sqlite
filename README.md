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
export JIRA_USERNAME="your-email@company.com"  # Not used with token auth, but kept for reference
export JIRA_API_TOKEN="your-api-token"
export JIRA_PROJECT_KEY="PROJ"
```

### Getting a Jira API Token

1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a label and copy the generated token
4. The script uses **bearer token authentication** (not basic auth) for better security

## Usage

### Basic Usage

Run the script to fetch all issues:
```bash
python main.py
```

### Command-Line Options

The script supports several command-line options:

```bash
python main.py --help
```

**Available options:**

- `--limit N`: Fetch only the N most recent issues (useful for testing)
- `--project PROJ`: Specify project key (overrides JIRA_PROJECT_KEY env var)  
- `--db-path PATH`: Specify database file path (default: jira_issues.db)

### Examples

Fetch only the 10 most recent issues for testing:
```bash
python main.py --limit 10
```

Fetch all issues from a specific project:
```bash
python main.py --project MYPROJ
```

Fetch 5 recent issues and save to custom database:
```bash
python main.py --limit 5 --db-path my_issues.db
```

Or if installed as a package:
```bash
uv run jira-to-sqlite --limit 10
```

The script will:
1. Connect to your Jira instance
2. Fetch issues from the specified project (ordered by creation date, newest first)
3. Store them in a SQLite database

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
