
import spacy
from src.graph import KnowledgeGraph


nlp = spacy.load('en_core_web_sm')
stopwords = ['a', 'the', 'for', 'at', 'by']

#Pronoun replace
last_masculaine_entity  = None
last_feminine_entity    = None
last_plural_entity      = None
feminine_pronouns =     ['she', 'her', 'hers', 'herself']
masculaine_pronouns =   ['he', 'him' 'his', 'himself']
neutral_pronouns =      ['it', 'its', 'itself']
plural_pronouns =       ['they', 'them', 'their', 'theirs', 'themselves']


def replace_pronoun(token):
    """
    Replace pronoun token with the string of what it refers to
    """
    global last_masculaine_entity
    global last_feminine_entity
    global last_plural_entity
    global feminine_pronouns
    global masculaine_pronouns
    global neutral_pronouns
    global plural_pronouns

    return "PRONOUN"


def add_adjectives_to_graph(kg, tokens):
    """
    Get entities and descriptions: adj expected to precede noun
    The 'tokens' arg is for a single sentence
    """
    descr_tokens = []
    for token in tokens:
        if token.pos_ in ['ADJ', 'NUM']:
            descr_tokens.append(token)
        elif token.pos_ in ['NOUN']:
            for descr_token in descr_tokens:
                if token.text.strip() and descr_token.text.strip():
                    kg.addNode(token.text)
                    kg.addNode(descr_token.text)
                    kg.addEdge(token.text, descr_token.text, label='')
            descr_tokens.clear()


def get_subj_obj(tokens, idx):
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


def translate_text_into_graph(kg, text):
    """
    Adds nodes and relationships from the sentences into knowledge graph (kg)
    """
    new_text = text.replace(';', '.')
    sentences = new_text.split(".")

    for sentence in sentences:
        tokens_w_stopwords = nlp(sentence)
        tokens = [token for token in tokens_w_stopwords if not token.text in stopwords]
        tokens = [token for token in tokens if token.text.strip()]

        print("\n\n")
        for t in tokens:
            print(t, t.pos_, t.dep_, t.text)

        adj_list = []
        subj = None
        obj = None
        verb = None

        add_adjectives_to_graph(kg, tokens)

        # get verb and connect main action, subj, obj
        subj_tok = []
        obj_tok = []
        verb_tok = None

        for idx in range(len(tokens)):
            token = tokens[idx]
            if token.pos_ == 'VERB':
                verb_token = token
                subjects, objects = get_subj_obj(tokens, idx)
                print("verb: {}, subj: {}, obj: {}".format(verb_token, subjects, objects))
                for subj in subjects:
                    for obj in objects:
                        if obj.text.strip() and subj.text.strip():
                            subj_text = subj.text
                            obj_text = obj.text
                            if subj.pos_ == 'PRON':
                                subj_text = replace_pronoun(subj)
                            if obj.pos_ == 'PRON':
                                obj_text = replace_pronoun(obj)
                            kg.addNode(subj_text)
                            kg.addNode(obj_text)
                            kg.addEdge(subj_text, obj_text, label=verb_token.text)


if __name__ == '__main__':
    kg = KnowledgeGraph()
    text = "The quick brown fox jumped over the lazy, fat dog."
    translate_text_into_graph(kg, text)
    kg.show()

