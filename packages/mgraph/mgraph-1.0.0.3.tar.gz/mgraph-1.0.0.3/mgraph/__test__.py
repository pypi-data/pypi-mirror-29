"""
Test suite for MGraph library
"""

import unittest

from mgraph import MGraph, MNode, FollowParams, exporting, EDirection, analysing, importing
from mgraph.graphing import EGraphFormat, MEdge
from mhelper import ByRef


class MGraphTestCases( unittest.TestCase ):
    def test_mgraph( self ):
        root_ref = ByRef[MNode]( None )
        ####################
        #             F  G #
        #              \/  #
        # A  B      E  /   #
        #  \/        \/    #
        #   \  C  D  /     #
        #    \/    \/      #
        #     \    /       #
        #      \  /        #
        #       \/         #
        ####################
        # Import (newick)
        NEWICK = "(((A,B)ab,C)abc,(D,(E,(F,G)fg)efg)defg)abcdefg;"
        g: MGraph = importing.import_newick( NEWICK, root_ref = root_ref )
        self.assertEqual( root_ref.value.data, "abcdefg" )
        
        # Structure test 
        newick = exporting.export_newick( g )
        self.assertEqual( newick, NEWICK )
        
        # Export (formatting)
        newick = exporting.export_newick( g, fnode = "<__len__()>" )
        self.assertEqual( newick, "(((1,1)2,1)3,(1,(1,(1,1)2)3)4)7;" )
        
        # Relationships
        for x in root_ref.value.children:
            self.assertIn( x.data, ("abc", "defg") )
        
        a: MNode = g.nodes["A"]
        b: MNode = g.nodes["B"]
        ab: MNode = g.nodes["ab"]
        a.edges.by_node( ab ).left.edges.by_node( b )
        
        # TEST: find_common_ancestor
        p = analysing.find_common_ancestor( g,
                                            lambda x: x.data in ("E", "F", "G") )
        self.assertEqual( p, g.nodes.by_data( "efg" ) )
        
        # TEST: find_common_ancestor_paths
        p = analysing.find_common_ancestor_paths( g,
                                                  lambda x: x.data in ("E", "F", "G") )
        self.__assert_mrca( p, "E,efg|F,fg,efg|G,fg,efg" )
        
        p = analysing.find_common_ancestor_paths( g,
                                                  lambda x: x.data in ("E", "F", "G", "A") )
        self.__assert_mrca( p, "A,ab,abc,abcdefg|E,efg,defg,abcdefg|F,fg,efg,defg,abcdefg|G,fg,efg,defg,abcdefg" )
        
        p = analysing.find_common_ancestor_paths( g,
                                                  lambda x: x.data in ("E", "F", "G", "A", "abcdefg") )
        self.__assert_mrca( p, "A,ab,abc,abcdefg|E,efg,defg,abcdefg|F,fg,efg,defg,abcdefg|G,fg,efg,defg,abcdefg|abcdefg" )
        
        # TEST: find_shortest_path
        # normal
        p = analysing.find_shortest_path( g,
                                          g.nodes["C"],
                                          g.nodes["E"],
                                          direction = EDirection.BOTH )
        self.assertEqual( ",".join( x.data for x in p ), "C,abc,abcdefg,defg,efg,E" )
        
        # with predicate
        p = analysing.find_shortest_path( g,
                                          lambda x: x.data in ("C", "A"),
                                          lambda x: x.data in ("E", "G"),
                                          direction = EDirection.BOTH )
        self.assertEqual( ",".join( x.data for x in p ), "C,abc,abcdefg,defg,efg,E" )
        
        # TEST: Follow
        vn = set( x.data for x in g.follow( FollowParams( start = g.nodes.by_data( "abc" ) ) ).visited_nodes )
        self.assertSetEqual( vn, { "abc", "ab", "A", "B", "C", "abcdefg", "defg", "D", "efg", "E", "fg", "F", "G" } )
        
        # TEST: Follow with direction
        vn = set( x.data for x in g.follow( FollowParams( start = g.nodes.by_data( "abc" ), direction = EDirection.OUTGOING ) ).visited_nodes )
        self.assertSetEqual( vn, { "abc", "ab", "A", "B", "C" } )
        
        # TEST: follow with node filter
        f = g.follow( FollowParams( start = g.nodes["A"], node_filter = lambda x: x.data not in ("C", "efg") ) )
        self.assertSetEqual( set( x.data for x in f.visited_nodes ), { "A", "B", "ab", "abc", "abcdefg", "D", "defg" } )
        
        # TEST: follow with edge filter
        f = g.follow( FollowParams( start = g.nodes["A"], edge_filter = lambda x: x.right.data not in ("C", "efg") ) )
        self.assertSetEqual( set( x.data for x in f.visited_nodes ), { "A", "B", "ab", "abc", "abcdefg", "D", "defg" } )
        
        # TEST: import/export
        _ = exporting.export_ancestry( g )
        
        _ = exporting.export_ascii( g )
        
        t = exporting.export_compact( g )
        self.assert_graphs_equal( g, importing.import_compact( t ) )
        
        t = exporting.export_edgelist( g )
        self.assert_graphs_equal( g, importing.import_edgelist( t ) )
        
        t = exporting.export_ete( g )
        self.assert_graphs_equal( g, importing.import_ete( t ) )
        
        t = exporting.export_newick( g )
        self.assert_graphs_equal( g, importing.import_newick( t ) )
        
        _ = exporting.export_nodelist( g )
        
        t = exporting.export_splits( g )
        i = importing.import_splits( t )
        self.__name_clades( i )
        self.assert_graphs_equal( g, i )
        
        _ = exporting.export_string( g, EGraphFormat.ASCII )
        
        _ = exporting.export_vis_js( g )
        
        # TEST: find_isolation_point
        ip = analysing.find_isolation_point( g,
                                             lambda x: x.data in { "A", "B", "C" },
                                             lambda x: x.data in { "abcdefg" } )
        
        self.assertEqual( ip.internal_node.data, "abc" )
        self.assertEqual( ip.external_node.data, "abcdefg" )
        
        # TEST: Make root
        c = g.copy()
        r = c.nodes["abcdefg"]
        e = c.nodes["E"]
        e.make_root()
        self.assertTrue(e.is_root)
        self.assertFalse(r.is_root)
        self.assertEqual(exporting.export_newick(c), "(((F,G)fg,(D,(((A,B)ab,C)abc)abcdefg)defg)efg)E;")
        
        # Appending
        f = g.nodes["F"]
        f.add_child( "X" )
        y = g.add_node( "Y" )
        f.add_edge_to( y )
        
        newick = exporting.export_newick( g )
        self.assertEqual( newick, "(((A,B)ab,C)abc,(D,(E,((X,Y)F,G)fg)efg)defg)abcdefg;" )
        
        # Copying (subset)
        c = g.copy( nodes = lambda x: x.data in ["A", "B", "C", "ab", "abc"] )
        
        newick = exporting.export_newick( c )
        self.assertEqual( newick, "((A,B)ab,C)abc;" )
    
    
    def __name_clades( self, g: MGraph ):
        clades = list( g.nodes.clades )
        
        for clade in clades:
            clade.data = ""
        
        for clade in clades:
            n = "".join( desc.data for desc in clade.list_descendants() if desc.is_leaf )
            n = "".join( sorted( n ) )
            clade.data = n.lower()
    
    
    def __assert_mrca( self, mrcas, eq ):
        mrcas = sorted( mrcas, key = lambda x: str( x[-1] ) )
        mrcas = [",".join( str( y ) for y in reversed( x ) ) for x in mrcas]
        mrcas = "|".join( mrcas )
        self.assertEqual( mrcas, eq )
    
    
    def assert_graphs_equal( self, a_graph: MGraph, b_graph: MGraph ):
        try:
            self.do_assert_graphs_equal( a_graph, b_graph )
        except Exception:
            raise
    
    
    def do_assert_graphs_equal( self, a_graph: MGraph, b_graph: MGraph ):
        self.assertSetEqual( set( x.data for x in a_graph.nodes ), set( x.data for x in b_graph.nodes ) )
        
        for a_node in a_graph:
            b_node = None
            
            for b_node_iter in b_graph:
                if b_node_iter.data == a_node.data:
                    if b_node is not None:
                        raise ValueError( "Multiple nodes." )
                    
                    b_node = b_node_iter
            
            if b_node is None:
                raise ValueError( "No equivalent node." )
        
        self.assertEqual( len( a_graph.edges ), len( b_graph.edges ) )
        
        for a_edge in a_graph.edges:
            assert isinstance( a_edge, MEdge )
            b_edge = None
            
            for b_edge_iter in b_graph.edges:
                assert isinstance( b_edge_iter, MEdge )
                
                if b_edge_iter.left.data == a_edge.left.data and b_edge_iter.right.data == a_edge.right.data:
                    if b_edge is not None:
                        raise ValueError( "Multiple edges." )
                    
                    b_edge = b_edge_iter
            
            if b_edge is None:
                raise ValueError( "No equivalent edge." )


if __name__ == '__main__':
    unittest.main()
