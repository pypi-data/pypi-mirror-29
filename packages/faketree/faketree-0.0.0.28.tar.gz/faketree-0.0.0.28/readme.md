Fake Tree
=========

A evolution simulator with fusions.

Introduction
------------

Ideal or realistic evolution of gene sequences according to trees incorporating fusion events (i.e. n-rooted fusion graphs).

The idea behind FakeTree is that during the development of algorithms it helps if the original trees/graphs can _always_ be deduced from the resultant data.
As development progresses it is then helpful if those methods are represent realistic data.

> FakeTree supports:
> * Evolution models:
>     *   Pure random (every site change is random)
>     *   Ideal (every site change is unique and irreversible)
>     *   Realistic (by back-ending [Sᴇǫɢᴇɴ](http://tree.bio.ed.ac.uk/software/seqgen))
> * Specification models:
>     *   Newick
>     *   Visually
>     *   Edge lists
> * Outputs:
>     *   FASTA sequences
>     *   "perfect BLAST" (the results we'd expect from BLAST if the evolution was known)

Example
-------

_FILE: example.imk_
```bash
# First we generate three very simple trees
# They all look the same
# Visually:
TREE a1
TREE -a2
TREE --a3
TREE --a4
TREE -a5

# Newick:
NEWICK (((b3,b4),b2),b5),b1

# Edge list:
ROOT c1
EDGE c1 c2
EDGE c1 c5
EDGE c2 c3
EDGE c2 c4 

# Okay, now we'll make each tree have a unique mutation sequence
UNIQUE a1
UNIQUE b1
UNIQUE c1

# And join our trees together to form a graph
BRANCH a3 c1
BRANCH b3 c1

# Now we can replace the mutation on the root of the "c" tree with a composite node
COMPOSITE c1

# Show the model
SHOW

# Generate our data
APPLY

# Generate and save the data
# - specify LEAVES to assume the internal (non-leaf) nodes are extinct and invisible
FASTA LEAVES output.fasta
BLAST LEAVES output.blast
```

Run the file using:

_bash_:
```bash
faketree source example.imk
```

Meta
----

```ini
type        =   arg,cli
language    =   python3
host        =   bitbucket,pypi
author      =   martin rusilowicz
```
