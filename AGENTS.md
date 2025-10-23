# Jira to SQLite Project

## Project Overview

This project uses modern Python development tools to fetch Jira project data and store it in a SQLite database.

## Goals

- Use modern Python development tools like `uv` for dependency management
- Utilize the Jira library to interact with the Jira API
- Fetch a single Jira project's issues
- Store relevant issue information in a SQLite database

## Data Fields to Store

The following key information should be extracted and stored for each issue:

- **Key (ID)**: Jira issue identifier (e.g., PROJ-123)
- **Title**: Issue title/summary
- **Description**: Issue description/summary text
- **Status**: Current issue status
- **Assignee**: Person assigned to the issue
- **Creator**: Person who created the issue
- **Creation Time**: When the issue was created
- **Fix Version**: Target fix version for the issue

## Technical Stack

- **Python**: Core language
- **uv**: Modern Python package and project manager
- **Jira Library**: Python library for Jira API interactions
- **SQLite**: Local database for data storage