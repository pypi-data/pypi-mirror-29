def __setup():
    from intermake import MENV
    from faketree.intermake import coercion
    
    if MENV.configure( name = "FakeTree",
                       version = __version__ ):
        coercion.setup()


__author__ = "Martin Rusilowicz"
__version__ = "0.0.0.28"
__setup()

from faketree.intermake.mutation import apply, pool, mk_composite, mk_random_root, mk_unique, mk_seqgen, mk_random, mk_random_root, unique, seqgen, random
from faketree.intermake.tree_generation import goto, copy, where, newick, random_node, random_tree, tree, branch, new, RandomChoiceError, outgroup
from faketree.intermake.output import show, blast, fasta, ESubset
from mgraph.graphing import EGraphFormat


EGraphFormat = EGraphFormat
