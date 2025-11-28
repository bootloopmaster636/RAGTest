from abc import ABC, abstractmethod

class IEmbedding(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        pass