#!/usr/bin/python3
# Get user github activity data
import sys
import json
from urllib import request, error


username = sys.argv[1]
event_url = f"https://api.github.com/users/{username}/events"

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

def process_data(data: dict) -> str:
    print(type(data))
    print(f"Length of data: {len(data)}")
    for item in data:
        t = item.get('type')
        repo_url = item.get('repo').get('url')
        match t:
            case 'PushEvent':
                commit_len = len(item.get('payload').get('commits'))
                repo_name = get_repo_name(repo_url)
                print(f"Pushed {commit_len} commits to {repo_name}")

if __name__ == "__main__":    
    if username == None:
        print("Enter a username")
    else:
        data = get_user_activity(event_url)
        print(type(data))
        process_data(data=data)
