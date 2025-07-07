import yaml
import os
from pydantic import BaseModel, ValidationError, SecretStr, ConfigDict


class AppConfigServer(BaseModel):
    host: str = "0.0.0.0"
    port: int = 9001
    debug: bool = False


class AppConfigMikrotik(BaseModel):
    host: str
    user: str
    password: SecretStr


class AppConfig(BaseModel):
    model_config = ConfigDict(hide_input_in_errors=True)

    server: AppConfigServer = AppConfigServer()
    mikrotik: AppConfigMikrotik


cfg = None | AppConfig


def load_config(config_path: str) -> AppConfig:
    """Load configuration from a YAML file."""
    try:
        with open(config_path, "r") as file:
            config_data = yaml.safe_load(file)
        return AppConfig(**config_data)
    except FileNotFoundError:
        print(
            f"Configuration file not found: {config_path} - falling back to environment variables"
        )
        return AppConfig(
            server=AppConfigServer(),
            mikrotik=AppConfigMikrotik(
                host=os.environ["MNV_HOST"],
                user=os.environ["MNV_USER"],
                password=SecretStr(os.environ["MNV_PASS"]),
            ),
        )
    except ValidationError as e:
        raise ValueError(f"Invalid configuration: {e}") from e
