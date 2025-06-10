def extract_repositories_metrics_and_versions(repositories):

    results = []

    for result in repositories:
        info = {
            "id": result.get("id"),
            "name": result.get("name"),
            "project_id": result.get("project", {}).get("id"),
            "project_name": result.get("project", {}).get("name"),
            "remote_url": result.get("remoteUrl")
        }
        results.append(info)

    return results
