from embeddings.i_embeddings import IEmbedding
import random

class FakeEmbedding(IEmbedding):
    def embed(self, text: str) -> list[float]:
        # Seed based on input so it's "deterministic"
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(128)]  # Small vector for demo