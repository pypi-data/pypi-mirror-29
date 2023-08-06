from typing import Dict, List, Optional, Set, Tuple, TypeVar, Union, cast

from mgraph.graphing import DEdgePredicate, DNodePredicate, EDirection, IsolationError, IsolationPoint, MEdge, MGraph, MNode, UNodePredicate, UEdgePredicate, FollowParams
from mhelper import ComponentFinder, Logger, NOT_PROVIDED, NotFoundError, ansi, array_helper, string_helper


_LOG = Logger( "isolate", False )

T = TypeVar( "T" )


def count_nodes( graph: MGraph, predicate: UNodePredicate ) -> int:
    """
    Returns the number of matching nodes.
    """
    predicate = realise_node_predicate( predicate )
    return sum( 1 for x in graph.nodes if predicate( x ) )


def find_shortest_path( graph: MGraph, start: UNodePredicate, end: UNodePredicate, filter: UNodePredicate = None, direction = EDirection.BOTH ) -> List["MNode"]:
    """
    Obtains the shortest path between two nodes.
    
    :param graph:           Graph
    :param start:           Start of path 
    :param end:             End of path  
    :param filter:          Filter on nodes 
    :param direction:       Direction to follow edges 
    :return:                Path, as a list of elements from `start` to `end`.
    :except NotFoundError:  No such path exists 
    """
    start = realise_node_predicate_as_set( graph, start )
    end = realise_node_predicate( end )
    
    # If we are already at the end that is fine
    for x in start:
        if end( x ):
            return [x]
    
    open: List[List[MNode]] = [[x] for x in start]
    closed = set()
    
    filter = realise_node_predicate( filter )
    
    while open:
        cur: List[MNode] = open.pop( 0 )
        nod: MNode = cur[-1]
        closed.add( nod )
        
        for edge in nod.edges.by_direction( direction ):
            oth = edge.opposite( nod )
            
            if end( oth ):
                return cur + [oth]
            
            if oth not in closed and filter( oth ):
                open.append( cur + [oth] )
    
    raise NotFoundError( "There is no «{}» path between nodes «{}» and «{}» using the filter «{}».".format( direction, start, end, filter ) )


def find_common_ancestor( graph: MGraph, filter: UNodePredicate, direction: EDirection = EDirection.INCOMING, default = NOT_PROVIDED ) -> "MNode":
    """
    Convenience function that returns the MRCA from `find_common_ancestor_paths`.
    """
    try:
        p = find_common_ancestor_paths( graph, filter, direction )
    except NotFoundError:
        if default is not NOT_PROVIDED:
            return default
        else:
            raise
    
    return p[0][0]


def find_common_ancestor_paths( graph: MGraph, filter: UNodePredicate, direction: EDirection = EDirection.INCOMING ) -> List[List["MNode"]]:
    """
    Finds the last common ancestor of the nodes predicated by the specified filter.
        
    :param graph:       Target graph.
    :param filter:      Predicate over which to filter nodes for inclusion in the result set.
    :param direction:   Ancestor direction
                            INCOMING  = against edges (the default, finds the MRCA on a rooted graph)
                            BOTH      = root independent (finds the closest node)
                            OUTGOING  = with edges (finds the shortest path)
    :return: A list of lists, each list has the MRCA as the first element, and the subsequent elements
             of that list describing the path from the MRCA to the `filter` nodes.
             
    :except ValueError: Filter excludes all nodes
    :except NotFoundError: Nodes do not share an MRCA 
    """
    query: List[Tuple[MNode,
                      List[MNode],
                      Dict[MNode,
                           Optional[MNode]]]] = [(node,
                                                  [node],
                                                  { node: None }) for node in realise_node_predicate_as_set( graph, filter )]
    all_visited = [x[2] for x in query]
    
    if not query:
        raise ValueError( "The specified filter («{}») excludes all nodes in the graph («{}»).".format( filter,
                                                                                                        graph.to_compact() ) )
    
    if len( query ) == 1:
        return [[query[0][0]]]
    
    while True:
        graph_complete = True
        
        for node, unvisited_list, visited_set in query:
            if unvisited_list:
                next = unvisited_list.pop()
                graph_complete = False
                
                for x in next.edges.list_nodes( direction ):
                    if x not in visited_set:
                        visited_set[x] = next
                        unvisited_list.append( x )
        
        if graph_complete:
            msg = "The nodes («{}») do not share a common ancestor in the graph («{}»)."
            raise NotFoundError( msg.format( string_helper.format_array( x[0] for x in query ),
                                             graph.to_compact() ) )
        
        intersection = set()
        
        for i, x in enumerate( all_visited ):
            if i == 0:
                intersection.update( x )
            else:
                for y in tuple( intersection ):
                    if y not in x:
                        intersection.remove( y )
        
        if intersection:
            if len( intersection ) != 1:
                msg = "The nodes («{}») share multiple common ancestors («{}») in the graph («{}»)."
                raise ValueError( msg.format( string_helper.format_array( x[0] for x in query ),
                                              string_helper.format_array( intersection ),
                                              graph.to_compact() ) )
            
            first = array_helper.single_or_error( intersection )
            
            paths = []
            
            for _, _, visited_set in query:
                l = []
                paths.append( l )
                
                next = first
                
                while next is not None:
                    l.append( next )
                    next = visited_set[next]
            
            return paths


def find_isolation_point( graph: MGraph, is_inside: UNodePredicate, is_outside: UNodePredicate ) -> IsolationPoint:
    """
    Convenience function that calls `find_isolation_points`, returning the resultant point or raising an error.
    
    :except IsolationError: Points are not isolated.
    """
    is_inside = realise_node_predicate_as_set( graph, is_inside )
    is_outside = realise_node_predicate_as_set( graph, is_outside )
    
    points = find_isolation_points( graph, is_inside, is_outside )
    
    if len( points ) != 1:
        msg = "Cannot extract an isolation point from the graph because the inside set ({}) is not isolated from the outside set ({})."
        raise IsolationError( msg.format( is_inside, is_outside ), is_inside, is_outside )
    
    return points[0]


def find_isolation_points( graph: MGraph, is_inside: UNodePredicate, is_outside: UNodePredicate ) -> List[IsolationPoint]:
    """
    Finds the points on the graph that separate the specified `inside` nodes from the `outside` nodes.
    
          --------I
      ----X1
      |   --------I
      |
    --X2
      |
      |   --------O
      ----X3
          --------O
         
    
    Nodes (X) not in the `inside` (I) and `outside` (O) sets are can be either inside or outside the isolated subgraph, however this
    algorithm will attempt to keep as many as possible outside, so in the diagram about, the point that isolates I from O is X1. 
    
    Ideally, there will just be one point in the results list, but if the inside points are scattered, more than one point will be
    returned, e.g. X1 and X3 separate I from O:
    
          --------I
      ----X1
      |   --------I
      |
    --X2
      |           --------I
      |   --------X3
      ----X4      --------I
          |
          --------O
     
     
    :param graph:         Target graph.
    :param is_outside:   A delegate expression yielding `True` for nodes outside the set to be separated, and `False` for all other nodes. 
    :param is_inside:    A delegate expression yielding `True` for nodes inside the set to be separated,  and `False` for all other nodes. 
    :return:          A list of `IsolationPoint` detailing the isolation points. 
    """
    # Iterate over all the edges to make a list of `candidate` edges
    # - those separating INSIDE from OUTSIDE
    candidates: List[IsolationPoint] = []
    
    is_inside = realise_node_predicate_as_set( graph, is_inside )
    is_outside = realise_node_predicate_as_set( graph, is_outside )
    
    if not is_inside:
        raise ValueError( "Cannot find isolation points because there are no interior nodes. Interior = {}. Exterior = {}.".format( string_helper.format_array( is_inside ), string_helper.format_array( is_outside ) ) )
    
    if not is_outside:
        raise ValueError( "Cannot find isolation points because there are no exterior nodes. Interior = {}. Exterior = {}.".format( string_helper.format_array( is_inside ), string_helper.format_array( is_outside ) ) )
    
    all_nodes = set( graph )
    
    for edge in graph.edges:
        _LOG( "~~~~ {} ~~~~", edge )
        left_nodes = set( graph.follow( FollowParams( start = edge.left, edge_filter = lambda x: x is not edge ) ).visited_nodes )
        right_nodes = all_nodes - left_nodes
        
        for node, inside_nodes, outside_nodes in ((edge.left, left_nodes, right_nodes), (edge.right, right_nodes, left_nodes)):
            _LOG( "WANT INSIDE:  {}", is_inside )
            _LOG( "WANT OUTSIDE: {}", is_outside )
            _LOG( "INSIDE:       {}", inside_nodes )
            _LOG( "OUTSIDE:      {}", outside_nodes )
            
            if not __check_inside_outside( inside_nodes, is_inside, is_outside, outside_nodes ):
                continue
            
            pure_inside_nodes = set( x for x in inside_nodes if x in is_inside )
            pure_outside_nodes = set( x for x in outside_nodes if x in is_outside )
            
            candidates.append( IsolationPoint( edge, node, edge.opposite( node ), pure_inside_nodes, pure_outside_nodes, inside_nodes, outside_nodes ) )
    
    # Our candidates overlap, so remove the redundant ones
    drop_candidates = []
    
    for candidate_1 in candidates:
        for candidate_2 in candidates:
            if candidate_1 is candidate_2:
                continue
            
            is_subset = candidate_1.pure_inside_nodes.issubset( candidate_2.pure_inside_nodes )
            
            # If the candidates encompass different sequences don't bother
            if not is_subset:
                continue
            
            # Any candidates that are a _strict_ subset of another can be dropped
            if len( candidate_1.pure_inside_nodes ) < len( candidate_2.pure_inside_nodes ):
                drop_candidates.append( candidate_1 )
                break
            
            # Any candidates equal to another, but have a greater number of cladistic nodes, can be dropped
            if len( candidate_1.all_inside_nodes ) > len( candidate_2.all_inside_nodes ):
                drop_candidates.append( candidate_1 )
                break
    
    for candidate in drop_candidates:
        candidates.remove( candidate )
    
    return candidates


def __check_inside_outside( inside_nodes: Set["MNode"],
                            is_inside: Set["MNode"],
                            is_outside: Set["MNode"],
                            outside_nodes: Set["MNode"]
                            ) -> bool:
    for x in inside_nodes:
        if x in is_outside:
            _LOG( ansi.FORE_RED + "REJECTED" + ansi.FORE_RESET + " - OUTSIDE NODE IS INSIDE: {}", x )
            return False
    
    for x in outside_nodes:
        if x in is_inside:
            _LOG( ansi.FORE_RED + "REJECTED" + ansi.FORE_RESET + " - INSIDE NODE IS OUTSIDE: {}", x )
            return False
    
    _LOG( ansi.FORE_GREEN + "ACCEPTED" + ansi.FORE_RESET )
    return True


def realise_node_predicate_as_set( graph: MGraph, node_filter: UNodePredicate ) -> Set["MNode"]:
    if node_filter is None:
        return set( graph.nodes )
    elif isinstance( node_filter, MNode ):
        return { node_filter }
    elif isinstance( node_filter, set ):
        return node_filter
    elif isinstance( node_filter, list ) or isinstance( node_filter, tuple ):
        return set( node_filter )
    else:
        return set( node for node in graph if node_filter( node ) )


def realise_predicate( entity_filter: Union[UEdgePredicate, UNodePredicate], type_: type ) -> Union[DEdgePredicate, DNodePredicate]:
    if entity_filter is None:
        return lambda _: True
    elif isinstance( entity_filter, type_ ):
        return (lambda y: lambda x: x is y)( entity_filter )
    elif isinstance( entity_filter, set ):
        return (lambda y: lambda x: x in y)( entity_filter )
    elif isinstance( entity_filter, list ) or isinstance( entity_filter, tuple ):
        return (lambda y: lambda x: x in y)( set( entity_filter ) )
    else:
        return entity_filter


def realise_edge_predicate( edge_filter: UEdgePredicate ) -> DEdgePredicate:
    return realise_predicate( edge_filter, MEdge )


def realise_node_predicate( node_filter: UNodePredicate ) -> DNodePredicate:
    return realise_predicate( node_filter, MNode )


def find_connected_components( graph: MGraph ) -> List[List["MNode"]]:
    """
    Calculates and returns the list of connected components.
    """
    cf = ComponentFinder()
    
    for edge in graph.edges:
        cf.join( edge.left, edge.right )
    
    return cast( List[List["MNode"]], cf.tabulate() )
