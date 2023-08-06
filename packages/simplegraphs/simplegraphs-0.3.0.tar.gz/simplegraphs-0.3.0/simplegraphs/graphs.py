from abc import ABC, abstractmethod
from typing import Dict, List, Set, Iterable, Iterator

class Vertice:
    def __init__(self, label: str=None) -> 'Vertice':
        """
        Create a new vertice.

        :param label str: Label of vertice.
        :returns: New vertice.
        :rtype: Vertice
        """
        self._label = label
        self._neighbors = set()
        self._incoming = set()
        self._outgoing = set()
        self._edges = set()
        self._incoming_edges = set()
        self._outgoing_edges = set()
        self._edge_to_vertice = {}

    @property
    def label(self) -> str:
        """
        Label of vertice (`str`).
        """
        return self._label

    @label.setter
    def label(self, value: str):
        self._label = value

    @property
    def neighbors(self) -> Set['Vertice']:
        """
        Set of all neighboring vertices (`Set[Vertice]`).
        """
        return self._neighbors

    @neighbors.setter
    def neighbors(self, value: Set['Vertice']):
        self._neighbors = value

    @property
    def incoming(self) -> Set['Vertice']:
        """
        Set of all incoming vertices (`Set[Vertice]`).
        """
        return self._incoming

    @incoming.setter
    def incoming(self, value: Set['Vertice']):
        self._incoming = value

    @property
    def outgoing(self) -> Set['Vertice']:
        """
        Set of all outgoing vertices (`Set[Vertice]`).
        """
        return self._outgoing

    @outgoing.setter
    def outgoing(self, value: Set['Vertice']):
        self._outgoing = value

    @property
    def edges(self) -> Set['Edge']:
        """
        Set of all connected edges (`Set[Edge]`).
        """
        return self._edges

    @edges.setter
    def edges(self, value: Set['Edge']):
        self._edges = value

    @property
    def incoming_edges(self) -> Set['Edge']:
        """
        Set of all incoming edges (`Set[Edge]`).
        """
        return self._incoming_edges

    @incoming_edges.setter
    def incoming_edges(self, value: Set['Edge']):
        self._incoming_edges = value

    @property
    def outgoing_edges(self) -> Set['Edge']:
        """
        Set of all outgoing edges (`Set[Edge]`).
        """
        return self._outgoing_edges

    @outgoing_edges.setter
    def outgoing_edges(self, value: Set['Edge']):
        self._outgoing_edges = value

    def __iter__(self) -> Iterator['Vertice']:
        return _BreadthFirstIterator(self)

    def edge(self, other: 'Vertice') -> 'Edge':
        """
        Returns edge connecting this vertice to another vertice.

        :param other Vertice: Other vertice.
        :returns: Connecting edge
        :rtype: Edge
        """
        return self._edge_to_vertice[other]

    def bfs(self) -> Iterator['Vertice']:
        return _BreadthFirstIterator(self)

    def dfs(self) -> Iterator['Vertice']:
        return _DepthFirstIterator(self)
        
    def connect(self, other: 'Vertice', directed: bool=False, weight: int=0):
        if directed:
            DirectedEdge(self, other, weight)
        else:
            UndirectedEdge(self, other, weight)

    def disconnect(self, other: 'Vertice'):
        self._edge_to_vertice[other].disconnect()


class Edge:
    """
    Edge between two vertices.
    """
    def __init__(self, vertice1: Vertice, vertice2: Vertice, 
                 weight: float=0) -> 'Edge':
        self._vertice1 = vertice1
        self._vertice2 = vertice2
        self._weight = weight

        vertice1.neighbors.add(vertice2)
        vertice2.neighbors.add(vertice1)
        vertice1.edges.add(self)
        vertice2.edges.add(self)

        vertice1._edge_to_vertice[vertice2] = self
        vertice2._edge_to_vertice[vertice1] = self
        
    @property
    def weight(self) -> float:
        """
        Cost of traversing edge (`float`).
        """
        return self._weight

    @weight.setter
    def weight(self, value: float):
        self._weight = value

    @abstractmethod
    def traverse(self, origin: Vertice) -> Vertice:
        """
        Traverse from one vertice in an edge to the other.

        :param origin Vertice: Starting vertice of traversal.
        :returns: Opposing vertice from origin.
        :rtype: Vertice
        """
        if origin == self._vertice1:
            return self._vertice2
        elif origin == self._vertice2:
            return self._vertice1

    def disconnect(self):
        self._vertice1.neighbors.discard()
        self._vertice1.outgoing.discard()
        self._vertice1.incoming.discard()
        self._vertice1._edge_to_vertice.pop(self._vertice2, None)

        self._vertice2.neighbors.discard()
        self._vertice2.outgoing.discard()
        self._vertice2.incoming.discard()
        self._vertice2._edge_to_vertice.pop(self._vertice1, None)


    def _connect(self, outgoing: Vertice, incoming: Vertice):
        outgoing.outgoing.add(incoming)
        incoming.incoming.add(outgoing)
        outgoing.outgoing_edges.add(self)
        incoming.incoming_edges.add(self)


class DirectedEdge(Edge):
    """
    Directed edge between two vertices.
    """
    def __init__(self, outgoing: Vertice, incoming: Vertice, 
                 weight: float=0) -> 'DirectedEdge':
        """
        Create a new directed edge between two vertices.

        :param outgoing Vertice: Outgoing vertice.
        :param incoming Vertice: Incoming vertice.
        :param weight float: Cost of travering edge.
        :returns: Directed edge between outgoing and incoming vertices.
        :rtype: DirectedEdge
        """
        Edge.__init__(self, outgoing, incoming, weight)
        self._outgoing = outgoing
        self._incoming = incoming
        self._connect(outgoing, incoming)

    @property
    def outgoing(self) -> Vertice:
        """
        Outgoing vertice of directed edge.
        """
        return self._outgoing

    @property
    def incoming(self) -> Vertice:
        """
        Incoming vertice of directed edge.
        """
        return self._incoming

    def traverse(self) -> Vertice:
        """
        Traverse to the incoming vertice of a directed edge.

        :returns: Incoming vertice of edge.
        :rtype: Vertice
        """
        return self.incoming


class UndirectedEdge(Edge):
    """
    Undirected edge between two vertices.
    """
    def __init__(self, vertice1: Vertice, vertice2: Vertice,
                 weight: int=0) -> 'UndirectedEdge':
        """
        Create a new undirected edge between two vertices.

        :param vertice1 Vertice: Vertice of edge.
        :param vertice2 Vertice: Vertice of edge.
        :param weight float: Cost of travering edge.
        :returns: Undirected edge between vertice1 and vertice2.
        :rtype: UndirectedEdge
        """
        Edge.__init__(self, vertice1, vertice2, weight)
        self._connect(vertice1, vertice2)
        self._connect(vertice2, vertice1)

    def traverse(self, origin: Vertice) -> Vertice:
        """
        Traverse from one vertice in an edge to the other.

        :param origin Vertice: Starting vertice of traversal.
        :returns: Opposing vertice from origin.
        :rtype: Vertice
        """
        return super().traverse(origin)


class _BreadthFirstIterator():
    def __init__(self, origin: Vertice) -> '_DepthFirstIterator':
        self._queue = [origin]
        self._visited = set()

    def __iter__(self) -> Iterator[Vertice]:
        return self

    def __next__(self) -> Vertice:
        if not self._queue:
            raise StopIteration
        next = self._queue.pop(0)
        self._visited.add(next)
        self._queue += {v for v in next.outgoing if v not in self._visited}
        return next


class _DepthFirstIterator():
    def __init__(self, origin: Vertice) -> '_BreadthFirstIterator':
        self._stack = [origin]
        self._visited = set()

    def __iter__(self) -> Iterator[Vertice]:
        return self

    def __next__(self) -> Vertice:
        if not self._stack:
            raise StopIteration
        next = self._stack.pop()
        self._visited.add(next)
        self._stack += {v for v in next.outgoing if v not in self._visited}
        return next


class Graph:
    def __init__(self):
        self._vertices = set()

    def bfs(self, origin: Vertice) -> Iterable[Vertice]:
        return _BreadthFirstIterator(origin)        

    def dfs(self, origin: Vertice) -> Iterable[Vertice]:
        return _DepthFirstIterator(origin)

    def edge_set(self) -> Set[Edge]:
        raise NotImplementedError

    def add_vertice(self, vertice: Vertice):
        self._vertices.add(vertice)

    def connect(self, vertice1: Vertice, vertice2: Vertice, 
                directed: bool=False, weight: int=0):
        vertice1.connect(vertice1, vertice2, directed, weight)
        