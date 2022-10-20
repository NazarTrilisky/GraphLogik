# GraphLogik

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
2. pytest tests

