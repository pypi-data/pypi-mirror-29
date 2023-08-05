XGraph
======

|Build Status|

About
-----

Is an open-source graph package that contains algorithms for
undirected/directed graphs and its written in **Python3.6** .

Code Example
~~~~~~~~~~~~

.. code:: python

    from XGraph import *

    if __name__ == "__main__":

        names = ['a','b','c','d'] # node-name list
        g = Graph() # Create the Graph instance

        createNodes(g,names) # Create the nodes based on the names list

      # Create the Weighted Edges
        g.addEdge('a','b',1) 
        g.addEdge('b','c',2)
        g.addEdge('c','a',3)
        g.addEdge('c','d',6)
      
      # Print the graph
        printGraph(g)

.. |Build Status| image:: https://travis-ci.com/DigitMan27/XGraph.svg?token=PnQRkEaHikski3HhP5jr&branch=master
   :target: https://travis-ci.com/DigitMan27/XGraph
