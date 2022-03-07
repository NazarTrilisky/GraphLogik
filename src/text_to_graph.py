
import spacy
from src.graph import KnowledgeGraph

from depronounize.depronounize import replace_pronouns

nlp = spacy.load('en_core_web_sm')
stopwords = ['a', 'the', 'for', 'at', 'by']


def translate_text_into_graph(kg, text):
    """
    Adds nodes and relationships from the sentences into knowledge graph (kg)
    """
    new_text = replace_pronouns(text)
    new_text = new_text.replace(';', '.')
    sentences = new_text.split(".")

    for sentence in sentences:
        tokens_w_stopwords = nlp(sentence)
        tokens = [token for token in tokens_w_stopwords if not token.text in stopwords]

        #print("\n\n")
        #for t in tokens:
        #    print(t, t.pos_, t.dep_)

        adj_list = []
        subj = None
        obj = None
        verb = None

        # get entities and descriptions: adj expected to precede noun
        descr_tokens = []
        for token in tokens:
            if token.pos_ in ['ADJ', 'NUM']:
                descr_tokens.append(token)
            elif token.pos_ in ['NOUN']:
                kg.addNode(token.lemma_)
                for descr_token in descr_tokens:
                    kg.addNode(descr_token.lemma_)
                    kg.connect(token.lemma_, descr_token.lemma_)
                descr_tokens.clear()

        def get_subj_obj(idx):
            """
            Return tuple with two lists ([subjects], [objects])
            for the verb at the given index
            """
            subjects = []
            objects = []
            cur = idx - 1
            # move backwards to find subjects
            while cur >= 0 and tokens[cur].dep_ != 'VERB':
                if tokens[cur].dep_.endswith('subj'):
                    subjects.append(tokens[cur])
                cur -= 1

            # move forward to find objects
            cur = idx + 1
            while cur < len(tokens) and tokens[cur].dep_ != 'VERB':
                if tokens[cur].dep_.endswith('obj'):
                    objects.append(tokens[cur])
                cur += 1

            return (subjects, objects)

        # get verb and connect main action, subj, obj
        subj_tok = []
        obj_tok = []
        verb_tok = None
        for idx in range(len(tokens)):
            token = tokens[idx]
            if token.pos_ == 'VERB':
                subjects, objects = get_subj_obj(idx)
                print("verb: {}, subj: {}, obj: {}".format(token, subjects, objects))
                kg.addNode(token.lemma_)
                for subj in subjects:
                    kg.addNode(subj.lemma_)
                    kg.connect(subj.lemma_, token.lemma_)
                for obj in objects:
                    kg.addNode(obj.lemma_)
                    kg.connect(obj.lemma_, token.lemma_)


if __name__ == '__main__':
    kg = KnowledgeGraph()
    text = "The quick brown fox jumped over the lazy, fat dog."
    translate_text_into_graph(kg, text)
    kg.show()

