from unittest.mock import patch
from azuredevops.generate.azure_detail import build_repository_metrics_entry

@patch("azuredevops.azure_detail.get_repository_files")
@patch("azuredevops.azure_detail.detect_repository_language")
@patch("azuredevops.azure_detail.compute_file_metrics")
def test_build_repository_metrics_entry(mock_compute, mock_detect, mock_get_files):
    # Arrange
    repository = {
        "project_name": "test_project",
        "name": "test_repo",
        "id": "abc123"
    }

    mock_get_files.return_value = [
        {"path": "/path/file1.py"},
        {"path": "/path/file2.py"},
        {"path": "/path/file3.py"},
        {"path": "/path/file4.py"}
    ]

    mock_detect.return_value = "Python"
    mock_compute.return_value = {
        "py": {"count": 4, "lines": 150}
    }

    #Act
    result = build_repository_metrics_entry(repository, "https://dev.azure.com/org", {})

    #Assert
    assert result[0][0] == "Summarized"
    assert result[1][0] == "Detailed"
    assert result[0][4] == "Python"
    assert result[1][6] == 4
    assert result[1][7] == 150


