import json
from pathlib import Path


class Config:
    _instance = None

    _DEFAULTS = {
        "path": "",
        "company": "Company",
        "app_name": "AppName",
    }

    _CONFIG_FILE = Path("config.json")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self._initialized = True
        self._config = {}

        if self._CONFIG_FILE.exists():
            self._load()
        else:
            self._config = self._DEFAULTS.copy()
            self.save()

    def _load(self):
        with self._CONFIG_FILE.open("r", encoding="utf-8") as f:
            self._config = json.load(f)

        # Add any missing default keys
        changed = False
        for key, value in self._DEFAULTS.items():
            if key not in self._config:
                self._config[key] = value
                changed = True

        if changed:
            self.save()

    def save(self):
        with self._CONFIG_FILE.open("w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=4)

    def get(self, key, default=None):
        return self._config.get(key, default)

    def set(self, key, value):
        self._config[key] = value
        self.save()

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value
        self.save()
