import requests
import os
from az_devops.generate.azure_detail import build_repository_metrics_entry
from az_devops.connection.azure_connection import get_azure_connection_cloud, get_azure_connection_legacy
from az_devops.metric.azure_metrics import extract_repositories_metrics_and_versions
from az_devops.settings.azure_settings import Settings


class AzureDevopsService:
    def __init__(self):
        self.settings = Settings()

    def _select_connection(self):
        environment = self.settings.azure_environment.lower()

        if environment == "cloud":
            return get_azure_connection_cloud()
        elif environment == "legacy":
            return get_azure_connection_legacy()
        else:
           raise ValueError("Unknown environment: {environment}")

    def get_all_azure_devops_repositories(self):
        connection = self._select_connection()
        base_url, headers, _ = connection
        url = f"{base_url}/_apis/git/repositories?api-version=5.1"
        response = requests.get(url, headers=headers, verify=False)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch repositories. Status code: {response.status_code}, {response.text}")

        repositories = response.json().get("value", [])
        rows = []
        rows.append(["Project name", "Repository name", "File extension"])

        for repo in repositories:
            print(f"Processing repository {repo['project']['name']} / {repo['name']}")
            extensions = self.get_repository_extensions(
                project=repo["project"]["name"],
                repo_id=repo["id"],
                base_url=base_url,
                headers=headers
            )
            print(f"[DEBUG] Extensões encontradas para {repo['name']}: {extensions}")
            for ext in extensions:
                rows.append([
                    repo["project"]["name"],
                    repo["name"],
                    ext
                ])

        return rows

    def get_repository_extensions(self,project, repo_id, base_url, headers):
        url = f"{base_url}/{project}/_apis/git/repositories/{repo_id}/items?recursionlevel=Full&api-version=5.1"
        params = {
            "recursionLevel": "Full",
            "includeContentMetadata": "true",
            "api-version": "6.0"
        }
        response = requests.get(url, headers=headers, params=params, verify=False)
        if response.status_code != 200:
            print(f"Erro ao buscar arquivos do repositório {repo_id}: {response.text}")
            return []
        
        data = response.json()
        extensions = set()

        for item in data.get("value", []):
            print(item)
            if item.get("gitObjectType") == "blob":
                path = item.get("path", "")
                _, ext = os.path.splitext(path)
                if ext:
                    extensions.add(ext.lower())

        return list(extensions)




