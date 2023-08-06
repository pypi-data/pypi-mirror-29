import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Settings:

    def __init__(self):
        self.settings = None

    def read(self, filename):
        with open(filename) as f:
            self.settings = yaml.safe_load(f)

    def get(self, item):
        if self.settings:
            return self.settings[item]
        else:
            raise ValueError("Settings is not yet initialized!")

    def __getitem__(self, item):
        return self.get(item)


settings = Settings()
