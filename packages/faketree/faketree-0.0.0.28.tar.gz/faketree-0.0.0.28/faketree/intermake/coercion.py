from stringcoercion import coercion, Coercer, CoercionInfo
from typing import Optional
from mgraph import MNode


def setup():
    coercer = coercion.get_default_coercer()
    
    
    class MNodeCoercer( Coercer ):
        def can_handle( self, info: CoercionInfo ):
            return info.annotation.is_directly_below( MNode )
        
        
        def coerce( self, info: CoercionInfo ) -> Optional[object]:
            from faketree.workspace import status
            
            for node in status.tree:
                if node.data.name == info.source:
                    return node
            
            raise ValueError( "No such node as «{}».".format( info.source ) )
    
    
    coercer.register( MNodeCoercer() )
