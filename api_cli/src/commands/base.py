from abc import ABC, abstractmethod
from argparse import Namespace
from api.client import ApiClient
from tui import Console


class BaseCommand(ABC):
    def __init__(self, api: ApiClient, console: Console):
        self.api = api
        self.console = console

    @abstractmethod
    def execute(self, args: Namespace) -> None:
        pass
