from typing import List, Tuple

from mgraph import MNode
from mhelper import ansi


class NodeData:
    def __init__( self, name: str ):
        from faketree.mutators import Mutation
        self.name = name
        self.mutator: Mutation = None
        self.sequence: FtSequence = None
        self.blast: List[FtBlast] = None
    
    
    def __str__( self ):
        return self.name
    
    
    def describe( self, name: bool, mutator: bool, sequence: bool, length: bool ):
        r = []
        
        if name:
            r.append( self.name )
        
        if mutator:
            if r:
                r.append( " : " )
            r.append( str( self.mutator ) if self.mutator else "⭕️(NONE)" )
        
        if sequence:
            if r:
                r.append( " = " )
            
            r.append( str( self.sequence ) if self.sequence else "(NONE)" )
        
        if length:
            if r:
                r.append( " = " )
            
            r.append( str( len( self.sequence ) ) if self.sequence else "(NONE)" )
        
        return "".join( r )


class FtSiteName:
    pass


class FtSite:
    def __init__( self, *, name: FtSiteName = None, site: str ):
        if not name:
            raise ValueError( "Name «{}» is invalid.".format( name ) )
        
        if len( site ) != 1:
            raise ValueError( "Site «{}» is invalid.".format( site ) )
        
        self.name = name
        self.site = site
    
    
    def __str__( self ):
        return self.site


class FtSequence:
    def __init__( self, sites: str = "" ):
        self.data = [FtSite( site = x ) for x in sites]
    
    
    def __iter__( self ):
        return iter( self.data )
    
    
    def __len__( self ):
        return len( self.data )
    
    
    def add_site( self, site: FtSite ):
        self.data.append( site )
    
    
    def extend( self, sequence: "FtSequence" ) -> Tuple[int, int]:
        start = len( self )
        
        for site in sequence:
            self.add_site( FtSite( name = site.name, site = site.site ) )
        
        return start, len( self )
    
    
    def __getitem__( self, item ) -> str:
        return self.data[item].site
    
    
    def __str__( self ):
        return "".join( str( x ) for x in self.data )


class FtBlast:
    def __init__( self, query_node: MNode, subject_node: MNode, query_start: int, query_end: int, subject_start: int, subject_end: int ):
        self.query_node: MNode = query_node
        self.subject_node: MNode = subject_node
        self.query_start = query_start
        self.query_end = query_end
        self.subject_start = subject_start
        self.subject_end = subject_end
        assert query_end - query_start == subject_end - subject_start
    
    
    def to_format_6( self ) -> str:
        r = [
            self.query_node.data.name,  # 1.	 query (e.g., gene) sequence id
            self.subject_node.data.name,  # 2.	 subject (e.g., reference genome) sequence id
            self.get_pident(),  # 3.	 percentage of identical matches
            self.__len__(),  # 4.	 length	 alignment length
            self.get_mismatch(),  # 5.	 mismatch	 number of mismatches
            0,  # 6.	 number of gap openings
            self.query_start,  # 7.	 start of alignment in query
            self.query_end,  # 8.	 end of alignment in query
            self.subject_start,  # 9.	 start of alignment in subject
            self.subject_end,  # 10.	 end of alignment in subject
            0,  # 11.	 expect value
            0,  # 12.	 bit score
        ]
        
        return "\t".join( str( x ) for x in r )
    
    
    def to_format_m( self ) -> str:
        r = [
            str( self.__len__() ),
            ansi.FORE_MAGENTA + str( self.query_node.data.name ) + ansi.RESET,
            str( self.query_start ),
            str( self.query_end ),
            ansi.FORE_MAGENTA + str( self.subject_node.data.name ) + ansi.RESET,
            str( self.subject_start ),
            str( self.subject_end ),
        ]
        
        return "\t".join( str( x ) for x in r )
    
    
    def __len__( self ) -> int:
        return (self.query_end - self.query_start) + 1
    
    
    def get_pident( self ) -> int:
        return (100 * (len( self ) - self.get_mismatch())) // len( self )
    
    
    def get_mismatch( self ) -> int:
        r = 0
        
        for i in range( len( self ) ):
            x = self.query_start + i - 1
            y = self.subject_start + i - 1
            
            if self.query_node.data.sequence[x] != self.subject_node.data.sequence[y]:
                r += 1
        
        return r
