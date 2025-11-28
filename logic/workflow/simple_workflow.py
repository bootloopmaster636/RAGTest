from logic.workflow.i_workflow import IWorkflow
from langgraph.graph import END, StateGraph
from data.access.document_store import DocumentStore

class SimpleWorkflow(IWorkflow):
    def __init__(self, storage: DocumentStore):
        super().__init__()
        self.storage = storage
        self.setup_graph()

    def setup_graph(self):
        workflow = self.workflow
        workflow.add_node("retrieve", self.__simple_retrieve)
        workflow.add_node("answer", self.__simple_answer)

        workflow.set_entry_point("retrieve")

        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)

        self.chain = workflow.compile()

    def __simple_retrieve(self, state):
        query = state["question"]
        results = self.storage.query(query)
        state["context"] = results
        return state

    def __simple_answer(self, state):
        ctx = state["context"]
        if ctx:
            answer = f"I found this: '{ctx[0][:100]}...'"
        else:
            answer = "Sorry, I don't know."
        state["answer"] = answer
        return state