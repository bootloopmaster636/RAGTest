from document_store import DocumentStore
from workflow.simple_workflow import SimpleWorkflow
from api_controller import ApiController
from embeddings.fake import FakeEmbedding
import uvicorn

def main():
    print('Making database...')
    fake_embedding = FakeEmbedding()
    storage = DocumentStore(embedder=fake_embedding)

    print('Building workflow...')
    workflow = SimpleWorkflow(storage=storage)

    print('Preparing server...')
    api_controller = ApiController(workflow=workflow, storage=storage)
        
    print('Running server...')
    uvicorn.run(app=api_controller.app)

    print('Server ready to use...')

if __name__ == '__main__':
    main()