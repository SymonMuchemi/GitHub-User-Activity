#!/usr/bin/python3
# Get user github activity data
import sys
import json
from urllib import request, error


username = sys.argv[1]
event_url = f"https://api.github.com/users/{username}/events"

if username is None:
    print("Enter a valid username")

def get_user_activity(url: str) -> dict:
    """get user data via http

    Args:
        url (str): url path to user data

    Returns:
        dict: response body
    """
    try:
        with request.urlopen(url) as response:
            data = response.read()
            json_data = json.loads(data.decode('utf-8'))
            return json_data
    except error.HTTPError as e:
        print(f"HTTP Error code: {e.code}")
    except error.URLError as e:
        print(f"HTTP Error message: {e.reason}")

def get_repo_name(url: str) -> str:
    """gets the name of the repository from the url

    Args:
        url (str): github repository url

    Returns:
        str: name of github repo
    """
    return url[29:]

def process_data(data: dict) -> None:
    """triggers response data processing

    Args:
        data (dict): responsse data
    """
    for item in data:
        print_event_data(item)

def print_event_data(data: dict) -> None:
    """prints the type of event and repo name

    Args:
        data (dict): event data
    """
    event_type = data.get('type')
    repo_url = data.get('repo').get('url')
    repo_name = get_repo_name(repo_url)
    commits = data.get('payload').get('commits')
    len_of_commits = len(commits) if commits else 0

    if event_type == 'PushEvent' and len_of_commits > 0:
        print(f'Pushed {len_of_commits} commits to {repo_name}')

    elif event_type == 'PullRequestEvent':
        print(f'Created a Pull Request on {repo_name}')

    elif event_type == 'IssueCommentEvent':
        print(f'Comment on an issue in {repo_name}')

    elif event_type == 'IssuesEvent':
        print(f'Opened an issue in {repo_name}')


if __name__ == "__main__":
    if username == None:
        print("Enter a username")
    else:
        data = get_user_activity(event_url)
        print(type(data))
        process_data(data=data)
