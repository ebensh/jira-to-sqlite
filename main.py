#!/usr/bin/env python3
"""
Jira to SQLite - Fetch Jira project issues and store them in SQLite database.
"""

import sqlite3
import os
import sys
import argparse
from datetime import datetime
from typing import Optional, List, Dict, Any
from jira import JIRA


class JiraToSQLite:
    def __init__(self, server_url: str, username: str, api_token: str, db_path: str = "jira_issues.db"):
        """
        Initialize the Jira to SQLite converter.
        
        Args:
            server_url: Jira server URL (e.g., 'https://company.atlassian.net')
            username: Jira username/email
            api_token: Jira API token
            db_path: Path to SQLite database file
        """
        self.server_url = server_url
        self.username = username
        self.api_token = api_token
        self.db_path = db_path
        self.jira = None
        self.conn = None

    def connect_to_jira(self) -> bool:
        """Connect to Jira using credentials."""
        try:
            # Use bearer token authentication for API tokens
            self.jira = JIRA(
                server=self.server_url,
                token_auth=self.api_token
            )
            print(f"Successfully connected to Jira: {self.server_url}")
            return True
        except Exception as e:
            print(f"Failed to connect to Jira: {e}")
            return False

    def create_database_schema(self):
        """Create SQLite database schema for storing Jira issues."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jira_issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                title TEXT,
                description TEXT,
                status TEXT,
                assignee TEXT,
                creator TEXT,
                creation_time TEXT,
                fix_version TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
        print(f"Database schema created at: {self.db_path}")

    def fetch_project_issues(self, project_key: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Fetch issues from a Jira project.
        
        Args:
            project_key: Jira project key (e.g., 'PROJ')
            limit: Maximum number of issues to fetch (None for all issues)
            
        Returns:
            List of issue dictionaries
        """
        if not self.jira:
            raise Exception("Not connected to Jira")
        
        issues_data = []
        start_at = 0
        max_results = 50
        
        if limit:
            print(f"Fetching up to {limit} recent issues from project: {project_key}")
        else:
            print(f"Fetching all issues from project: {project_key}")
        
        while True:
            try:
                # Adjust max_results if we're near the limit
                current_max_results = max_results
                if limit and (start_at + max_results > limit):
                    current_max_results = limit - start_at
                
                # Order by created date descending to get most recent issues first
                jql_query = f'project = {project_key} ORDER BY created DESC'
                
                issues = self.jira.search_issues(
                    jql_query,
                    startAt=start_at,
                    maxResults=current_max_results,
                    expand='renderedFields'
                )
                
                if not issues:
                    break
                
                for issue in issues:
                    issue_data = {
                        'key': issue.key,
                        'title': getattr(issue.fields, 'summary', ''),
                        'description': getattr(issue.fields, 'description', ''),
                        'status': getattr(issue.fields.status, 'name', '') if issue.fields.status else '',
                        'assignee': getattr(issue.fields.assignee, 'displayName', '') if issue.fields.assignee else '',
                        'creator': getattr(issue.fields.creator, 'displayName', '') if issue.fields.creator else '',
                        'creation_time': getattr(issue.fields, 'created', ''),
                        'fix_version': ', '.join([v.name for v in issue.fields.fixVersions]) if issue.fields.fixVersions else ''
                    }
                    issues_data.append(issue_data)
                
                print(f"Fetched {len(issues)} issues (total: {len(issues_data)})")
                
                # Break if we've reached the limit or no more issues
                if limit and len(issues_data) >= limit:
                    break
                if len(issues) < current_max_results:
                    break
                    
                start_at += current_max_results
                
            except Exception as e:
                print(f"Error fetching issues: {e}")
                break
        
        print(f"Total issues fetched: {len(issues_data)}")
        return issues_data

    def store_issues_to_db(self, issues: List[Dict[str, Any]]):
        """Store issues data to SQLite database."""
        if not self.conn:
            raise Exception("Database not connected")
        
        cursor = self.conn.cursor()
        
        for issue in issues:
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO jira_issues 
                    (key, title, description, status, assignee, creator, creation_time, fix_version)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    issue['key'],
                    issue['title'],
                    issue['description'],
                    issue['status'],
                    issue['assignee'],
                    issue['creator'],
                    issue['creation_time'],
                    issue['fix_version']
                ))
            except Exception as e:
                print(f"Error storing issue {issue['key']}: {e}")
        
        self.conn.commit()
        print(f"Stored {len(issues)} issues to database")

    def close_connections(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def run(self, project_key: str, limit: Optional[int] = None):
        """
        Main execution method to fetch Jira issues and store them in SQLite.
        
        Args:
            project_key: Jira project key to fetch issues from
            limit: Maximum number of issues to fetch (None for all issues)
        """
        try:
            if not self.connect_to_jira():
                return False
            
            self.create_database_schema()
            issues = self.fetch_project_issues(project_key, limit)
            
            if issues:
                self.store_issues_to_db(issues)
                print(f"Successfully processed {len(issues)} issues from project {project_key}")
            else:
                print(f"No issues found in project {project_key}")
            
            return True
            
        except Exception as e:
            print(f"Error during execution: {e}")
            return False
        finally:
            self.close_connections()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch Jira project issues and store them in SQLite database"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Maximum number of issues to fetch (fetches most recent issues first). Default: fetch all issues"
    )
    parser.add_argument(
        "--project",
        type=str,
        help="Jira project key to fetch (overrides JIRA_PROJECT_KEY env var)"
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default="jira_issues.db",
        help="Path to SQLite database file (default: jira_issues.db)"
    )
    
    args = parser.parse_args()
    
    # Get configuration from environment variables
    server_url = os.getenv('JIRA_SERVER_URL')
    username = os.getenv('JIRA_USERNAME')
    api_token = os.getenv('JIRA_API_TOKEN')
    project_key = args.project or os.getenv('JIRA_PROJECT_KEY')
    
    if not all([server_url, api_token, project_key]):
        print("Error: Missing required configuration:")
        print("- JIRA_SERVER_URL: Your Jira server URL (e.g., https://company.atlassian.net)")
        print("- JIRA_API_TOKEN: Your Jira API token (uses bearer token authentication)")
        print("- JIRA_PROJECT_KEY: The project key to fetch (e.g., PROJ) or use --project flag")
        print("Note: JIRA_USERNAME is optional and not used with token authentication")
        sys.exit(1)
    
    # Initialize and run the converter
    converter = JiraToSQLite(server_url, username, api_token, args.db_path)
    success = converter.run(project_key, args.limit)
    
    if success:
        print("Jira to SQLite conversion completed successfully!")
    else:
        print("Jira to SQLite conversion failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()