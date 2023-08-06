from mgraph import MGraph, MNode


class CurrentStatus:
    def __init__( self ):
        self.tree: MGraph = MGraph()
        self.selected: MNode = None
    
    
    def reset( self ):
        self.tree = MGraph()
        self.selected = None


status: CurrentStatus = CurrentStatus()
