XGraph
======
|PyPi| |MIT|

+ Build Status(Windows/Linux)
       |Build|

About
-----

Is an open-source graph package that contains algorithms for
undirected/directed graphs and its written in **Python3.6** .

Installation Instructions
-----
Install with **python3 -m pip install xgraph** or **pip3 install xgraph** .



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
        
.. |Build| image:: https://travis-ci.org/DigitMan27/XGraph.svg?branch=master
    :target: https://travis-ci.org/DigitMan27/XGraph
 
.. |PyPi| image:: https://badge.fury.io/py/XGraph.svg
    :target: https://badge.fury.io/py/XGraph

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
