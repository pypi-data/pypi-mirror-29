MGraph
======

Yet another graphing library.
This library provides supports to Gʀᴏᴏᴛ, providing functionality for graphs somewhere on the phylogenetic tree/network border.

MGʀᴀᴩʜ provides an uncommon feature set, with much of its functionality being provided in GROOT itself.
If you are looking for a graph library you might want to check out Nᴇᴛᴡᴏʀᴋx or Iɢʀᴀᴩʜ, or for phylogenetics, Eᴛᴇ or Dᴇɴᴅʀᴏᴩʏ. 


Installation
------------

```bash
(sudo) pip install mgraph
```

Usage
-----

MGʀᴀᴩʜ follows an object orientated approach, where nodes and edges are objects to which arbitrary data may (or may not) be attached.
The MGʀᴀᴩʜ library is well documented inline using [reStructuredText](http://docutils.sourceforge.net/rst.html).

```python
from mgraph import MGraph

g = MGraph.from_newick( "((A,B),C);" )
node1 = g.nodes.by_data( "A" )
node2 = g.nodes.by_data( "C" )
node3 = node1.add_child( "D" )
node3.add_edge_to( node2 )
print( g.to_csv() )
```

All edges and nodes support arbitrary data.

```python
from mgraph import MGraph

g = MGraph()
spam  = g.add_node( "Spam" )
beans = g.add_node( { "name": "Beans" } )
eggs  = g.add_node( 42 )
g.add_edge( spam, beans, data = {"types": ("is_parent", "is_relation"), "weight": 42 } )
```

MGraph enforces some basic constraints for cases that represent error more often than intention ane make network analysis difficult.
Both of these cases can be represented using other means.

Both nodes and edges are singular; two nodes may only share a single edge and a single edge may only span two nodes.
This doesn't mean nodes cannot have multiple relation types between them, just make sure the edge's `data` property accommodates them both. e.g.
This helps to avoid common mistakes and means that when travelling the graph all the necessary data is contained within the singular edge object and the programmer doesn't have to look anywhere else.

```python
from mgraph import MGraph

g = MGraph()
node_1 = g.add_node()
node_2 = g.add_node()

# Don't do this
g.add_edge(node_1, node_2, data = "is_parent")
g.add_edge(node_1, node_2, data = "is_relation") # Error

# Do this
g.add_edge(node_1, node_2, data = ("is_parent", "is_relation")) 
```

Similarly, self-references are invalid.
This helps to avoid common mistakes. 

```python
from mgraph import MGraph

g = MGraph()
node_1 = g.add_node()

# Don't do this
g.add_edge(node_1, node_1, data = "likes_itself")  # Error

# Do this
node_1.data = "likes_itself"
```

Development
-----------

MGraph uses the unit tests run by executing the `__test__.py` file.
Code coverage should be >= 70% for each source file.


Meta
----

```ini
host     = bitbucket,pypi
language = python3
author   = martin rusilowicz
licence  = https://www.gnu.org/licenses/agpl-3.0.html
```
