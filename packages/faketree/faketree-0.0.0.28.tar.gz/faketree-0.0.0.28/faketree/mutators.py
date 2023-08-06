import random
from typing import Set, List, cast

from os import path

from faketree.treedata import FtBlast, FtSequence, FtSite, FtSiteName, NodeData
from intermake import MENV, constants
from mgraph import MNode, FollowParams, exporting
from mgraph.graphing import EDirection
from mhelper import string_helper, LogicError, safe_cast, bio_helper, Logger
from intermake import subprocess_helper


class Frame:
    def __init__( self, sequence: FtSequence, blast: List[FtBlast], _no_check: bool = False ):
        if not _no_check:
            assert isinstance( sequence, FtSequence )
            assert isinstance( blast, list )
            assert not blast or all( isinstance( x, FtBlast ) for x in blast )
        
        self.sequence = sequence
        self.blast = blast
    
    
    WAITING = None
    WORKING = None


Frame.WAITING = Frame( cast( FtSequence, None ), cast( list, None ), True )
Frame.WORKING = Frame( cast( FtSequence, None ), cast( list, None ), True )

LOG_SG = Logger( "seqgen", False )


class Mutation:
    def __init__( self, node: MNode ):
        self.__node = node
    
    
    @property
    def node( self ) -> MNode:
        return self.__node
    
    
    def reset( self ):
        self.on_reset()
    
    
    def on_reset( self ):
        self.node.data.sequence = None
        self.node.data.blast = None
    
    
    def mutate( self ) -> bool:
        """
        Mutates the node.
        
        :return:    A value `True` to indicate a change in status, or `False` to indicate no change in status. 
        """
        d = self.node.data
        assert isinstance( d, NodeData )
        if d.sequence is None:
            r: Frame = self.on_mutate()
            
            if r is None:
                raise ValueError( ":method:`on_mutate` must return a value." )
            if r is Frame.WAITING:
                return False
            elif r is Frame.WORKING:
                return True
            
            assert r.sequence is not None
            assert r.blast is not None
            
            d.sequence = r.sequence
            d.blast = r.blast
            
            return True
        else:
            assert d.blast is None
            return False
    
    
    def on_mutate( self ) -> Frame:
        raise NotImplementedError( "abstract" )


class MutationWithPool( Mutation ):
    DEFAULT_POOL = "ACEFGHIKLMNPQRSTVWY"
    
    
    def __init__( self, node: MNode, pool: str ):
        super().__init__( node )
        self.__pool = pool
    
    
    @property
    def use_pool( self ) -> str:
        if self.__pool:
            return self.__pool
        else:
            return MutationWithPool.DEFAULT_POOL
    
    
    def format_display_pool( self, text ):
        if self.__pool:
            return text.replace( "*", self.__pool )
        else:
            return ""
    
    
    def pick_from_pool( self, disregard = None ):
        if disregard:
            choices = list( self.use_pool )
            
            for old_site in disregard:
                if old_site in choices:
                    choices.remove( old_site )
                else:
                    raise ValueError( "«{}» not in «{}»".format( old_site, choices ) )
        else:
            choices = self.use_pool
        
        if not choices:
            raise ValueError( "Cannot pick from pool because the pool is empty (this may be after disregarding certain sites). Change your mutation parameters and try again." )
        
        r = random.choice( choices )
        
        if disregard and r in disregard:
            raise ValueError( "Sorry. I chose «{}» from «{}» but you told me not to do that.".format( r, self.use_pool ) )
        
        return r
    
    
    def on_mutate( self ) -> Frame:
        raise NotImplementedError( "abstract" )


class UniqueMutationRoot( MutationWithPool ):
    def __init__( self, node: MNode, pool: str, amplitude: int ):
        super().__init__( node, pool )
        self.sequence_out = FtSequence( "" )
        self.amplitude = amplitude
    
    
    def on_reset( self ):
        self.sequence_out = FtSequence( "" )
    
    
    def acquire_unique_index( self ) -> FtSiteName:
        name = FtSiteName()
        self.sequence_out.add_site( FtSite( name = name, site = self.pick_from_pool() ) )
        return name
    
    
    def on_mutate( self ) -> Frame:
        # Find all descendants
        de = self.node.list_descendants()
        for descendant in de:
            if isinstance( descendant.data.mutator, UniqueMutation ):
                if descendant.data.mutator.site_names is None:
                    # Not all descendants are yet ready
                    return Frame.WAITING
        
        # Root has no BLAST
        blast = []
        
        # We must shuffle the result, or if `amplitude` is > 1 then adjacent sites will always mutate together, which causes problems for alignments
        random.shuffle( self.sequence_out.data )
        
        return Frame( self.sequence_out, blast )
    
    
    def __str__( self ):
        if self.amplitude == 1:
            a = ""
        else:
            a = "+{} ".format( self.amplitude )
        
        return "🔧 UNIQUE MUTATION {}ROOT{}".format( a, self.format_display_pool( " (pool=*)" ) )


class RandomMutationRoot( MutationWithPool ):
    
    
    def __init__( self, node: MNode, length: int, pool: str ):
        super().__init__( node, pool )
        self.intended_length = length
    
    
    def __str__( self ):
        return "💥 RANDOM SEQUENCE ({}{})".format( self.format_display_pool( "*=" ), self.intended_length )
    
    
    def on_mutate( self ) -> Frame:
        r = []
        
        for _ in range( self.intended_length ):
            r.append( self.pick_from_pool() )
        
        sequence_result = FtSequence( "".join( r ) )
        blast_result = []  # root has no blast
        
        return Frame( sequence_result, blast_result )


class RandomMutation( MutationWithPool ):
    def __init__( self, node: MNode, chance: float, pool: str ):
        super().__init__( node, pool )
        self.intended_chance = chance
    
    
    def on_mutate( self ) -> Frame:
        sequence = FtSequence()
        
        if self.node.num_parents != 1:
            raise ValueError( "Cannot apply a random mutation to a node with «{}» parents.".format( self.node.num_parents ) )
        
        if self.node.parent.data.sequence is None:
            return Frame.WAITING
        
        for site in self.node.parent.data.sequence:
            assert isinstance( site, FtSite )
            
            if random.random() >= self.intended_chance:
                sequence.add_site( site )
            else:
                sequence.add_site( FtSite( name = site.name, site = self.pick_from_pool() ) )
        
        blasts = [FtBlast( self.node, self.node.parent, 1, len( sequence ), 1, len( sequence ) )]
        
        return Frame( sequence, blasts )
    
    
    def __str__( self ):
        return "▶️ RANDOM MUTATIONS ({}{})".format( self.format_display_pool( "*=" ), self.intended_chance )


class FixedSequence( Mutation ):
    def __init__( self, node: MNode, sequence: str ):
        super().__init__( node )
        self.intended_sequence = sequence
    
    
    def on_mutate( self ) -> Frame:
        sequence = FtSequence( self.intended_sequence )
        blasts = []
        return Frame( sequence, blasts )
    
    
    def __str__( self ):
        return "📝 " + self.intended_sequence


class CombinationMutation( Mutation ):
    def on_mutate( self ) -> Frame:
        r = FtSequence()
        b = []
        
        for parent in sorted( self.node.parents, key = lambda x: x.data.name ):
            s = parent.data.sequence
            if s is None:
                return Frame.WAITING
            
            start, end = r.extend( s )
            b.append( FtBlast( self.node, parent, start + 1, end, 1, len( s ) ) )
        
        return Frame( r, b )
    
    
    def __str__( self ):
        return "‼️ COMPOSITE {}".format( string_helper.format_array( self.node.parents, final = " and " ) )


class SeqgenMutation( Mutation ):
    def __init__( self, node: MNode, length: int, seq_len: int, parameters: str ):
        super().__init__( node )
        self.edge_length = length
        self.seq_len = seq_len
        self.reg_sequence = None
        self.is_appropriated = False
        self.subgraph = None
        self.mrca = None
        self.all_done = False
        self.parameters = parameters
    
    
    def __str__( self ):
        return "🖥 SEQGEN"
    
    
    def is_compatible( self, node: MNode ):
        if node is None:
            return False
        
        d = safe_cast( NodeData, node.data )
        
        if not isinstance( d.mutator, SeqgenMutation ):
            return False
        
        if d.mutator.parameters != self.parameters:
            return False
        
        return True
    
    
    def on_reset( self ):
        self.reg_sequence = None
        self.is_appropriated = None
        self.subgraph = None
        self.mrca = None
        self.all_done = False
    
    
    def set_reg_sequence( self, value ):
        if self.reg_sequence:
            raise ValueError( "Cannot set a reg_sequence on this node «{}» because it already has one.".format( self.node ) )
        
        self.reg_sequence = value
    
    
    def on_mutate( self ) -> Frame:
        # Sanity check
        if self.all_done:
            raise ValueError( "{}: Mutator called when already complete.".format( self.node ) )
        
        # The first node called is responsible for the work, is that us?
        if self.is_appropriated:
            # No, it's not.
            if self.reg_sequence:
                if self.node.has_parents:
                    if not self.node.parent.data.sequence:
                        # Wait for parent so we can get the site names
                        return Frame.WAITING
                    
                    return self.__use_registered_sequence( self.node.parent.data.sequence )
                else:
                    return self.__use_new_sequence()
            else:
                # Another node is doing the work, we just need to wait for reg_sequence to be set
                return Frame.WAITING
        
        # Have we generated the subgraph already?
        if self.subgraph is None:
            # No. Find our root.
            mrca = self.node
            
            while True:
                if mrca.parent is None:
                    break
                elif not self.is_compatible( mrca.parent ):
                    mrca = mrca.parent
                    break
                else:
                    mrca = mrca.parent
            
            self.mrca = mrca
            
            # `self.mrca` is now either a true root (SeqgenMutation) or the node before it (some other Mutation)
            # whatever, generate our subtree
            subset = self.node.graph.follow( FollowParams( start = self.mrca, node_filter = self.is_compatible, direction = EDirection.OUTGOING ) ).visited_nodes
            self.subgraph = self.node.graph.copy( nodes = subset )
            self.subgraph.find_node( self.mrca.uid ).make_root()
            
            # Flag all the nodes as appropriated so they won't try to do the same things as us
            for node in subset:
                if isinstance( node.data.mutator, SeqgenMutation ):
                    node.data.mutator.is_appropriated = True
            
            # We're doing the work
            self.is_appropriated = False
            
            LOG_SG( "{}: Taking the subset {}", self.node, subset )
        
        if not self.is_compatible( self.mrca ):
            # If the MRCA is something else that'll be our ancestor when we call Seqgen
            LOG_SG( "{}: The MRCA is already built - {}", self.node, self.mrca )
            
            if not self.mrca.data.sequence:
                # We must wait for the MRCA to become ready
                return Frame.WAITING
            
            origin_sequence = self.mrca.data.sequence
            arg_1k = "-k"
            arg_1v = "1"
        else:
            # Otherwise the MRCA gets randomised by Seqgen just like everything else
            LOG_SG( "{}: The MRCA is not built - {}", self.node, self.mrca )
            origin_sequence = None
            arg_1k = "-l"
            arg_1v = str( self.seq_len )
        
        # Write the SEQGEN file
        file_name = path.join( MENV.local_data.local_folder( constants.FOLDER_TEMPORARY ), "seq_gen.newick" )
        
        with open( file_name, "w" ) as file_out:
            if origin_sequence:
                file_out.write( "1 {}\n".format( len( origin_sequence ) ) )
                file_out.write( "root    {}\n".format( origin_sequence ) )
                file_out.write( "1" )
            
            subtree = exporting.export_newick( self.subgraph,
                                               fnode = lambda x: x.data.name,
                                               fedge = lambda x: str( x.right.data.mutator.edge_length ),
                                               internal = False )
            file_out.write( subtree + "\n" )
        
        # Run seqgen
        stdout = []
        # noinspection SpellCheckingInspection
        args = ["seq-gen",
                "-m", "MTREV",
                arg_1k, arg_1v,
                "-wa"]
        args.extend( x for x in self.parameters.split( " " ) if x )
        args.append( file_name )
        LOG_SG( "{}: Running {}", self.node, args )
        subprocess_helper.run_subprocess( args,
                                          collect_stdout = stdout.append,
                                          hide = True )
        
        # Parse the output
        nodes = dict( (x.data.name, x) for x in self.subgraph )
        pending = []
        
        # Loop the sequences.
        # Note that Seqgen outputs bad Fasta and an incorrect sequence count for Phylip, so we need to fiddle about a bit with its output
        for accession, sequence in bio_helper.parse_phylip( lines = stdout, ignore_num_seq = True ):
            node = nodes.get( accession )
            if node is not None:
                LOG_SG( "{}:       ASSIGN: {}", self.node, accession )
                self.set_reg_sequence_on( node, sequence )
                
                while pending:
                    node = node.parent
                    LOG_SG( "{}: POP  PENDING: {}", self.node, node )
                    self.set_reg_sequence_on( node, pending.pop() )
            else:
                LOG_SG( "{}: PUSH PENDING: {}", self.node, accession )
                pending.append( sequence )
        
        # Some sanity checks
        for node in self.subgraph:
            if isinstance( node.data.mutator, SeqgenMutation ):
                if node.data.mutator.reg_sequence is None:
                    raise ValueError( "{}: Failed to provide a sequence to all nodes, for instance «{}» is unassigned.".format( self.node, node ) )
        
        if pending:
            raise ValueError( "‘SeqGenMutation’ on the node «{}». Expected SeqGen output to be ordered and have the same number of sequences as in the initial tree, but «{}» sequences are in the output that haven't been assigned. Something went wrong. Try turning on «{}» logging and rerun your query.".format( self.node, len( pending ), LOG_SG.name ) )
        
        # We've all done, return asking to be called back one last time
        self.is_appropriated = True
        return Frame.WORKING
    
    
    def __use_new_sequence( self ) -> Frame:
        result = FtSequence()
        
        for new_site in self.reg_sequence:
            result.add_site( FtSite( name = FtSiteName(), site = new_site ) )
        
        self.all_done = True
        return Frame( result, [] )
    
    
    def __use_registered_sequence( self, ancestor_sequence: FtSequence ) -> Frame:
        result = FtSequence()
        
        assert isinstance( ancestor_sequence, FtSequence ), ancestor_sequence
        assert isinstance( self.reg_sequence, str )
        
        if len( ancestor_sequence ) != len( self.reg_sequence ):
            raise ValueError( "{}: Mutated sequence not same length «{}» as its origin «{}».".format( self.node, len( self.reg_sequence ), len( ancestor_sequence ) ) )
        
        for old_site, new_site in zip( ancestor_sequence, self.reg_sequence ):
            assert isinstance( old_site, FtSite )
            assert isinstance( new_site, str )
            result.add_site( FtSite( name = old_site.name, site = new_site ) )
        
        blast = FtBlast( self.node, self.node.parent, 1, len( result ), 1, len( result ) )
        self.all_done = True
        return Frame( result, [blast] )
    
    
    def set_reg_sequence_on( self, node, sequence ):
        if isinstance( node.data.mutator, SeqgenMutation ):
            node.data.mutator.set_reg_sequence( sequence )
        else:
            assert isinstance( node.data, NodeData ), node
            assert isinstance( node.data.sequence, FtSequence ), node
            
            for old_site, new_site in zip( node.data.sequence, sequence ):
                assert isinstance( old_site, FtSite )
                assert isinstance( new_site, str )
                
                if old_site.site != new_site:
                    raise ValueError( "{}: Expected origin sequence to stay intact.".format( self.node ) )


class UniqueMutation( MutationWithPool ):
    def __init__( self, node: MNode, pool: str, amplitude: int ):
        super().__init__( node, pool )
        self.site_names: Set[FtSiteName] = None
        self.amplitude = amplitude
    
    
    def on_reset( self ):
        self.site_names = None
    
    
    def on_mutate( self ) -> Frame:
        if self.node.num_parents != 1:
            raise ValueError( "This node «{}» has a `UniqueMutation` but it has no parent. Set this node as a child of another, or change its mutation type to `UniqueMutationRoot`.".format( self.node ) )
        
        # Get the parent sequence
        parent_sequence = self.node.parent.data.sequence
        
        if self.site_names is None:
            ancestors = self.__get_viable_ancestors()
            
            if not ancestors:
                raise ValueError( "UniqueMutation isn't viable because the node has no UniqueMutationRoot ancestors." )
            
            lst = set()
            
            for ancestor in ancestors:
                for i in range( self.amplitude ):
                    for j in range( ancestor.amplitude ):
                        lst.add( ancestor.acquire_unique_index() )
            
            self.site_names = lst
            
            if parent_sequence is None:
                return Frame.WORKING
        
        elif parent_sequence is None:
            return Frame.WAITING
        
        r = FtSequence()
        
        for s in parent_sequence:
            if s.name in self.site_names:
                old_site = s.site
                
                new_site = self.pick_from_pool( disregard = old_site )
                
                if new_site == old_site:
                    raise LogicError( "This mutation is not a mutation but a UniqueMutation must be guaranteed. («{}»): «{}» --> «{}»".format( self, old_site, new_site ) )
                
                r.add_site( FtSite( site = new_site, name = s.name ) )
            else:
                r.add_site( FtSite( site = s.site, name = s.name ) )
        
        assert len( r ) == len( parent_sequence )
        
        b = [FtBlast( self.node, self.node.parent, 1, len( r ), 1, len( r ) )]
        
        return Frame( r, b )
    
    
    def __get_viable_ancestors( self ):
        ancestors = []
        visits = [self.node]
        for visit in visits:
            if isinstance( visit.data.mutator, UniqueMutationRoot ):
                ancestors.append( visit.data.mutator )
                continue
            
            for parent in visit.parents:
                visits.append( parent )
        return ancestors
    
    
    def __str__( self ):
        if self.amplitude == 1:
            a = ""
        else:
            a = "+{} ".format( self.amplitude )
        return "↖️ UNIQUE MUTATION {}FROM {}{}".format( a, string_helper.format_array( (x.node for x in self.__get_viable_ancestors()), final = " or " ), self.format_display_pool( " (pool=*)" ) )
