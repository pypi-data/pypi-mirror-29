from typing import Optional, Sequence, Tuple, Callable, cast, List, Union, Set, Iterable, FrozenSet, TypeVar
import itertools
from os import path
import re
from mhelper import array_helper, SwitchError, file_helper, string_helper

from mgraph.graphing import MGraph, MNode, UNodeToText, DNodeToText, FollowParams, EDirection, DEdgeToText, GraphRecursionError, EGraphFormat, MEdge, DNodePredicate, Split
from mhelper.colours import Colour


T = TypeVar( "T" )
_RX1 = re.compile( "(<[^>]+>)" )


class NodeStyle:
    def __init__( self, node: MNode ):
        self.node = node
        self.label = str( node )
        
        if node.is_leaf:
            self.background = NodeStyle._make_unique_colour( self.label )
            self.shape = 'box'
        elif node.is_root:
            self.background = "#800000"
            self.shape = 'box'
        elif node.num_parents > 1:
            self.background = "#FF0000"
            self.shape = 'star'
        else:
            self.background = "#FFFFFF"
            self.shape = 'ellipse'
        
        self.__foreground = None
    
    
    @property
    def foreground( self ):
        if self.__foreground is None:
            return Colour( self.background ).contrasting_bw().html
        else:
            return self.__foreground
    
    
    @foreground.setter
    def foreground( self, value ):
        self.__foreground = value
    
    
    @staticmethod
    def _make_unique_colour( label: str ):
        import hashlib
        hash_object = hashlib.md5( label.encode() )
        return (Colour( hash_object.hexdigest()[0:8] ) // 2).html


DNodeStyler = Callable[[NodeStyle], None]


def realise_node_to_text( fnode: UNodeToText ) -> DNodeToText:
    """
    Given a string format or callable, returns a callable.
    
    :param fnode: Either:
                  A callable that takes a single `MNode` argument and returns a string.
                        e.g. `lambda node: "My node is called {} and has {} children.".format( node.data.name, node.num_children )`.
                  or
                  A format string that uses `<xxx.yyy.zzz>` to denote dynamic values of the `data` property and `<.xxx.yyy.zzz>` to denote dynamic values of the node.
                        e.g. `"my node is called <name> and has <.num_children> children."`
                  Other values are undefined, if `fname` does not derive from `str` it will be assumed to be a callable.
    :return:    A callable that takes a single `MNode` argument and returns a string. 
    """
    if fnode is None:
        return cast( DNodeToText, str )
    elif isinstance( fnode, str ):
        if fnode == "":
            return cast( DNodeToText, str )
        
        
        def __fn( node: MNode ):
            r = []
            
            for element in _RX1.split( fnode ):
                if element.startswith( "<" ):
                    element = element[1:-1]
                    props = element.split( "." )
                    
                    if not props[0]:
                        t = node
                        del props[0]
                    else:
                        t = node.data
                    
                    for prop in props:
                        if prop.endswith( "()" ):
                            prop = prop[:-2]
                            call = True
                        else:
                            call = False
                        
                        t = getattr( t, prop )
                        
                        if call:
                            t = t()
                    
                    r.append( str( t ) )
                else:
                    r.append( element )
            
            return "".join( r )
        
        
        return __fn
    else:
        return fnode


def export_vis_js( graph: Union[MGraph, Sequence[MGraph], Sequence[Tuple[str, MGraph]]],
                   *,
                   visjs_path: str = None,
                   fnode: UNodeToText = None,
                   inline_title: bool = False,
                   title: str = None,
                   rooted = True,
                   node_styler: DNodeStyler = None ) -> str:
    """
    Creates a vis.js html file, to view a graph.
     
    :param graph:               A graph, or a sequence of one or more graphs and names.
    :param visjs_path:          Path to Vis.js. Probably mandatory for meaningful output.
    :param node_styler:         How to style the nodes
    :param fnode:               String describing how the nodes are formatted.
                                See `specify_graph_help` for details.
    :param title:               The title of the page. When `None` a default title is suggested.
                                Note that the title will always show in the title bar, even if `inline_title` is `False`.
    :param inline_title:        When `True` an inline heading is added to the page. 
    :param rooted:              Draw a rooted graph.
    :return:                    A string containing the HTML. 
    """
    # Parameter handling
    fnode = realise_node_to_text( fnode )
    
    if isinstance( graph, MGraph ):
        graph = [graph]
    
    graphs: List[Tuple[str, MGraph]] = [("MGraph", x) if isinstance( x, MGraph ) else x for x in graph]
    
    # Page heading
    if inline_title:
        prefix = "<p><b>$(TITLE)</b></p><p>$(COMMENT)</p>"
    else:
        prefix = ""
    
    # Page title
    multiple_graphs = len( graphs ) != 1
    
    if not title:
        if not multiple_graphs:
            title = graphs[0][0] or "Untitled graph"
    
    # Get graph information
    mgraphs = [x[1] for x in graphs]
    all_nodes = [λnode for λgraph in mgraphs for λnode in λgraph.nodes]
    all_edges = [λedge for λgraph in mgraphs for λedge in λgraph.edges]
    nodes = array_helper.create_index_lookup( itertools.chain( all_nodes, graphs ) )
    # Add the nodes
    node_list = []
    
    for node, node_id in nodes.items():
        if isinstance( node, MNode ):
            style = NodeStyle( node )
            
            if fnode:
                style.label = fnode( node )
            
            if node_styler:
                node_styler( style )
            
            node_list.append( "{{shape:'{}', id: {}, label: '{}', color: '{}', font:{{color: '{}'}} }},".format( style.shape,
                                                                                                                 node_id,
                                                                                                                 style.label,
                                                                                                                 style.background,
                                                                                                                 style.foreground ) )
        elif isinstance( node, tuple ):
            # Labels...
            name, graph = node
            
            if multiple_graphs:
                node_list.append( "{{shape:'text', id: {}, label: '{}', color: '#FFFFC0', font:{{size:32}}}},".format( node_id, name ) )
        else:
            # Something else...
            raise SwitchError( "node", node, instance = True )
    
    # Add the edges
    edge_list = []
    
    for edge in all_edges:
        if edge.right.num_parents > 1:
            colour = "#FF0000"
        else:
            colour = "#000000"
        
        edge_list.append( "{{from: {}, to: {}, arrows:'to', color:{{color:'{}'}}}},".format( nodes[edge.left],
                                                                                             nodes[edge.right],
                                                                                             colour ) )
    
    # Fake edges to the labels
    for name_graph in graphs:
        if multiple_graphs:
            node_id_1 = nodes[name_graph[1].any_root]
            node_id_2 = nodes[name_graph]
            edge_list.append( "{{from: {}, to: {}, dashes:'true', color:{{color:'#C0C0C0'}}, smooth:{{enabled:'false'}}}},".format( node_id_1, node_id_2 ) )
    
    # Layout
    if not rooted:
        options = ''
    else:
        # noinspection SpellCheckingInspection
        options = """
        layout:
        {
            hierarchical: 
            { 
                direction: "UD", 
                sortMethod: "directed" 
            }
        },
        physics: 
        {
            hierarchicalRepulsion:
            {
                centralGravity: 0.0,
                springLength: 100,
                springConstant: 0.01,
                nodeDistance: 120,
                damping: 0.09
            },
            maxVelocity: 1,
            solver: 'hierarchicalRepulsion',
            timestep: 0.35,
            stabilization: 
            {
                enabled: true,
                iterations: 1,
                updateInterval: 25
            }
        }"""
    
    # Output the page
    HTML_T = file_helper.read_all_text( path.join( file_helper.get_directory( __file__, ), "vis_js_template.html" ) )
    HTML_T = HTML_T.replace( "$(PREFIX)", prefix )
    HTML_T = HTML_T.replace( "$(TITLE)", title )
    HTML_T = HTML_T.replace( "$(PATH)", path.join( visjs_path or "", "vis/dist/vis.js" ) )
    HTML_T = HTML_T.replace( "$(COMMENT)", "File automatically generated by Groot. Please replace this line with your own description." )
    HTML_T = HTML_T.replace( "$(NODES)", "\n".join( node_list ) )
    HTML_T = HTML_T.replace( "$(EDGES)", "\n".join( edge_list ) )
    HTML_T = HTML_T.replace( "$(OPTIONS)", options )
    return HTML_T


def export_ancestry( graph: MGraph,
                     *,
                     fnode: UNodeToText = None ):
    """
    Converts the graph to a node list, with included ancestry information.
    :param graph:   Graph to export
    :param fnode:   Formatter for node names, see `to_string`.
    """
    fnode = realise_node_to_text( fnode )
    r = []
    
    for node in graph.nodes:
        if node.num_parents == 0:
            r.append( fnode( node ) )
        elif node.num_parents == 1:
            r.append( "{} ➡ {}".format( fnode( node.parent ), fnode( node ) ) )
        else:
            r.append( "({}) ➡ {}".format( string_helper.format_array( (fnode( x ) for x in node.parents), join = "+" ), fnode( node ) ) )
    
    return "\n".join( r )


def export_compact( graph: MGraph ):
    """
    Retrieves a compact string representing the graph.
    Useful for debugging.
    :param graph: Graph to export
    """
    return export_edgelist( graph, fnode = lambda x: str( x ).replace( ",", "_" ).replace( "|", "¦" ), delimiter = ",", line = "|" )


def export_nodelist( graph: MGraph,
                     *,
                     fname: UNodeToText = None ):
    """
    Lists the nodes of the graph, as text.
    :param graph:   Graph to export
    :param fname:   Node name format
    """
    fname = realise_node_to_text( fname )
    r = []
    
    for node in graph:
        r.append( fname( node ) )
    
    return "\n".join( r )


def export_edgelist( graph: MGraph,
                     *,
                     fnode: UNodeToText = str,
                     delimiter: str = ", ",
                     colnames: Tuple[str, str] = None,
                     pad: Union[int, bool] = False,
                     line: str = "\n" ):
    """
    Converts the graph to a textual edge-list.
    
    :param graph:           Graph to export
    :param fnode:           How to name the nodes 
    :param delimiter:       The delimiter to use 
    :param colnames:        Names of the columns, or `None` for no column names.
    :param pad:             Pad node names to this long. If this is `True` the padding will be determined automatically. If this is `False` there will be no padding.
    :param line:            Linebreak character. 
    :return:                Edgelist as a string. 
    """
    fnode = realise_node_to_text( fnode )
    
    if pad is False:
        pad = 0
    elif pad is True:
        pad = 0
        
        for node in graph.nodes:
            pad = max( pad, len( fnode( node ) ) )
    
    r = []
    
    if colnames is not None:
        r.append( "{}{}{}".format( colnames[0].ljust( pad ), delimiter, colnames[1].ljust( pad ) ) )
    
    for edge in graph.edges:
        r.append( "{}{}{}".format( fnode( edge.left ).ljust( pad ), delimiter, fnode( edge.right ).ljust( pad ) ) )
    
    return line.join( sorted( r ) )


def export_ascii( graph: MGraph,
                  *,
                  fnode: UNodeToText = str,
                  direction: EDirection = EDirection.OUTGOING ):
    """
    Shows the graph as ASCII-art (UTF8).
    
    :param graph:           Graph to export
    :param direction:       Direction to follow edges. 
    :param fnode:           How to name the nodes
    """
    fnode = realise_node_to_text( fnode )
    results: List[str] = []
    
    all = set( graph )
    num_roots = 0
    
    while all:
        num_roots += 1
        results.append( "(ROOT {} OF <NUM_ROOTS>)".format( num_roots ) )
        root = __suggest_root( graph, all, direction )
        params = graph.follow( FollowParams( start = root, include_repeats = True, direction = direction ) )
        __remove_touched( all, params.visited_nodes )
        results.extend( x.describe( fnode ) for x in params.visited )
    
    return "\n".join( results ).replace( "<NUM_ROOTS>", str( num_roots ) )


def export_newick( graph: MGraph,
                   *,
                   fnode: UNodeToText = str,
                   direction: EDirection = EDirection.OUTGOING,
                   fedge: Optional[DEdgeToText] = None,
                   internal: bool = True ):
    """
    Converts the graph to a Newick tree (or trees if there are multiple roots).
    
    :param graph:        Graph to export
    :param direction:    Direction to follow edges 
    :param fnode:        How to name the nodes
    :param fedge:        How to name the edges  
    :param internal:     Whether to name internal nodes
    :return:             Newick tree, as a string. 
    """
    all = set( graph )
    r = []
    
    while all:
        root = __suggest_root( graph, all, direction )
        touched = set()
        try:
            r.append( __node_to_newick( root, fnode, fedge, direction, internal, None, touched ) + ";" )
        except GraphRecursionError as ex:
            raise GraphRecursionError( "Cannot convert the graph to Newick because it has loops.", ex.nodes ) from ex
        
        assert touched
        __remove_touched( all, touched )
    
    return "\n".join( r )


def export_ete( graph: MGraph,
                *,
                fnode: UNodeToText = None ):
    """
    Converts the graph to an Ete tree.
    Requires library: `ete`.
    
    :remarks:
    At the time of writing, the Ete code doesn't appear to handle multi-rooted trees
    and therefore Ete's behaviour with non-treelike graphs is undefined. 
    
    :param graph:   Graph to export
    :param fnode:   How to format nodes.
    :return: An arbitrary node from the resulting Ete tree.
    """
    from ete3 import TreeNode
    fnode = realise_node_to_text( fnode )
    
    map = { }
    
    
    def __recurse( m_node: MNode ) -> TreeNode:
        if m_node in map:
            return map[m_node]
        
        e_node = TreeNode( name = fnode( m_node ) )
        map[m_node] = e_node
        
        for m_child in m_node.edges.list_nodes( EDirection.OUTGOING ):
            e_child = __recurse( m_child )
            # noinspection PyTypeChecker
            e_node.add_child( e_child )
        
        return e_node
    
    
    r = None
    
    for node in graph:
        r = __recurse( node )
    
    return r


def export_string( graph: MGraph,
                   format: EGraphFormat,
                   fname: UNodeToText = str ):
    """
    Converts the graph to text.
    Default options are used. Use :function:export_newick, :function:export_ascii, etc. to provide more options.  
    
    :param graph:       Graph to export
    :param format:      Format 
    :param fname:       How to name the nodes 
    :return:            Text
    """
    if format == EGraphFormat.NEWICK:
        return export_newick( graph = graph, fnode = fname )
    elif format == EGraphFormat.NODELIST:
        return export_nodelist( graph = graph, fname = fname )
    elif format == EGraphFormat.ANCESTRY:
        return export_ancestry( graph = graph, fnode = fname )
    elif format == EGraphFormat.ASCII:
        return export_ascii( graph = graph, fnode = fname )
    elif format == EGraphFormat.CSV:
        return export_edgelist( graph = graph, fnode = fname )
    elif format == EGraphFormat.TSV:
        return export_edgelist( graph = graph, fnode = fname, delimiter = "\t" )
    elif format == EGraphFormat.COMPACT:
        return export_compact( graph = graph )
    elif format == EGraphFormat.ETE_ASCII:
        return export_ete( graph = graph, fnode = fname ).get_ascii()
    else:
        raise SwitchError( "format", format )


def __suggest_root( graph: MGraph, subset: Set["MNode"], direction: EDirection ) -> "MNode":
    for node in graph.iter_roots( subset, direction ):
        return node


def __remove_touched( all, touched ):
    for node in touched:
        if node in all:
            all.remove( node )


def __node_to_newick( node: MNode,
                      fnode: UNodeToText,
                      fedge: Optional[DEdgeToText] = None,
                      direction: EDirection = EDirection.OUTGOING,
                      internal: bool = True,
                      origin: Optional[MEdge] = None,
                      touched: Set["MNode"] = None ):
    """
    Resolves this node to Newick.
    This is used by the :func:`mgraph.exporting.export_newick`.
    
    :param node:            Node
    :param internal:        Whether to name internal nodes
    :param fedge:           How to obtain edge names
    :param fnode:           How to obtain node names 
    :param origin:          When set, will not follow to this relation 
    :param direction:       Direction to follow edges
    :param touched:         Set of touched nodes. 
    :return:                Newick string 
    """
    
    #  Parameters
    if touched is None:
        touched = set()
    
    fnode = realise_node_to_text( fnode )
    
    # Loop detection
    if node in touched:
        raise GraphRecursionError( "`__node_to_newick` recurring to same node..", [node] )
    
    touched.add( node )
    
    # Get outgoing edges
    edges = node.edges.by_direction( direction )
    
    if origin in edges:
        edges.remove( origin )
    
    # Name the incoming edge
    if origin is not None and fedge is not None:
        edge_txt = fedge( origin )
        if edge_txt:
            edge_txt = ":" + edge_txt
    else:
        edge_txt = ""
    
    # Lone node, simple format
    if not edges:
        return fnode( node ) + edge_txt
    
    # Concatenate the children
    try:
        children_str = ",".join( __node_to_newick( edge.opposite( node ), fnode = fnode, fedge = fedge, direction = direction, internal = internal, origin = edge, touched = touched ) for edge in edges )
    except GraphRecursionError as ex:
        raise GraphRecursionError( "`__node_to_newick` recurring.", [node] + ex.nodes )
    
    # Format the results
    return "(" + children_str + ")" + (fnode( node ) if internal else "") + edge_txt


def __export_splits_iter( graph: MGraph, filter: DNodePredicate = None, gdata: Callable[[MNode], T] = None ) -> Iterable[Tuple[FrozenSet[T], FrozenSet[T]]]:
    """
    Iterates the set of splits in a graph.
    See :func:`export_splits` for parameter details.
    
    :return:    Iterable of splits (tuple):
                    1. Left set of split (`node.data` where `leaf_definition(node)` is `True`)
                    2. Right set of split 
    """
    if filter is None:
        filter = lambda x: x.is_leaf
    
    if gdata is None:
        gdata = lambda x: x.data
    
    all_sequences = set( gdata( x ) for x in graph if filter( x ) )
    
    for edge in graph.edges:
        left_all = graph.follow( FollowParams( start = edge.left, edge_filter = lambda x: x is not edge ) ).visited_nodes
        left_leaves = set( gdata( x ) for x in left_all if filter( x ) )
        right_leaves = all_sequences - left_leaves
        yield frozenset( left_leaves ), frozenset( right_leaves )


def export_splits( graph: MGraph, *, filter: DNodePredicate = None, gdata: Callable[[MNode], object] = None ) -> Set[Split]:
    """
    Obtains the set of splits in a graph.
    See :class:`Split`.
    
    :param graph:       Graph 
    :param filter:      Definition of a leaf node. `node.is_leaf` by default.
                        ( we _can_ create splits of internal nodes too, we just can't _recreate_ such splits )
    :param gdata:       How to retrieve data from node. `node.data` by default.
                        Note that data must be _unique_, if two nodes share the same `gdata` result then they will be considered equivalent. 
    :return:            Set of splits as :class:`Split` objects. 
    """
    all_splits: Set[Split] = set()
    
    for left_sequences, right_sequences in __export_splits_iter( graph, filter, gdata ):
        all_splits.add( Split( left_sequences, right_sequences ) )
        all_splits.add( Split( right_sequences, left_sequences ) )
    
    return all_splits
