import itertools
import warnings
from typing import AbstractSet, Callable, Dict, FrozenSet, Iterable, Iterator, List, Optional, Set, Tuple, TypeVar, Union, cast
from uuid import uuid4
from mhelper import Logger, MEnum, MFlags, NOT_PROVIDED, NotFoundError, Serialisable, SwitchError, TTristate, ansi, array_helper, exception_helper, string_helper
from mhelper.exception_helper import MultipleError


T = TypeVar( "T" )

TUid = int
"""UID of a node. It's an int."""

TNodeOrUid = Union[TUid, "MNode"]
"""A node in the graph, or a UID allowing the node to be found, or a node in another graph that can also be found in this graph"""

DFindId = Callable[[str], object]
DNodePredicate = Callable[["MNode"], bool]
DEdgePredicate = Callable[["MEdge"], bool]
DNodeToText = Callable[["MNode"], str]
DEdgeToText = Callable[["MEdge"], str]
UNodeToText = Union[DNodeToText, str]
DConverter = Callable[[object], object]
DTransform = Callable[[object], object]
UNodePredicate = Union[DNodePredicate, "MNode", List["MNode"], Set["MNode"], Tuple["MNode"], None]
UEdgePredicate = Union[DEdgePredicate, "MEdge", List["MEdge"], Set["MEdge"], Tuple["MEdge"], None]

__LOG_F = Logger( "follow", False )


def _identity( x ):
    return x


class EGraphFormat( MEnum ):
    """
    :data NEWICK:        Newick format
    :data ASCII:         ASCII diagram (basic)
    :data EDGELIST:      Edgelist
    :data SVG:           SVG
    :data HTML:          HTML SVG
    :data COMPACT:       Compact edgelist (does not support node names)
    :data ETE_ASCII:     ASCII diagram (better but requires Ete)
    :data NODELIST:      Nodes (no edges)
    """
    NEWICK = 1
    ASCII = 2
    CSV = 3
    TSV = 4
    _OBSOLETE = 5
    COMPACT = 6
    ETE_ASCII = 7
    NODELIST = 8
    ANCESTRY = 9


class ExistsError( Exception ):
    pass


class EdgeExistsError( ExistsError ):
    pass


class EDirection( MFlags ):
    """
    Direction of edges.
    
    :data INCOMING: Incoming edges. A<--B. Effective roots have no children. For trees, traversal is from the true leaves to the true roots.
    :data OUTGOING: Outgoing edges. A-->B. Effective roots have no parents.  For trees, traversal is from the true roots to the true leaves.
    :data BOTH:     Any edges. A---B.      Effective roots have no children and/or no parents.   For trees, traversal is in both directions. 
    """
    INCOMING: "EDirection" = 1
    OUTGOING: "EDirection" = 2
    BOTH: "EDirection" = 3


class DepthInfo:
    """
    Describes how a node was located when calling `MGraph.follow`.
    
    :attr node:                   Node in question.
    :attr depth:                  Depth of node from start.
    :attr follow_edge:            Edge through which this node was found.
    :attr follow_is_last:         UI hint. Is this the last listed child of the parent.
    :attr follow_is_repeat:       UI hint. Has this node already been listed. 
    :attr follow_parent_info:     Parent through which this node was found. 
    :attr follow_has_children:    UI hint. Does this node have any children.
    """
    
    
    def __init__( self,
                  *,
                  node: "MNode",
                  edge: Optional["MEdge"],
                  is_last: bool,
                  is_repeat: bool,
                  parent_info: "Optional[DepthInfo]",
                  has_children: bool ):
        """
        CONSTRUCTOR 
        """
        self.node = node
        self.depth = (parent_info.depth + 1) if parent_info is not None else 0
        self.edge = edge,
        self.is_last = is_last
        self.is_repeat = is_repeat
        self.parent = parent_info
        self.has_children = has_children
    
    
    def full_path( self ) -> "List[DepthInfo]":
        r = []
        parent = self.parent
        
        while parent:
            r.append( parent )
            parent = parent.parent
        
        return list( reversed( r ) )
    
    
    def describe( self, get_text: DNodeToText ) -> str:
        # return "{}:{}{}".format( "{}".format(self.parent.node.uid) if self.parent else "R", "*" if self.is_repeat else "", self.node.detail )
        # return "{}{}->{}".format( "{}".format( self.parent.node.uid ) if self.parent else "(NO_PARENT)", "(POINTER)" if self.is_repeat else "", self.node.detail )
        ss = []
        
        for parent in self.full_path():
            ss.append( "    " if parent.is_last else "│   " )
            # ss.append( str(parent.node.uid).ljust(4, ".") )
        
        if self.node.is_root:
            ss.append( "    " )
        else:
            ss.append( "└───" if self.is_last else "├───" )
        
        if self.is_repeat:
            ss.append( "(REPEAT)" )
        
        ss.append( "┮" if self.has_children else "╼" )
        ss.append( get_text( self.node ) )
        
        return "".join( ss )


class GraphRecursionError( Exception ):
    def __init__( self, message: str, nodes: List["MNode"] ):
        message += " Nodes: «{}»".format( string_helper.format_array( nodes, join = "-->" ) )
        super().__init__( message )
        self.nodes = nodes


class FollowParams:
    def __init__( self,
                  *,
                  start: "MNode",
                  include_repeats: bool = False,
                  edge_filter: UNodePredicate = None,
                  node_filter: UEdgePredicate = None,
                  direction: EDirection = EDirection.BOTH ) -> None:
        """
        Parameters for recursing a graph.
        
        :param start:               Node to start at. 
        :param include_repeats:     If the graph loops, whether we should return the loop points. 
        :param direction:           In what direction should we follow the edges. 
        :param edge_filter:         A UEdgePredicate determining whether we traverse individual edges. 
        :param node_filter:         A UNodePredicate determining whether we traverse individual nodes.
        """
        from mgraph import analysing
        self.used: bool = False
        self.graph: MGraph = start.graph
        self.include_repeats: bool = include_repeats
        self.fn_filter_edges = analysing.realise_edge_predicate( edge_filter )
        self.fn_filter_nodes = analysing.realise_node_predicate( node_filter )
        self.visited: List[DepthInfo] = []
        self.root_info: DepthInfo = DepthInfo( node = start,
                                               edge = None,
                                               is_last = True,
                                               is_repeat = False,
                                               parent_info = None,
                                               has_children = False )
        
        self.visited.append( self.root_info )
        self.direction = direction
    
    
    def __iter__( self ):
        return iter( self.visited_nodes )
    
    
    def execute( self ) -> "FollowParams":
        return self.graph.follow( self )
    
    
    @property
    def visited_nodes( self ) -> List["MNode"]:
        return [x.node for x in self.visited]
    
    
    def get_visited_nodes( self ) -> Set["MNode"]:
        return set( self.visited_nodes )
    
    
    def get_unvisitied_nodes( self ) -> Iterator["MNode"]:
        visited_nodes = self.get_visited_nodes()
        return (x for x in self.graph.nodes if x not in visited_nodes)


class IsolationPoint:
    def __init__( self, edge: "MEdge", internal_node: "MNode", external_node: "MNode", pure_inside_nodes: Set["MNode"], pure_outside_nodes: Set["MNode"], all_inside_nodes: Set["MNode"], all_outside_nodes: Set["MNode"] ) -> None:
        self.edge: MEdge = edge
        self.internal_node: MNode = internal_node
        self.external_node: MNode = external_node
        self.pure_inside_nodes: Set["MNode"] = pure_inside_nodes
        self.pure_outside_nodes: Set["MNode"] = pure_outside_nodes
        self.all_inside_nodes: Set["MNode"] = all_inside_nodes
        self.all_outside_nodes: Set["MNode"] = all_outside_nodes
    
    
    @property
    def count( self ):
        return len( self.pure_inside_nodes )
    
    
    def __str__( self ):
        return "<ISOLATES {} FROM {}>".format( self.pure_inside_nodes, self.pure_outside_nodes )


class IsolationError( Exception ):
    def __init__( self, message, inside_set: Iterable["MNode"], outside_set: Iterable["MNode"] ):
        super().__init__( message )
        self.inside_set = inside_set
        self.outside_set = outside_set


class RootEdgeCollection:
    def __init__( self ):
        self.edges = set()
    
    
    def __repr__( self ):
        return "{} edges".format( len( self ) )
    
    
    def __iter__( self ):
        return iter( self.edges )
    
    
    def _register( self, edge: "MEdge" ):
        self.edges.add( edge )
    
    
    def _deregister( self, edge: "MEdge" ):
        self.edges.remove( edge )
    
    
    def __len__( self ):
        return len( self.edges )


class EdgeCollection:
    def __init__( self, owner: "MNode" ):
        self.owner = owner
        self.outgoing_dict: Dict[MNode, MEdge] = { }
        self.incoming_dict: Dict[MNode, MEdge] = { }
    
    
    def __repr__( self ):
        return "{} outgoing and {} incoming".format( len( self.outgoing_dict ), len( self.incoming_dict ) )
    
    
    def __bool__( self ):
        return bool( self.incoming_dict or self.outgoing_dict )
    
    
    @property
    def incoming( self ) -> AbstractSet["MEdge"]:
        return cast( AbstractSet["MEdge"], self.incoming_dict.values() )
    
    
    @property
    def outgoing( self ) -> AbstractSet["MEdge"]:
        return cast( AbstractSet["MEdge"], self.outgoing_dict.values() )
    
    
    @property
    def count( self ):
        return len( self )
    
    
    def __contains__( self, item: Union["MNode", "MEdge"] ) -> bool:
        if isinstance( item, MNode ):
            return item in self.incoming_dict or item in self.outgoing_dict
        elif isinstance( item, MEdge ):
            return item in self.incoming_dict.values() or item in self.outgoing_dict.values()
        else:
            raise exception_helper.type_error( "item", item, Union[MNode, MEdge] )
    
    
    def __iter__( self ):
        return itertools.chain( self.incoming_dict.values(), self.outgoing_dict.values() )
    
    
    def __len__( self ):
        return len( self.incoming_dict ) + len( self.outgoing_dict )
    
    
    def by_direction( self, direction: EDirection = EDirection.BOTH ) -> List["MEdge"]:
        """
        Iterates over the edges.
        
        :param direction: Direction. -1 = incoming, 1 = outgoing, 0 = both.
        """
        if direction.INCOMING:
            if direction.OUTGOING:
                return list( itertools.chain( self.incoming_dict.values(), self.outgoing_dict.values() ) )
            else:
                return list( self.incoming_dict.values() )
        elif direction.OUTGOING:
            return list( self.outgoing_dict.values() )
    
    
    def has_node( self, node: "MNode", direction: EDirection = EDirection.BOTH ) -> bool:
        try:
            self.by_node( node, direction )
            return True
        except NotFoundError:
            return False
    
    
    def by_node( self, node: "MNode", direction: EDirection = EDirection.BOTH ) -> "MEdge":
        if direction.INCOMING:
            edge = self.incoming_dict.get( node )
            
            if edge is not None:
                return edge
        
        if direction.OUTGOING:
            edge = self.outgoing_dict.get( node )
            
            if edge is not None:
                return edge
        
        raise NotFoundError( "There is no «{}» edge between «{}» and «{}».".format( direction, self.owner, node ) )
    
    
    def list_nodes( self, direction: EDirection = EDirection.BOTH ) -> List["MNode"]:
        if direction.INCOMING:
            if direction.OUTGOING:
                return list( itertools.chain( (x.left for x in self.incoming_dict.values()), (x.right for x in self.outgoing_dict.values()) ) )
            else:
                return [x.left for x in self.incoming_dict.values()]
        elif direction.OUTGOING:
            return [x.right for x in self.outgoing_dict.values()]
    
    
    def _register_outgoing( self, edge: "MEdge" ):
        assert edge.left is self.owner
        self.outgoing_dict[edge.right] = edge
    
    
    def _register_incoming( self, edge: "MEdge" ):
        assert edge.right is self.owner
        self.incoming_dict[edge.left] = edge
    
    
    def _deregister_outgoing( self, edge: "MEdge" ):
        assert edge.left is self.owner
        del self.outgoing_dict[edge.right]
    
    
    def _deregister_incoming( self, edge: "MEdge" ):
        assert edge.right is self.owner
        del self.incoming_dict[edge.left]


class NodeCollection:
    def __init__( self ):
        self._by_id: Dict[int, MNode] = { }
        self._by_data: Dict[object, Set[MNode]] = { }
    
    
    def __repr__( self ):
        return "{} nodes".format( len( self ) )
    
    
    def __bool__( self ) -> bool:
        return bool( self._by_id )
    
    
    def __len__( self ):
        return len( self._by_id )
    
    
    def by_id( self, item ):
        return self._by_id[item]
    
    
    def get_by_id( self, item ):
        return self._by_id.get( item )
    
    
    def by_predicate( self, predicate: DNodePredicate ) -> "MNode":
        try:
            return array_helper.single_or_error( x for x in self if predicate( x ) )
        except KeyError as ex:
            raise KeyError( "Cannot get node by predicate «{}».".format( predicate ) ) from ex
    
    
    def __getitem__( self, item ) -> "MNode":
        return self.by_data( item )
    
    
    def by_data( self, item ) -> "MNode":
        set_ = self._by_data.get( item )
        
        if set_ is None:
            raise ValueError( "There is no node with the data «{}» in the set «{}».".format( item, string_helper.format_array( self, limit = 100 ) ) )
        
        if len( set_ ) != 1:
            raise ValueError( "There are multiple ({}) nodes with the data «{}» in the set «{}».".format( len( set_ ), item, string_helper.format_array( self, limit = 100 ) ) )
        
        for item in set_:
            return item
    
    
    def list_by_data( self, item ) -> Tuple["MNode", ...]:
        return tuple( self._by_data[item] )
    
    
    def __iter__( self ) -> Iterator["MNode"]:
        return iter( self._by_id.values() )
    
    
    def values( self ) -> "NodeCollection":
        warnings.warn( "Deprecated. Use `iter`.", DeprecationWarning )
        return self
    
    
    @property
    def nodes( self ) -> "NodeCollection":
        warnings.warn( "Deprecated. Use `iter`.", DeprecationWarning )
        return self
    
    
    @property
    def clades( self ) -> Iterable["MNode"]:
        """
        Clades (all non-leaf nodes, including roots)
        """
        return (x for x in self if not x.is_leaf)
    
    
    @property
    def roots( self ) -> Iterable["MNode"]:
        """
        Roots (nodes with no parents)
        """
        return (x for x in self if not x.is_root)
    
    
    @property
    def leaves( self ) -> Iterable["MNode"]:
        """
        Leaves (nodes with no children)
        """
        return (x for x in self if not x.is_leaf)
    
    
    @property
    def uids( self ) -> Iterable[int]:
        """
        All UIDs 
        """
        return self._by_id.keys()
    
    
    def _register( self, node: "MNode", uid, data ):
        self._by_id[uid] = node
        self.__register_data_add( node, data )
    
    
    def __register_data_add( self, node, data ):
        set_ = self._by_data.get( data )
        
        if set_ is None:
            set_ = set()
            self._by_data[data] = set_
        
        set_.add( node )
    
    
    def _register_data( self, node: "MNode", old: object, new: object ):
        self.__register_data_remove( node, old )
        self.__register_data_add( node, new )
    
    
    def __register_data_remove( self, node: "MNode", data: object ):
        set_ = self._by_data.get( data )
        set_.remove( node )
        if not set:
            del self._by_data[data]
    
    
    def _unregister( self, node: "MNode", uid: int, data: object ):
        del self._by_id[uid]
        self.__register_data_remove( node, data )


class MGraph:
    """
    Graph class.
    
    :attr data: Arbitrary user-data on the graph.
    """
    
    
    def __init__( self ) -> None:
        """
        CONSTRUCTOR
        """
        self.__nodes = NodeCollection()
        self.__edges = RootEdgeCollection()
        self.data: object = None
    
    
    def __repr__( self ):
        return "{} nodes and {} edges".format( len( self.nodes ), len( self.edges ) )
    
    
    def copy( self,
              *,
              nodes: UNodePredicate = None,
              edges: UEdgePredicate = None,
              preserve_uid: bool = None,
              target: "MGraph" = None,
              data: DTransform = None,
              edge_data: DTransform = None ) -> "MGraph":
        """
        Makes a copy of this graph, or a part thereof.
        
        :param nodes:               Which nodes to copy (a set, list, tuple or predicate) 
        :param edges:               Which edges to copy (a set, list, tuple or predicate)
        :param preserve_uid:        Whether to preserve the UID of the copied nodes.
                                    If this the `target` is the current graph this is `False` by default, otherwise it is `True`.
        :param target:              The graph into which to copy the nodes.
                                    If this is `None` a new graph is created.
        :param data:                Transformation to apply to data to set on new nodes.
        :param edge_data:           Transformation to apply to data to set on new edges.
        :return:                    The graph into which the nodes were copied. 
        """
        if preserve_uid is None:
            if target is self:
                preserve_uid = False
            else:
                preserve_uid = True
        
        if target is self and preserve_uid:
            raise ValueError( "Cannot preserve the UID when the target is self." )
        
        if target is None:
            target = MGraph()
        
        if data is None:
            data = _identity
        
        if edge_data is None:
            edge_data = _identity
        
        import mgraph.analysing
        edges = mgraph.analysing.realise_edge_predicate( edges )
        nodes = mgraph.analysing.realise_node_predicate_as_set( self, nodes )
        
        if not nodes:
            raise ValueError( "Refusing to create a subgraph with no nodes." )
        
        mapping = { }
        
        for old_node in nodes:
            new_node = MNode( target, data( old_node.data ), uid = old_node.uid if preserve_uid else None )
            mapping[old_node] = new_node
        
        for node in nodes:
            for edge in node.edges.outgoing:
                if edges( edge ) and edge.right in nodes:
                    target.add_edge( mapping[edge.left], mapping[edge.right], data = edge_data( edge.data ) )
        
        assert target.nodes
        return target
    
    
    @property
    def nodes( self ) -> NodeCollection:
        return self.__nodes
    
    
    @property
    def edges( self ) -> RootEdgeCollection:
        return self.__edges
    
    
    def __str__( self ):
        return "({} nodes, {} edges)".format( len( self ), len( self.edges ) )
    
    
    def __iter__( self ) -> Iterator["MNode"]:
        return iter( self.nodes )
    
    
    def __len__( self ):
        return len( self.nodes )
    
    
    @property
    def root( self ):
        """
        Returns the root of the graph.
        See :property:`roots`.
        """
        return array_helper.single_or_error( self.iter_roots() )
    
    
    @property
    def any_root( self ):
        """
        Root any root of the graph.
        See :property:`roots`.
        """
        return array_helper.first_or_error( self.iter_roots() )
    
    
    @property
    def roots( self ) -> List["MNode"]:
        """
        Gets the roots of the graph.
        
        A root is defined as a node with 0 parents.
        No checks are made to detect if roots are tree-like.
        See :method:`MNode.make_root` for making roots tree-like. 
        """
        warnings.warn( "Deprecated, use `nodes.roots` instead.", DeprecationWarning )
        return list( self.iter_roots() )
    
    
    def cut( self, left_node: TNodeOrUid, right_node: TNodeOrUid ) -> Tuple["MGraph", "MGraph"]:
        """
        This is the same as `cut_one`, but returns both the left and the right halves of the cut.
        """
        left_node = self.find_node( left_node )
        right_node = self.find_node( right_node )
        
        exception_helper.assert_type( "left_node", left_node, MNode )
        exception_helper.assert_type( "right_node", right_node, MNode )
        
        left_graph = self.cut_one( left_node, right_node )
        right_graph = self.cut_one( right_node, left_node )
        return left_graph, right_graph
    
    
    def cut_one( self, internal_node: "MNode", external_node: "MNode" ) -> "MGraph":
        """
        Cuts the graph along the edge between the specified nodes, yielding a new subset graph.
        
        The new subset contains `containing_node`, and all its relations, excluding those crossing `missing_node`. 
        
        Note this function accepts two nodes, rather than an edge, so that the assignment of
        `containing_node` and `missing_node` is always explicit, which wouldn't be obvious for undirected edges. 
        
        :param internal_node:     Node that will form the inside (accepted) half of the cut 
        :param external_node:     Node that will form the outside (rejected) half of the cut. 
        :return:                  The new graph
        """
        params = FollowParams( start = internal_node, node_filter = lambda x: x is not external_node )
        self.follow( params )
        
        visited_nodes = set( params.visited_nodes )
        visited_edges = set()  # use a set because every edge appears twice (TODO: fix using a directional query)
        
        return self.copy( nodes = visited_nodes, edges = visited_edges )
    
    
    def add_node( self, data: Optional[object] = None ) -> "MNode":
        """
        Convenience function that creates a node with this graph as the owner.
        :return:     The added node 
        """
        return MNode( self, data = data )
    
    
    def add_edge( self, parent: TNodeOrUid, child: TNodeOrUid, *, data: Optional[object] = None ) -> "MEdge":
        """
        Convenience function that creates an edge with this graph as the owner.
        :param parent:  Left node of edge (or a TNodeOrUid allowing the left node to be found)     
        :param child:   Right node of edge (or a TNodeOrUid allowing the right node to be found)
        :param data:    Data on edge 
        :return:        Resulting edge 
        """
        return MEdge( self.find_node( parent ), self.find_node( child ), data = data )
    
    
    def try_add_edge( self, parent: TNodeOrUid, child: TNodeOrUid ) -> Optional["MEdge"]:
        """
        Version of `add_edge` that returns `None` if the edge already exists. 
        """
        try:
            return self.add_edge( parent, child )
        except EdgeExistsError:
            return None
    
    
    def remove_edge( self, left: TNodeOrUid, right: TNodeOrUid, direction: EDirection = EDirection.BOTH ) -> None:
        """
        Removes the specified edge. See `find_edge` for parameter details.
        """
        self.find_edge( left, right, direction ).remove_edge()
    
    
    def find_edge( self, left: TNodeOrUid, right: TNodeOrUid, direction: EDirection = EDirection.BOTH ) -> "MEdge":
        """
        Finds an edge in the graph.
        :param left:        One side of the edge, the parent when direction = EDirection.OUTGOING
        :param right:       The other side of the edge, the child when direction = EDirection.OUTGOING 
        :param direction:   The direction of the edge. 
        :return: The edge 
        """
        return self.find_node( left ).edges.by_node( self.find_node( right ), direction )
    
    
    # noinspection PyDeprecation
    def copy_into( self, target: "MGraph" ) -> None:
        """
        Copies all nodes and edges from this graph into another.
        Note that node information and UIDs are copied, which prevents accidentally incorporating the same set of nodes twice.
        :param target:   The graph to incorporate this graph into.
        """
        warnings.warn( "deprecated, use :method:`copy` instead.", DeprecationWarning )
        for node in self.nodes:
            node.copy_into( target )
        
        for edge in self.edges:
            edge.copy_into( target )
    
    
    def find_node( self, node: TNodeOrUid, default: Optional["MNode"] = NOT_PROVIDED ) -> Optional["MNode"]:
        """
        Finds a node in this graph, to one that exists in a different graph.
         
        :param default: Default value (otherwise error) 
        :param node:    Node or UID of node to find. 
        :return:        Node in this graph. 
        """
        if isinstance( node, MNode ):
            if node.graph is self:
                return node
            else:
                uid = node.uid
        elif isinstance( node, TUid ):
            uid = node
            node = None
        else:
            raise SwitchError( "node", node, instance = True )
        
        result = self.nodes.get_by_id( uid )
        
        if result is not None:
            return result
        
        if default is not NOT_PROVIDED:
            return default
        
        raise ValueError( "Cannot find the requested node (uid = «{}», original = «{}») in this graph.".format( uid, node or "unknown" ) )
    
    
    def format_data( self, format: Callable[[object], object] ):
        for node in self.nodes:
            node.data = format( node.data )
    
    
    def to_compact( self ) -> str:
        """
        Calls :func:`mgraph.exporting.export_compact` using the default parameters.
        This can be considered the extended version of __repr__, containing the minimal information required to recreate the graph (but not the data).
        """
        import mgraph.exporting
        return mgraph.exporting.export_compact( self )
    
    
    def to_ascii( self ) -> str:
        """
        Calls :func:`mgraph.exporting.export_ascii` using the default parameters.
        This can be considered the extended version of __str__, containing a visualisation of the full graph.
        """
        import mgraph.exporting
        return mgraph.exporting.export_ascii( graph = self )
    
    
    def iter_roots( self, node_iter: Iterable["MNode"] = None, direction: EDirection = EDirection.OUTGOING ) -> Iterator["MNode"]:
        """
        Suggests a node in the `subset` that is a root (i.e. has no parents).
        
        The `self.root` will be selected preferentially.
        Then any node with no parents will be selected.
        Then any node will be selected.
        """
        if node_iter is None:
            node_iter = self
        
        yielded = False
        subset = set( node_iter )
        
        if direction.OUTGOING:
            for node in set( subset ):
                if node.num_parents == 0:
                    yielded = True
                    subset.remove( node )
                    yield node
        
        if direction.INCOMING:
            for node in subset:
                if node.num_children == 0:
                    yielded = True
                    yield node
        
        if not yielded:
            raise ValueError( "Cannot suggest an «{}» root from the set because there are no roots in this set: «{}».".format( direction, subset ) )
    
    
    def get_nodes( self ) -> Iterator["MNode"]:
        """
        Iterates over all the nodes.
        """
        return iter( self.nodes )
    
    
    def follow( self, *args, **kwargs ) -> FollowParams:
        """
        Follows the graph from the specified point.
        
        :param args:        Arguments to be passed to the constructor of `FollowParams`.
                            You can also pass a `FollowParams` object directly, which might be nicer from an IDE.
        :return:            The `FollowParams` passed in or created. Its `visited` field should now be set. 
        """
        if len( args ) == 1 and len( kwargs ) == 0 and isinstance( args[0], FollowParams ):
            params = args[0]
        else:
            params = FollowParams( *args, **kwargs )
        
        if params.used:
            raise ValueError( "FollowParams already populated. Use a new object." )
        
        if params.graph is not self:
            raise ValueError( "FollowParams constructed for a different graph." )
        
        params.used = True
        params.graph = self
        
        self.__follow( params = params,
                       parent_info = params.root_info,
                       visited_nodes = set() )
        return params
    
    
    def __follow( self,
                  *,
                  params: FollowParams,
                  parent_info: DepthInfo,
                  visited_nodes: Set["MNode"] ) -> None:
        """
        Populates the `visited` set with all connected nodes, starting from the `source` node.
        Nodes already in the visited list will not be visited again.
        
        Unlike normal path-following, e.g. Dijkstra, this does not use the visited list as the `source`,
        this allows the caller to iterate from a node to the exclusion of a specified branch(es).
        """
        parent = parent_info.node
        edges = parent.edges.by_direction( params.direction )
        depth_info = None
        
        edges = sorted( edges, key = lambda x: len( x.opposite( parent ).edges ) )
        
        for edge in edges:
            if not params.fn_filter_edges( edge ):
                continue
            
            opposite = edge.opposite( parent )
            
            if parent_info.parent is not None and opposite is parent_info.parent.node:
                continue
            
            if not params.fn_filter_nodes( opposite ):
                continue
            
            if opposite in visited_nodes:
                if params.include_repeats:
                    depth_info = DepthInfo( node = opposite,
                                            edge = edge,
                                            is_repeat = True,
                                            parent_info = parent_info,
                                            is_last = False,
                                            has_children = False )
                    
                    params.visited.append( depth_info )
                
                continue
            
            visited_nodes.add( opposite )
            
            depth_info = DepthInfo( node = opposite,
                                    edge = edge,
                                    parent_info = parent_info,
                                    is_last = False,
                                    is_repeat = False,
                                    has_children = False )
            
            params.visited.append( depth_info )
            
            self.__follow( params = params,
                           parent_info = depth_info,
                           visited_nodes = visited_nodes )
        
        if depth_info is not None:
            parent_info.has_children = True
            depth_info.is_last = True


_session_ids = 0


class MNode( Serialisable ):
    """
    Nodes of the MGraph.
    
    :attr __uid:    UID of node
    :attr _graph:   Graph this node is contained within
    :attr _edges:   Edges on this node (in any direction)
    :attr data:     User (arbitrary) data associated with this node
    """
    
    
    def __init__( self, graph: MGraph, data: object = None, *, uid: int = None ):
        """
        CONSTRUCTOR 
        """
        super().__init__()
        if uid is None:
            uid = uuid4().int
        
        self.__uid: int = uid
        self.graph: MGraph = graph
        self.edges: EdgeCollection = EdgeCollection( self )
        self.__data: object = data
        self.__session_id: int = None
        
        if self.__uid in graph.nodes.uids:
            raise ValueError( "Attempt to add a node («{}») to the graph but a node with the same UID already exists in the graph («{}»).".format( self, graph.nodes.by_id( self.__uid ) ) )
        
        graph.nodes._register( self, self.uid, self.data )
    
    
    def _SERIALISABLE_state( self ):
        yield MNode, "__session_id", None
    
    
    @property
    def is_leaf( self ):
        """
        As `is_isolated` for only outgoing nodes.
        """
        return self.num_children == 0
    
    
    @property
    def is_root( self ):
        """
        As `is_isolated` for only incoming nodes.
        """
        return self.num_parents == 0
    
    
    @property
    def is_isolated( self ):
        """
        A node is isolated if it has no relations.
        """
        return self.num_relations == 0
    
    
    @property
    def num_parents( self ):
        """
        As `num_relations` for only incoming nodes.
        """
        return len( self.edges.incoming_dict )
    
    
    @property
    def num_children( self ):
        """
        As `num_relations` for only outgoing nodes.
        """
        return len( self.edges.outgoing_dict )
    
    
    @property
    def num_relations( self ):
        """
        The number of directly connected nodes.
        """
        return len( self.edges )
    
    
    @property
    def has_children( self ) -> bool:
        """
        As `has_relations` for only outgoing nodes.
        """
        return bool( self.edges.outgoing_dict )
    
    
    @property
    def has_parents( self ) -> bool:
        """
        As `has_relations` for only incoming nodes.
        """
        return bool( self.edges.incoming_dict )
    
    
    @property
    def has_relations( self ) -> bool:
        """
        Whether this node has any connected nodes.
        """
        return bool( self.edges )
    
    
    @property
    def parents( self ) -> Iterable["MNode"]:
        """
        As `relations` for incoming nodes.
        """
        return self.edges.incoming_dict.keys()
    
    
    @property
    def children( self ) -> Iterable["MNode"]:
        """
        As `relations` for outgoing nodes.
        """
        return self.edges.outgoing_dict.keys()
    
    
    @property
    def relations( self ) -> Iterable["MNode"]:
        """
        Iterable over connected nodes.
        """
        return itertools.chain( self.parents, self.children )
    
    
    @property
    def parent( self ) -> Optional["MNode"]:
        """
        As `relation` for only incoming nodes.
        """
        return self.__get_relation( EDirection.INCOMING )
    
    
    @property
    def child( self ) -> Optional["MNode"]:
        """
        As `relation` for only outgoing nodes. 
        """
        return self.__get_relation( EDirection.OUTGOING )
    
    
    @property
    def relation( self ) -> Optional["MNode"]:
        """
        Obtains the direct relation of this node.
        :return: The direct relation of the none, or `None` if the node has no relations.
        :except MultipleError: Node has multiple relations.
        """
        return self.__get_relation( EDirection.BOTH )
    
    
    def __get_relation( self, direction: EDirection ):
        incoming_edges = self.edges.by_direction( direction )
        
        if len( incoming_edges ) == 0:
            return None
        elif len( incoming_edges ) == 1:
            return array_helper.single_or_error( incoming_edges ).opposite( self )
        else:
            raise MultipleError( "This node does not have a {} relation because it has more than 1 edge in this direction.".format( direction ) )
    
    
    def list_ancestors( self ) -> List["MNode"]:
        """
        As `list_family` for only incoming nodes.
        """
        return self.list_family( EDirection.INCOMING )
    
    
    def list_descendants( self ) -> List["MNode"]:
        """
        As `list_family` for only outgoing nodes.
        """
        return self.list_family( EDirection.OUTGOING )
    
    
    def list_family( self, direction: EDirection = EDirection.BOTH ) -> List["MNode"]:
        """
        Lists all nodes connected by ONE OR MORE edges.
        """
        return self.graph.follow( FollowParams( start = self, direction = direction ) ).get_visited_nodes() - { self }
    
    
    @property
    def data( self ):
        return self.__data
    
    
    @data.setter
    def data( self, value ):
        self.graph.nodes._register_data( self, self.__data, value )
        self.__data = value
    
    
    def add_child( self, data: Optional[object] = None ) -> "MNode":
        """
        Adds a new node, with an edge from this node to the new node.
         
        :return:    Edge, Node 
        """
        new_node = self.graph.add_node( data = data )
        self.graph.add_edge( self, new_node )
        return new_node
    
    
    def add_parent( self, data: Optional[object] = None ) -> "MNode":
        """
        Adds a new node, with an edge to this node to the new node.
         
        :return:    Edge, Node 
        """
        new_node = self.graph.add_node( data = data )
        self.graph.add_edge( new_node, self )
        return new_node
    
    
    def add_edge_to( self, target: "MNode" ) -> "MEdge":
        """
        Adds an edge from this node to another node.
        """
        return self.graph.add_edge( self, target )
    
    
    def try_add_edge_to( self, target: "MNode" ) -> Optional["MEdge"]:
        """
        Version of `add_edge_to` that returns `None` of the edge already exists.
        """
        return self.graph.try_add_edge( self, target )
    
    
    def remove_edge_to( self, target: "MNode", direction: EDirection = EDirection.BOTH ):
        exception_helper.assert_instance( "target", target, MNode )
        edge = self.edges.by_node( target, direction )
        
        if edge is None:
            raise NotFoundError( "An edge from «{}» to «{}» does not exist.".format( self, target ) )
        
        edge.remove_edge()
    
    
    def make_root( self, *, node_filter: UNodePredicate = None, edge_filter: UEdgePredicate = None ):
        """
        Makes this node the root.
        (All edges expand outwards from here)
        
        :param node_filter: Filter on nodes when enforcing tree like structure originating from the new root. 
        :param edge_filter: Filter on edges when enforcing tree like structure originating from the new root.
        :except ValueError: Graph is not a tree (contains cycles)
        """
        from mgraph import analysing
        node_filter = analysing.realise_node_predicate( node_filter )
        edge_filter = analysing.realise_edge_predicate( edge_filter )
        
        open_set = list( (self, x) for x in self.edges if edge_filter( x ) )
        closed_set = set()
        to_flip = []
        
        while open_set:
            origin, edge = open_set.pop( 0 )
            
            if edge in closed_set:
                raise ValueError( "Cannot make node root because the graph is cyclic at edge «{}».".format( edge ) )
            
            closed_set.add( edge )
            
            if edge.left is not origin:
                to_flip.append( edge )
                destination_node = edge.left
            else:
                destination_node = edge.right
            
            if not node_filter( destination_node ):
                continue
            
            for destination_edge in destination_node.edges:
                if destination_edge is not edge:
                    if edge_filter( destination_edge ):
                        open_set.append( (destination_node, destination_edge) )
        
        for edge in to_flip:
            edge.flip()
    
    
    def copy_into( self, target_graph: MGraph ) -> "MNode":
        """
        Copies the node (but not the edges!)
        """
        warnings.warn( "deprecated, use :method:`__init__` instead.", DeprecationWarning )
        return MNode( target_graph, self.data, uid = self.__uid )
    
    
    @property
    def uid( self ) -> int:
        """
        A unique identifier on the node (by default a GUID). 
        """
        return self.__uid
    
    
    def get_session_id( self ):
        if self.__session_id is None:
            global _session_ids
            _session_ids += 1
            self.__session_id = _session_ids
        
        return self.__session_id
    
    
    def __repr__( self ):
        if self.data is None or not str( self.data ):
            return "№" + str( self.get_session_id() )
        else:
            return str( self.data ) if self.data is not None else ""
    
    
    def remove_node_safely( self ):
        """
        Removes this node from the graph, but any edges it had will be reassigned between the current relations.
        """
        for parent in self.parents:
            for child in self.children:
                parent.try_add_edge_to( child )
        
        self.remove_node()
    
    
    def remove_node( self ) -> None:
        """
        Removes this node from the graph.
        
        Associated edges are also removed.
        """
        while self.edges:
            for x in self.edges:
                x.remove_edge()
                break
        
        self.graph.nodes._unregister( self, self.uid, self.data )
    
    
    def follow( self, **kwargs ) -> FollowParams:
        return self.graph.follow( FollowParams( start = self, **kwargs ) )


class MEdge:
    """
    Represents an edge of an :class:`MGraph`
    """
    
    
    def __init__( self, left: MNode, right: MNode, *, data: Optional[object] = None ):
        """
        CONSTRUCTOR
        Constructing the edge automatically adds it to the graph.
        For clarity, use :method:`MGraph.add_edge` or :method:`MNode.add_edge_to` instead.
        
        :param left:      The left node (arbitrary for undirected graphs, "source" for directed graphs)
        :param right:     The right node (arbitrary for undirected graphs, "destination" for directed graphs)
        """
        assert isinstance( left, MNode )
        assert isinstance( right, MNode )
        
        if left.graph is not right.graph:
            raise ValueError( "Cannot create an edge between two nodes in different graphs." )
        
        if left is right:
            raise ValueError( "Cannot create an edge to the same node." )
        
        if right in left.edges or left in right.edges:
            raise EdgeExistsError( "Cannot add an edge from node to node because these nodes already share an edge." )
        
        self._graph = left.graph
        self._left = left
        self._right = right
        self.data = data
        
        self.__register()
    
    
    def cut_nodes( self ) -> Tuple[Set[MNode], Set[MNode]]:
        """
        Cuts the edge and returns the set of nodes on each half.
        """
        left = set( self.graph.follow( start = self.left, edge_filter = lambda x: x is not self ).visited_nodes )
        right = set( self.graph.nodes ) - left
        return left, right
    
    
    @property
    def graph( self ) -> MGraph:
        """
        Obtains the graph this edge is situated within.
        """
        return self.left.graph
    
    
    def flip( self ):
        """
        Flips the direction of this edge.
        
        !Warning: Flip affects the lookup tables in the graph that contains the edge!
        
        """
        self.__deregister()
        
        left = self._left
        self._left = self.right
        self._right = left
        
        self.__register()
    
    
    def __register( self ):
        self.left.edges._register_outgoing( self )
        self.right.edges._register_incoming( self )
        self.left.graph.edges._register( self )
    
    
    def __deregister( self ):
        self.left.edges._deregister_outgoing( self )
        self.right.edges._deregister_incoming( self )
        self.left.graph.edges._deregister( self )
    
    
    def copy_into( self, target_graph: MGraph ) -> Optional["MEdge"]:
        """
        Copies this edge into the target graph.
        
        If the same nodes do not exist in the target graph, no edge is created and the function returns `None`.
        """
        warnings.warn( "deprecated, use :method:`__init__` instead.", DeprecationWarning )
        left = target_graph.find_node( self._left.uid )
        
        if left is None:
            return None
        
        right = target_graph.find_node( self._right.uid )
        
        if right is None:
            return None
        
        new_edge = MEdge( left, right )
        return new_edge
    
    
    def remove_edge( self ) -> None:
        """
        Removes this edge from the graph.
        The edge should not be used after calling this function.
        """
        self.__deregister()
    
    
    def __repr__( self ) -> str:
        """
        OVERRIDE
        """
        return "{}-->{}".format( self._left, self._right )
    
    
    @property
    def left( self ) -> MNode:
        """
        Returns the left ("incoming"/"origin" node in directed graphs) endpoint.
        """
        return self._left
    
    
    def follow_left( self ):
        return self.graph.follow( FollowParams( start = self.left, edge_filter = lambda x: x is not self ) ).visited_nodes
    
    
    def follow_right( self ):
        return self.graph.follow( FollowParams( start = self.right, edge_filter = lambda x: x is not self ) ).visited_nodes
    
    
    @property
    def right( self ) -> MNode:
        """
        Returns the right ("outgoing"/"destination" node in directed graphs) endpoint.
        """
        return self._right
    
    
    def opposite( self, node: MNode ) -> MNode:
        """
        Returns the endpoint opposite the one specified.
        """
        if self._left is node:
            return self._right
        elif self._right is node:
            return self._left
        else:
            raise KeyError( "Cannot find opposite side to '{}' because that isn't part of this edge '{}'.".format( node, self ) )
    
    
    def iter_a( self ) -> Set[MNode]:
        """
        Returns a set containing all nodes to the left.
        """
        return set( self._graph.follow( FollowParams( start = self._left, node_filter = lambda x: x is not self._right ) ).visited_nodes )
    
    
    def iter_b( self ) -> Set[MNode]:
        """
        Returns a set containing all nodes to the right.
        """
        return set( self._graph.follow( FollowParams( start = self._right, node_filter = lambda x: x is not self._left ) ).visited_nodes )
    
    
    def ensure( self, left: "MNode" = None, right: "MNode" = None ) -> bool:
        """
        Ensures the edge goes from :param:`left` to :param:`right`, calling `flip` if necessary.
        See :method:`inverts` and :method:`flip`.
        
        :param left:        Left node (`None` for wildcard). 
        :param right:       Right node (`None` for wildcard). 
        """
        if self.inverts( left, right ):
            self.flip()
            return True
        
        return False
    
    
    def inverts( self, left: "MNode" = None, right: "MNode" = None ) -> bool:
        """
        Returns `True` if the edge runs in the opposite direction from :param:`left` to :param:`right`.
        
        Accepts one wildcard parameter but both :param:`left` and :param:`right` cannot be wildcards. 
        
        :param left:        Left node (Must be an end-point of this edge, or `None` for wildcard). 
        :param right:       Right node (Must be an end-point of this edge, or `None` for wildcard). 
        """
        if left is None:
            if right is None:
                raise ValueError( "Both :param:`left` and :param:`right` cannot be `None` when calling `ensure` on edge «{}».".format( self ) )
            
            if self.right is not right:
                if self.left is not right:
                    raise ValueError( "param:`right` specifies a node «{}» that is not an endpoint of the edge «{}».".format( right, self ) )
                
                return True
            
            return False
        
        if self.left is not left:
            if self.right is not left:
                raise ValueError( "param:`left` specifies a node «{}» that is not an endpoint of the edge «{}».".format( left, self ) )
            
            if right is not None and right is not self.left:
                raise ValueError( "param:`right` specifies a node «{}» that is not an endpoint of the edge «{}».".format( right, self ) )
            
            return True
        
        return False


class Split:
    """
    Defines an edge in a tree as a "split".
    """
    
    
    def __init__( self, inside: FrozenSet[T], outside: FrozenSet[T] ):
        """
        CONSTRUCTOR
        :param inside:      Nodes inside the edge 
        :param outside:     Nodes outside the edge 
        """
        self.inside: FrozenSet[T] = inside
        self.outside: FrozenSet[T] = outside
        self.all = frozenset( itertools.chain( self.inside, self.outside ) )
    
    
    def intersection( self, other: AbstractSet[T] ) -> "Split":
        """
        Returns a split that encompasses the intersection of this split and an `other`.
        """
        return Split( frozenset( self.inside.intersection( other ) ),
                      frozenset( self.outside.intersection( other ) ) )
    
    
    def is_redundant( self ) -> bool:
        """
        A split is bad if it has no nodes on one side of the edge.
        """
        return not self.inside or not self.outside
    
    
    def __str__( self ):
        """
        OVERRIDE 
        """
        return self.to_string()
        
    
    def to_ansi_string( self ):
        r = []
        
        for x in sorted( self.all, key = str ):
            if x in self.inside:
                r.append( ansi.FORE_GREEN + str( x ) + ansi.FORE_RESET )
            else:
                r.append( ansi.FORE_RED + str( x ) + ansi.FORE_RESET )
        
        return "·".join( r ) 
    
    
    def to_string( self ):
        """
        Converts the split to a string.
        Unlike `str` this is formatted for an arbitrary display and does not use ANSI colours.
        """
        if len( self.inside ) < len( self.outside ):
            return string_helper.format_array( self.inside, sort = True ) + " ¦ *"
        else:
            return string_helper.format_array( self.outside, sort = True ) + " ¦ *"
    
    
    @property
    def is_empty( self ):
        """
        A split is empty if it has no inside nodes.
        TODO: Is this a bad use case of is_redundant?
        """
        return len( self.inside ) == 0
    
    
    def __len__( self ):
        """
        Number of inside nodes.
        """
        return len( self.inside )
    
    
    def __hash__( self ):
        """
        OVERRIDE
        Hash of the split. See `__eq__`.
        """
        return hash( (self.inside, self.outside) )
    
    
    def __eq__( self, other ):
        """
        OVERRIDE
        Splits are equal if they share the same inside and outside nodes.
        """
        return isinstance( other, Split ) and self.inside == other.inside and self.outside == other.outside
