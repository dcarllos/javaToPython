from az_devops.settings.azure_settings import Settings

def get_azure_connection_legacy():
    settings = Settings()
    url = settings.azure_devops_legacy_url
    token = settings.azure_devops_legacy_token

    if not url or not token:
        raise ValueError("AZURE_DEVOPS_LEGACY_URL and TOKEN must be set.")

    headers = {
        'Accept': 'application/json',
        'Authorization': token
    }
    return url.rstrip('/'), headers, None


def get_azure_connection_cloud():
    settings = Settings()
    url = settings.azure_devops_url
    token = settings.azure_devops_token

    if not url or not token:
        raise ValueError("AZURE_DEVOPS_URL and TOKEN must be set.")

    headers = {
        'Accept': 'application/json',
        'Authorization': token
    }
    return url.rstrip('/'), headers, None
