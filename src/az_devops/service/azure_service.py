import requests
import os
from az_devops.generate.azure_detail import build_repository_metrics_entry
from az_devops.connection.azure_connection import get_azure_connection_cloud, get_azure_connection_legacy
from az_devops.metric.azure_metrics import extract_repositories_metrics_and_versions
from az_devops.settings.azure_settings import Settings
from collections import Counter

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
        rows = [["Project name", "Repository name", "Branch", "File extension", "Count"]]

        for repo in repositories:
            project_name = repo["project"]["name"]
            repo_name = repo["name"]
            repo_id = repo["id"]
        
            # 1) Buscar todas as branches do repositório
            refs_url = f"{base_url}/{project_name}/_apis/git/repositories/{repo_id}/refs"
            params_refs = {
                "filter": "heads/",        # pega apenas refs/heads/*
                "api-version": "6.0"
            }
            resp_refs = requests.get(refs_url, headers=headers, params=params_refs, verify=False)
            branches = [
                ref["name"].split("/")[-1] 
                for ref in resp_refs.json().get("value", [])
            ]
        
            for branch in branches:
                # 2) Listar todos os arquivos dessa branch
                items_url = f"{base_url}/{project_name}/_apis/git/repositories/{repo_id}/items"
                params_items = {
                    "recursionLevel": "Full",
                    "includeContentMetadata": "true",
                    "versionType": "branch",
                    "version": branch,
                    "api-version": "6.0"
                }
                resp_items = requests.get(items_url, headers=headers, params=params_items, verify=False)
                items = resp_items.json().get("value", [])
        
                # 3) Contar arquivos por extensão
                ext_counter = Counter()
                for item in items:
                    if item.get("gitObjectType") == "blob":
                        _, ext = os.path.splitext(item.get("path", ""))
                        if ext:
                            ext_counter[ext.lower()] += 1
        
                # 4) Adicionar ao CSV
                for ext, count in ext_counter.items():
                    rows.append([
                        project_name,
                        repo_name,
                        branch,
                        ext,
                        count
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




