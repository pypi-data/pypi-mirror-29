from typing import List

from faketree.mutators import CombinationMutation, MutationWithPool, RandomMutation, RandomMutationRoot, SeqgenMutation, UniqueMutation, UniqueMutationRoot
from faketree.treedata import NodeData
from faketree.workspace import status
from intermake import command
from intermake.engine.environment import MCMD
from mgraph import MNode
from mhelper import file_helper


def __send_to_target( target, r ):
    text = "\n".join( r )
    
    if target is None:
        MCMD.print( text )
    else:
        file_helper.write_all_text( target, text )
        MCMD.print( "{} bytes sent to “{}”".format( len( text ), target ) )


@command()
def apply( verbose: bool = False ):
    """
    Applies the current mutators and generates the sequences.
    
    :param verbose: Verbose output
    """
    for node in status.tree:
        if node.data.mutator is None:
            raise ValueError( "The node {} has no mutator assigned.".format( node ) )
        
        node.data.mutator.reset()
    
    n = 0
    
    all_good = False
    
    while not all_good:
        n += 1
        if verbose:
            MCMD.progress( "***** ITERATION {} *****".format( n ) )
        
        all_good = True
        any_changed = False
        
        for node in status.tree:
            if node.data.sequence:
                continue
            
            if node.data.mutator.mutate():
                any_changed = True
                
                if verbose:
                    if node.data.sequence:
                        MCMD.progress( str( node ) )
                    else:
                        MCMD.progress( str( node ) + "..." )
            
            if not node.data.sequence:
                all_good = False
        
        if not all_good and not any_changed:
            raise ValueError( "Iteration occurred but nothing changed. Check your mutators." )
    
    MCMD.print( "Applied. {} of {} nodes have a sequence.".format( sum( 1 for node in status.tree if node.data.sequence is not None ), len( status.tree ) ) )


@command()
def pool( pool: str = "" ):
    # noinspection SpellCheckingInspection
    """
        Displays or modifies the default site pool.
        This is used as the default value for some functions.
        
        :param pool:    New value for the site pool.
                        If empty the pool is displayed but not changed.
                        You can also use a single letter to specify an inbuilt pool: `D`NA or `P`rotein.
    """
    pool = pool.upper()
    if pool == "D":
        pool = "ACGT"
    elif pool == "P":
        pool = "ACEFGHIKLMNPQRSTVWY"
    elif len( pool ) == 1:
        raise ValueError( "Pool must have at least two site possibilities." )
    
    if pool:
        MutationWithPool.DEFAULT_POOL = pool
        MCMD.progress( "POOL CHANGED TO «{}»".format( pool ) )
    else:
        MCMD.progress( "POOL IS «{}»".format( pool ) )


@command( names = ("mk_composite", "composite") )
def mk_composite( nodes: List[MNode] ):
    """
    Specifies that a node originates through a composite mutation event.
    The node should have multiple parents for this to make sense.
    :param nodes:    Node(s) to set this mutator on.     
    """
    for node in nodes:
        if len( node.parents ) <= 1:
            raise ValueError( "Cannot make the node «{}» composite because composite nodes must have at least two parents." )
        
        data: NodeData = node.data
        data.mutator = CombinationMutation( node )


@command()
def mk_unique_root( nodes: List[MNode], origin: str = "", amplitude: int = 1 ):
    """
    Sets a node to use the `UniqueMutationRoot` mutator.
    - Defines a sequence with enough sites for a unique mutation for every descendant with a `UniqueMutation` mutator.
    
    :param nodes:       Node(s) to set this mutator on.     
    :param origin:      Initial site pool. An empty string denotes the default pool.
    :param amplitude:   Multiplier on the length of the sequence. e.g. If this is `2` every child will get 2 unique mutations in this sequence.
    :return: 
    """
    for node in nodes:
        node.data.mutator = UniqueMutationRoot( node, origin, amplitude )
    
    MCMD.print( "{} roots unique.".format( len( nodes ) ) )


@command()
def mk_unique( nodes: List[MNode], new_site: str = "", amplitude: int = 1 ):
    """
    Sets a node to use the `UniqueMutation` mutator.
    - Changes 1 site descending from any and all parents with a `UniqueMutationRoot` mutator.
     
    :param nodes:       Node(s) to set this mutator on. 
    :param new_site:    Mutated site. An empty string denotes the default pool.
    :param amplitude:   Multiplier on the number of sites to mutate. e.g. If this is `2` this will change 2 unique mutations from its ancestor(s).
    """
    for node in nodes:
        node.data.mutator = UniqueMutation( node, new_site, amplitude )
    
    MCMD.print( "{} nodes now unique.".format( len( nodes ) ) )


@command()
def mk_seqgen( nodes: List[MNode], parameters: str = "", edge_length: int = 1, seq_length: int = 1000 ):
    """
    Sets a node to use the `SeqgenMutation` mutator.
    Uses Seqgen to perform the mutations.
     
    :param seq_length:          Length of randomly generated sequences (ignored if the genes have an ancestor from which they derive).
    :param edge_length:         Length of edge into this node 
    :param nodes:               Node(s) to set this mutator on. 
    :param parameters:          Parameter string passed to Seq-Gen.
    """
    for node in nodes:
        node.data.mutator = SeqgenMutation( node, edge_length, seq_length, parameters )
    
    MCMD.print( "{} nodes now using seqgen.".format( len( nodes ) ) )


@command()
def mk_random( nodes: List[MNode], pool: str = "", chance = 0.05 ):
    """
    Sets a node to use the `RandomMutation` mutator.
    - Randomly changes all sites (coming from any parent).
     
    :param nodes:   Node(s) to set this mutator on. 
    :param pool:    Site pool. An empty string denotes the default pool. 
    :param chance:  Chance of mutation per site.
    """
    for node in nodes:
        node.data.mutator = RandomMutation( node, chance, pool )
    
    MCMD.print( "{} nodes now random.".format( len( nodes ) ) )


@command()
def mk_random_root( nodes: List[MNode], pool: str = "", length = 1000 ):
    """
    Sets a node to use the `RandomMutation` mutator.
    - Randomly changes all sites (coming from any parent).
     
    :param nodes:   Node(s) to set this mutator on. 
    :param pool:    Site pool. An empty string denotes the default pool. 
    :param length:  Length of sequence.
    """
    for node in nodes:
        node.data.mutator = RandomMutationRoot( node, length, pool )
    
    MCMD.print( "{} nodes now random.".format( len( nodes ) ) )


@command()
def unique( roots: List[MNode], origin: str = "", new_site: str = "", amplitude: int = 1, d_amplitude: int = 1 ):
    """
    Applies `mk_unique_root` to the root nodes and `mk_unique` to all descendants.
     
    :param roots:       Root node(s). These nodes and all descendants will have their mutators set.
    :param origin:      Parameter on `mk_unique_root`.
    :param new_site:    Parameter on `mk_unique`.
    :param amplitude:   Parameter on `mk_unique_root`.
    :param d_amplitude: Parameter on `mk_unique`.  
    """
    descendants = __acquire_set( roots )
    mk_unique_root( roots, origin, amplitude )
    mk_unique( descendants, new_site, d_amplitude )


@command()
def seqgen( roots: List[MNode], parameters: str = "" ):
    """
    Applies `mk_seqgen` to the root nodes and descendants.
     
    :param roots:           Root node(s). These nodes and all descendants will have their mutators set.
    :param parameters:      Parameter on `mk_seqgen`.
    """
    descendants = __acquire_set( roots )
    mk_seqgen( roots, parameters )
    mk_seqgen( descendants, parameters )


@command()
def random( roots: List[MNode], length = 250, pool: str = "", chance = 0.05 ):
    """
    Applies `mk_random_root` to the root nodes and `mk_random` to all descendants.
    
    :param roots:     Root node(s). These nodes and all descendants will have their mutators set.
    :param pool:      Parameter on `mk_random` and `mk_random_root`.
    :param length:    Parameter on `mk_random_root`. 
    :param chance:    Parameter on `mk_random`.
    """
    descendants = __acquire_set( roots )
    mk_random_root( roots, pool, length )
    mk_random( descendants, pool, chance )


def __acquire_set( nodes ):
    """
    Acquires the set of nodes.
    :param nodes: roots
    :return: descendants
    """
    descendants = []
    for node in nodes:
        descendants.extend( node.list_descendants() )
    return descendants
