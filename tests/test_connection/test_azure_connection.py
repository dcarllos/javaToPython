import pytest
from unittest.mock import patch
from azuredevops.connection.azure_connection import get_azure_connection_cloud, get_azure_connection_legacy


@patch("azuredevops.connection.azure_connection.Settings")
def test_get_azure_connection_cloud_success(mock_settings_class):
    # Arrange
    mock_settings = mock_settings_class.return_value
    mock_settings.azure_devops_url = "https://dev.azure.com/fakeorg"
    mock_settings.azure_devops_token = "Basic faketoken"

    # Act
    url, headers, auth = get_azure_connection_cloud()

    # Assert
    assert url == "https://dev.azure.com/fakeorg"
    assert headers == {
        'Accept': 'application/json',
        'Authorization': "Basic faketoken"
    }
    assert auth is None


@patch("azuredevops.connection.azure_connection.Settings")
def test_get_azure_connection_legacy_success(mock_settings_class):
    mock_settings = mock_settings_class.return_value
    mock_settings.azure_devops_legacy_url = "https://dev.azure.com/legacyorg"
    mock_settings.azure_devops_legacy_token = "Basic legacypass"

    url, headers, auth = get_azure_connection_legacy()

    assert url == "https://dev.azure.com/legacyorg"
    assert headers["Authorization"] == "Basic legacypass"
    assert auth is None


@patch("azuredevops.connection.azure_connection.Settings")
def test_get_azure_connection_cloud_missing_values(mock_settings_class):
    mock_settings = mock_settings_class.return_value
    mock_settings.azure_devops_url = ""
    mock_settings.azure_devops_token = ""

    with pytest.raises(ValueError, match="AZURE_DEVOPS_URL and TOKEN must be set."):
        get_azure_connection_cloud()


@patch("azuredevops.connection.azure_connection.Settings")
def test_get_azure_connection_legacy_missing_values(mock_settings_class):
    mock_settings = mock_settings_class.return_value
    mock_settings.azure_devops_legacy_url = None
    mock_settings.azure_devops_legacy_token = ""

    with pytest.raises(ValueError, match="AZURE_DEVOPS_LEGACY_URL and TOKEN must be set."):
        get_azure_connection_legacy()
