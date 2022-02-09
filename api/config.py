""" config.py """

from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # first argument of 'Field' is the default
    api_name: str = Field('API Name', env="API_NAME")
    # ellipsis here means field is required
    # (https://pydantic-docs.helpmanual.io/usage/schema/#field-customization)
    model_version: str = Field(..., env="MODEL_VERSION")

    class Config:
        env_file = '.env'


@lru_cache
def getSettings():
    return Settings()
