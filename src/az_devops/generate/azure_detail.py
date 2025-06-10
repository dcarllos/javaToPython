from az_devops.extension.azure_extension import compute_file_metrics
from az_devops.file.azure_repository import get_repository_files
from az_devops.language.azure_language import detect_repository_language

def build_repository_metrics_entry(repository, base_url, headers):
    project_name = repository["project_name"]
    repository_name = repository["name"]
    repository_id = repository["id"]

    files = get_repository_files(base_url, headers, project_name, repository_id)
    languages = detect_repository_language(files)
    metrics = compute_file_metrics(files)

    summarized = ["Summarized", repository_id, project_name, repository_name, languages, "#", "#"]
    detailed = [
        ["Detailed", repository_id, project_name, repository_name, "#", value, data["count"], data["lines"]]
        for value, data in metrics.items()
    ]

    return [summarized] + detailed