from abc import ABC, abstractmethod
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

class IWorkflow(ABC):
    @abstractmethod
    def __init__(self):
        self.workflow= StateGraph(dict)  # pyright: ignore[reportArgumentType]
        self.chain: None | CompiledStateGraph = None
        pass

    @abstractmethod
    def setup_graph(self):
        pass