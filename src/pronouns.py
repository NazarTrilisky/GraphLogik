
last_masculine_token  = None
last_feminine_token   = None
last_plural_token     = None
last_neutral_token    = None

feminine_pronouns =     ['she', 'her', 'hers', 'herself']
masculine_pronouns =    ['he', 'him' 'his', 'himself']
neutral_pronouns =      ['who', 'whom', 'whose', 'it', 'its', 'itself']
plural_pronouns =       ['they', 'them', 'their', 'theirs', 'themselves']


def is_plural(token):
    return token.text.lower() != token.lemma_.lower()


def get_last_fem_pron(token):
    global last_feminine_token
    if last_feminine_token:
        return last_feminine_token
    else:
        if last_neutral_token:
            last_feminine_token = last_neutral_token
            return last_feminine_token
    return token


def get_last_masc_pron(token):
    global last_masculine_token
    if last_masculine_token:
        return last_masculine_token
    else:
        if last_neutral_token:
            last_masculine_token = last_neutral_token
            return last_masculine_token
    return token


def get_root(tokens):
    for tok in tokens:
        if tok.dep_ == 'ROOT':
            return tok
    return None


def update_last_noun(tokens, idx):
    global last_plural_token
    global last_neutral_token

    # Only consider key nouns
    root = get_root(tokens)
    if root and tokens[idx] not in [t for t in root.children]:
        pass
    else:
        if is_plural(tokens[idx]):
            last_plural_token = tokens[idx]
        else:
            last_neutral_token = tokens[idx]


def get_text_for_pronoun(token):
    pronoun = token.text.lower()

    if pronoun in plural_pronouns and last_plural_token:
        return last_plural_token.text
    elif pronoun in feminine_pronouns:
        return get_last_fem_pron(token).text
    elif pronoun in masculine_pronouns:
        return get_last_masc_pron(token).text
    elif pronoun in neutral_pronouns and last_neutral_token:
        return last_neutral_token.text

    return token.text

