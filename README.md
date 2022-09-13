# AssociativeLogic

## Setup
1. pip3 install -r requirements.txt
2. python3 -m spacy download en_core_web_sm
3. sudo apt-get install python3-tk  # for GUI to work

## Basic Idea
1. Create a graph of concepts by reading and pulling out concepts and relationships.
2. Feed a situation into the above world model (graph) to activate a certain group of nodes.
3. Flow the activation along graph edges to get the next logical concept (activated group of nodes).
4. See how the thought progresses to next logical concepts/actions.


## Testing
1. cd <top-level workspace>
2. python -m pytest tests


## ToDo
* Add negation (determinant 'no'), e.g. reverse sign of weight on node for get_next_nodes().
  - May be best to add this to the graph.py traversal function: if negation, then switch weight sign.
  - First properly position negation: may need to move negation node between two nouns or move negation to edge ... not sure yet.

* Add a POC service to:
  1. Load text and conver to graph.
  2. Allow user to enter a query / question.
  3. Provide answer / next logical outcome.
     Depict relevant part of graph.
     Cool if this is game-like.
