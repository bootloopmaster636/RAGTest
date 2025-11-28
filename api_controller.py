from fastapi import FastAPI, HTTPException
from config import FASTAPI_APP_TITLE
from workflow.i_workflow import IWorkflow
from entity.api_entity import DocumentRequest, QuestionRequest
from document_store import DocumentStore
import time

class ApiController:
    def __init__(self, workflow: IWorkflow, storage: DocumentStore):
        self.app = FastAPI(title=FASTAPI_APP_TITLE)

        self.app.post("/ask")(self.__ask_question)
        self.app.post("/add")(self.__add_document)
        self.app.get("/status")(self.__status)

        self.workflow = workflow
        self.storage = storage
    
    def __ask_question(self, req: QuestionRequest):
        start = time.time()
        try:
            result = self.workflow.chain.invoke({"question": req.question})
            return {
                "question": req.question,
                "answer": result["answer"],
                "context_used": result.get("context", []),
                "latency_sec": round(time.time() - start, 3)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

            
    def __add_document(self, req: DocumentRequest):
        try:
            doc_id = self.storage.add(text=req.text)
            return {"id": doc_id, "status": "added"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    def __status(self):
        return {
            "qdrant_ready": self.storage.use_qdrant,
            "in_memory_docs_count": self.storage.get_in_memory_fallback_len,
            "graph_ready": self.workflow.chain is not None
        }