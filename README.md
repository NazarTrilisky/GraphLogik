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
* Update text-to-graph to not lose data (every item in sentence should be linked)
   - verb approach is good, but is missing some data: e.g. "handsome" from test_1
   - issue is that the "handsome" sentence - Spacy doesn't recognize subj and obj pos_
   - the token.head tree-building approach does not miss "handsome", but has
     nodes for verbs, which should be links between nodes
   - May need to combine two approaches: token.head tree approach and subj-verb-obj approach
* Keep using verb as edge between Noun and Adj nodes
* Add weights to nodes, not edges.

