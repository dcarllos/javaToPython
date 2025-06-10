from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    azure_environment: str
    azure_devops_url: str
    azure_devops_token: str
    azure_devops_legacy_url: str
    azure_devops_legacy_token: str

    class Config:
        env_file = ".env"
