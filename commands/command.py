from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_message(self, message):
        pass