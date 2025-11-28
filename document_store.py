from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from config import QDRANT_COLLECTION_NAME, QDRANT_URL
from embeddings.i_embeddings import IEmbedding
import uuid

class DocumentStore:
    def __init__(self, embedder: IEmbedding):
        self.qdrant: QdrantClient = QdrantClient(QDRANT_URL)
        self.use_qdrant: bool = False
        self.in_memory_fallback: list = []
        self.embedder: IEmbedding = embedder

        self.__init_collection()

    # Get in memory fallback length
    def get_in_memory_fallback_len(self) -> int:
        return len(self.in_memory_fallback)

    # Initialize the collection, enabling Qdrant mode
    # if available. 
    def __init_collection(self):
        try:
            self.qdrant.create_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(size=128, distance=Distance.COSINE)
            )
            self.use_qdrant = True
        except Exception as e:
            print("⚠️  Qdrant not available. Falling back to in-memory list.")
            self.use_qdrant = False
    
    # Query specified string to array of payload
    # Params:
    # text: text to search in storage
    def query(self, text: str) -> list:
        results = []
        embedded_query = self.embedder.embed(text=text)

        if self.use_qdrant:
            hits = self.qdrant.search(collection_name=QDRANT_COLLECTION_NAME, query_vector=embedded_query, limit=2)
            for hit in hits:
                results.append(hit.payload["text"])
        else:
            for doc in self.in_memory_fallback:
                if text.lower() in doc.lower():
                    results.append(doc)
            if not results and self.in_memory_fallback:
                results = [self.in_memory_fallback[0]]  # Just grab first

        return results

    # Add specified string to memory/database
    # Params:
    # text: text to insert to storage
    def add(self, text: str) -> str:
        doc_id = uuid.uuid4().hex
        embedded_query = self.embedder.embed(text=text)
        payload = {"text": text}

        if self.use_qdrant:
            self.qdrant.upsert(
                QDRANT_COLLECTION_NAME,
                points=[PointStruct(id=doc_id, vector=emb, payload=payload)]
            )
        else:
            self.in_memory_fallback.append(text)

        return doc_id
