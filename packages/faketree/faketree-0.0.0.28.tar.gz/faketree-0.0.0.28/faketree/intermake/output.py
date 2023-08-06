from typing import Dict, List, Optional
from intermake import command, MCMD
from mgraph import MNode, exporting
from mgraph.graphing import EGraphFormat
from mhelper import ComponentFinder, Logger, MEnum, array_helper, file_helper, string_helper, io_helper

from faketree.treedata import FtBlast, NodeData
from faketree.workspace import status


LOG = Logger( "blast", False )


class ESubset( MEnum ):
    """
    Which nodes to display.
    :data ALL: All nodes
    :data LEAVES: Leaf nodes
    :data INTERNAL: Non-leaf nodes
    """
    ALL = 1
    LEAVES = 2
    INTERNAL = 3
    
    
    def includes( self, node: MNode ) -> bool:
        if node.edges.outgoing_dict:
            # Internal node
            return self != ESubset.LEAVES
        else:
            # Leaf node
            return self != ESubset.INTERNAL


def __propagate_blast() -> List[FtBlast]:
    original_blasts: List[FtBlast] = __get_all_blasts()
    cc_finder = ComponentFinder()
    complex_blasts: List[FtBlast] = []
    output_blasts: List[FtBlast] = []
    
    for blast in original_blasts:
        assert isinstance( blast, FtBlast )
        query: NodeData = blast.query_node.data
        subject: NodeData = blast.subject_node.data
        
        if len( query.sequence ) != len( subject.sequence ) or len( query.sequence ) != len( blast ):
            complex_blasts.append( blast )
            continue
        
        cc_finder.join( blast.query_node, blast.subject_node )
    
    components: List[List[MNode]] = cc_finder.tabulate()
    MCMD.information( "There are {} blast components.".format( len( components ) ) )
    
    node_to_component: Dict[MNode, List[MNode]] = { }
    
    for list_ in components:
        for element in list_:
            node_to_component[element] = list_
        
        for a, b in array_helper.triangular_comparison( sorted( list_, key = lambda x: x.data.name ) ):
            output_blasts.append( FtBlast( a, b, 1, len( a.data.sequence ), 1, len( a.data.sequence ) ) )
    
    for blast in complex_blasts:
        q_relations = node_to_component[blast.query_node]
        s_relations = node_to_component[blast.subject_node]
        
        for query_node in q_relations:
            for subject_node in s_relations:
                output_blasts.append( FtBlast( query_node, subject_node, blast.query_start, blast.query_end, blast.subject_start, blast.subject_end ) )
    
    return output_blasts


def __get_all_blasts() -> List[FtBlast]:
    blasts = []
    
    for node in status.tree:
        for blast in node.data.blast:
            blasts.append( blast )
    
    return blasts


@command()
def show( format: EGraphFormat = EGraphFormat.ASCII,
          fname: Optional[str] = None,
          name: bool = True,
          mutator: bool = True,
          sequence: bool = False,
          length: bool = True,
          file: str = "" ):
    """
    Write the tree out.
    :param file:            File to write to. See `file_write_help`.
    :param format:          Format 
    :param fname:           How to name nodes (see :function:`mgraph.realise_node_to_text`). If not specified uses the following flags. 
    :param name:            Show node names in result.
    :param mutator:         Show node mutators in result.
    :param sequence:        Show node sequences in result.
    :param length:          Show node lengths in result.
    """
    
    
    def ___get_text( n: MNode ):
        return n.data.describe( name, mutator, sequence, length )
    
    
    if fname is None:
        fname = ___get_text
    
    with io_helper.open_write( file ) as file_out:
        file_out.write( exporting.export_string( status.tree, format, fname ) )


@command()
def blast( which: ESubset = ESubset.ALL, file: str = "", minimal: bool = False ) -> None:
    """
    Prints the sequences of the tree
    :param which:           What to display.
    :param file:            File to write to. See `file_write_help`. If this is empty then headings are also printed.
    :param minimal:         Minimal output with colours. Good for viewing in the CLI. Don't use for parsing.
    """
    __check_data()
    
    r = []
    
    if not file:
        if not minimal:
            # noinspection SpellCheckingInspection
            r.append( "\t".join( ("q", "s", "%id", "len", "mis", "gap", "<<quer", "quer>>", "<<subj", "subj>>", "e", "bit") ) )
            r.append( "\t".join( ("-", "-", "---", "---", "---", "---", "------", "------", "------", "------", "-", "---") ) )
        else:
            # noinspection SpellCheckingInspection
            r.append( "\t".join( ("len", "q", "<<quer", "quer>>", "s", "<<subj", "subj>>") ) )
            r.append( "\t".join( ("---", "-", "------", "------", "-", "------", "------") ) )
    
    full_blast: List[FtBlast] = __propagate_blast()
    
    for blast in full_blast:
        if not which.includes( blast.subject_node ) or not which.includes( blast.query_node ):
            continue
        
        if not minimal:
            r.append( blast.to_format_6() )
        else:
            r.append( blast.to_format_m() )
    
    with io_helper.open_write( file ) as file_out:
        file_out.write( "\n".join( r ) )


@command()
def fasta( which: ESubset = ESubset.ALL,
           file: str = "",
           ancestral_naming: bool = False ) -> None:
    """
    Prints the sequences of the tree
    :param which:             What to display.
    :param file:            File to write to. See `file_write_help`.
    :param ancestral_naming:  Include ancestors in names.
    """
    __check_data()
    
    r = []
    
    for node in status.tree:
        assert isinstance( node, MNode )
        if not which.includes( node ):
            continue
        
        d: NodeData = node.data
        name = d.name
        
        if ancestral_naming and node.has_parents:
            if node.num_parents == 1:
                name = "{}➡{}".format( node.parent.data.name, name )
            else:
                name = "({})➡{}".format( string_helper.format_array( (x.data.name for x in node.parents), join = "+" ), name )
        
        r.append( ">{}\n{}".format( name, d.sequence ) )
    
    with io_helper.open_write( file ) as file_out:
        file_out.write( "\n".join( r ) )


def __check_data():
    for node in status.tree:
        if node.data.blast is None or node.data.sequence is None:
            raise ValueError( "No data, please create and `apply` mutations first." )


def __send_to_target( target, r ):
    text = "\n".join( r )
    
    if target is None:
        MCMD.print( text )
    else:
        file_helper.write_all_text( target, text )
        MCMD.print( "{} bytes sent to “{}”".format( len( text ), target ) )
