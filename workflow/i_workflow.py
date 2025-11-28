from abc import ABC, abstractmethod
from langgraph.graph.state import StateGraph, CompiledStateGraph

class IWorkflow(ABC):
    @abstractmethod
    def __init__(self):
        self.workflow: StateGraph = StateGraph(dict)
        self.chain: CompiledStateGraph  = None
        pass

    @abstractmethod
    def setup_graph(self):
        pass