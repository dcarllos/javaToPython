import requests

def get_repository_files(base_url, headers, project_name, repository_id):
    items_url = f"{base_url}/{project_name}/_apis/git/repositories/{repository_id}/items"

    params = {
        "recursionLevel": "Full",
        "includeContentMetadata": "true",
        "api-version": "6.0"
    }

    response = requests.get(items_url, headers=headers, params=params, verify=False)
    if response.status_code != 200:
        print(f"Failed to fetch files for repository {repository_id}")
        return []
    else:
        return response.json().get("value", [])