from ruamel import yaml
from typing import NamedTuple, Optional

from pathlib import Path


class UserContext(NamedTuple):
    api_url: Optional[str] = None
    api_token: Optional[str] = None

    @classmethod
    def load(cls, config_path: Path):
        config = yaml.safe_load(config_path.open("r"))
        return cls(**config)

    def store(self, config_path: Path):
        config_path.mkdir(parents=True, exist_ok=True)
        yaml.dump(dict(self._asdict()), config_path.open("w"))
