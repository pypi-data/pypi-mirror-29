import random
from typing import Tuple, List, cast, Optional

from faketree.treedata import NodeData
from faketree.workspace import status as status_, CurrentStatus
from intermake import command
from intermake.engine.environment import MCMD
from mgraph import MNode, importing
from mgraph.graphing import EDirection, MEdge
from mhelper import string_helper, ByRef


status: CurrentStatus = status_


class RandomChoiceError( IndexError ):
    pass


@command()
def new():
    """
    Starts a new session.
    The model is cleared, but not parameter settings such as the pool.
    """
    status.reset()


def __count_dashes( text: str ) -> Tuple[str, int]:
    no_dashes = text.lstrip( "-" )
    return no_dashes, len( text ) - len( no_dashes )


@command()
def goto( node: MNode ):
    """
    Selects a particular node so that it may be modified with the `tree` command.
    :param node:    Node to select
    """
    status.selected = node
    
    MCMD.print( "Selected: {}".format( string_helper.format_array( get_path() ) ) )


@command()
def copy( source: MNode, old: str = "", new: str = "" ):
    """
    Copies a tree.
    
    Note:
    Only structure and names are copied.
    The copy will not inherit the original's mutators (if set) or sequences (if created).
    
    :param source:  Source node 
    :param old:     Find in node names 
    :param new:     Replace with in node names 
    """
    source.graph.copy( nodes = source.follow().visited_nodes,
                       target = source.graph,
                       data = lambda old_data: NodeData( cast( str, old_data.name ).replace( old, new ) ) )


@command()
def where():
    """
    Prints the currently selected node.
    """
    MCMD.print( "Selected: {}".format( string_helper.format_array( get_path() ) ) )


@command()
def newick( text: str ) -> MNode:
    """
    Imports a newick string into the graph.
    
    Note:
    Branch lengths are NOT imported since not all mutators can use them.
    These must be set on the mutators themselves.
    
    :param text:  Text to import.
    """
    root_ref = ByRef["MNode"]
    importing.import_newick( text, converter = NodeData, root_ref = root_ref, graph = status.tree )
    return root_ref.value


@command()
def random_node( node: MNode, closed: bool = False, avoid: Optional[List[MNode]] = None ) -> MNode:
    """
    Obtains a random descendant of the specified node.
    
    :param avoid: Don't return these nodes. These nodes don't have to be in the candidate set.
    :param node: Specified node
    :param closed: Closed interval? (exclude `node` from the possibilities).
    :returns: The random node.
    :except RandomChoiceError: No sub-nodes
    """
    nodes = node.follow( direction = EDirection.OUTGOING ).visited_nodes
    
    if not closed:
        nodes.remove( node )
    
    if avoid:
        for x in avoid:
            if x in nodes:
                nodes.remove( x )
    
    if not nodes:
        raise RandomChoiceError( "Cannot choose from an empty set of descendants of «{}».".format( node ) )
    
    return random.choice( nodes )


@command()
def outgroup( nodes: List[MNode], names: List[str] ) -> List["MNode"]:
    """
    Creates an outgroup on a node.
    
    :param nodes:   Root(s) 
    :param names:   Name(s) of outgroup(s) 
    """
    r = []
    
    for node, name in zip( nodes, names ):
        r.append( node.add_child( data = NodeData( name ) ) )
    
    return r


@command()
def random_tree( names: List[str], size = 25, suffix = "a", delimiter = "", outgroup: bool = False ) -> List[MNode]:
    """
    Generates a random tree or trees.
    
    :param outgroup:  Add root outgroups. When true the result will be the outgroups, not the roots.
    :param delimiter: Suffix delimiter.
    :param suffix:    Suffix, `a`, `A`, `0`, `1` or your own list of characters.
    :param names:     Prefix names of the tree nodes. 
    :param size:      Number of iterations.
    """
    results = []
    outgroups = []
    
    for name in names:
        root = status.tree.add_node( data = NodeData( "" ) )
        results.append( root )
        leaves = set()
        leaves.add( root )
        
        if suffix == "a":
            suffix_fn = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".__getitem__
        elif suffix == "A":
            suffix_fn = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".__getitem__
        elif suffix == "0":
            suffix_fn = lambda x: str( x )
        elif suffix == "1":
            suffix_fn = lambda x: str( x + 1 )
        else:
            suffix_fn = suffix.__getitem__
        
        for _ in range( size ):
            # Choose a random leaf
            leaf: MNode = random.choice( list( leaves ) )
            
            # Bifurcate the leaf
            child_1 = leaf.add_child( data = NodeData( "" ) )
            child_2 = leaf.add_child( data = NodeData( "" ) )
            leaves.remove( leaf )
            leaves.add( child_1 )
            leaves.add( child_2 )
        
        if outgroup:
            old_edges = list( root.edges )
            outgroup = root.add_child( data = NodeData( "" ) )
            leaves.add( outgroup )
            outgroups.append( outgroup )
            
            new_root = root.add_child( data = NodeData( "" ) )
            
            for old_edge in old_edges:
                assert isinstance( old_edge, MEdge )
                new_root.add_edge_to( old_edge.right )
                old_edge.remove_edge()
        
        # Name everything
        for i, leaf in enumerate( leaves ):
            suffix_str = suffix_fn( i )
            leaf.data.name = name + suffix_str
            parent = leaf.parent
            
            while parent:
                if not parent.data.name:
                    parent.data.name = name
                
                parent.data.name += delimiter + suffix_str
                parent = parent.parent
        
        root.data.name = name
    
    if outgroup:
        return outgroups
    else:
        return results


def get_path() -> List[MNode]:
    r = []
    
    node = status.selected
    
    while node:
        r.append( node )
        node = node.parent
    
    return list( reversed( r ) )


@command()
def tree( names: List[str] ):
    """
    Adds a node to the graph.
    Specify `-` in the name to indicate ancestry, e.g.
    
    `add root`
    `add -clade1`
    `add --member1`
    `add --member2`
    `add -clade2`
    `add --member3`
    `add --member4`
    
    :param names:    One or more node names.
    """
    for name in names:
        name, dashes = __count_dashes( name )
        
        if dashes == 0:
            new_node = status.tree.add_node( data = NodeData( name ) )
            status.selected = new_node
            MCMD.print( "New root: {}".format( new_node ) )
            continue
        
        path = get_path()
        
        if not path:
            raise ValueError( "Cannot add «{}» - no selected node.".format( name ) )
        
        selected_dashes = len( path )
        
        delta = dashes - selected_dashes + 1
        
        if delta <= 0:
            for i in range( 0, 1 - delta ):
                path.pop()
        elif delta > 1:
            raise ValueError( "Tree syntax error. Too many indents." )
        
        last_node = path[-1]
        new_node = last_node.add_child( data = NodeData( name ) )
        status.selected = new_node
        
        MCMD.print( "Selected: {}".format( string_helper.format_array( get_path() ) ) )


@command()
def branch( parents: List[MNode], child: MNode ):
    """
    Specifies a branch from one node to another.
    :param parents:  Parent node(s) 
    :param child:   Child node
    """
    for parent in parents:
        parent.add_edge_to( child )
        MCMD.print( "{} --> {}".format( parent, child ) )
