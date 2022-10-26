""" config.py """

from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # first argument of 'Field' is the default
    api_name: str = Field('API Name', env='API_NAME')
    # ellipsis here means field is required
    # (https://pydantic-docs.helpmanual.io/usage/schema/#field-customization)
    model_version: str = Field(..., env='MODEL_VERSION')
    model_directory: str = Field(..., env='MODEL_DIRECTORY')
    #
    astra_db_keyspace: str = Field(..., env='ASTRA_DB_KEYSPACE')
    astra_db_secure_bundle_path: str = Field(..., env='ASTRA_DB_SECURE_BUNDLE_PATH')
    astra_db_application_token: str = Field(..., env='ASTRA_DB_APPLICATION_TOKEN')

    # this trick is redundant once we enforce a restricted Pydantic schema
    # on the route response, but ...
    # (see https://fastapi.tiangolo.com/tutorial/response-model/#add-an-output-model)
    secret_fields = {
        'astra_db_secure_bundle_path',
        'astra_db_application_token',
        'secret_fields',
    }

    # mock-model setting (usually False!)
    # This field will not be returned by the "/" endpoint thanks to the route
    # enforcing the response to be of type APIInfo.
    mock_model_class: bool = Field(..., env='MOCK_MODEL_CLASS')

    class Config:
        env_file = '.env'


@lru_cache()
def getSettings():
    return Settings()

