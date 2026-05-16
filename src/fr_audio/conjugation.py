from verbecc import CompleteConjugator


def fetch_verb_conjugation(
    lang: str, infinitive: str, mood: str, tense: str
) -> list[str]:
    """
    Fetch a set of French conjugated verb phrases from verbecc. 

    Args:
        lang (str): language (eg. 'fr', 'es', 'ca', etc.)
        infinitive (str): infinitive verb
        mood (str): Grammatical mood (eg. 'indicative', 'imperative', 'conditional', etc.)
        tense (str): GRammatical tense (eq. 'present', 'past', 'future', etc.)
    Returns:
        set[str]: A set of French conjugated verb phrases regarding the tense \
            or an empty set if the requested tense not found
    """
    cc = CompleteConjugator(lang).conjugate(infinitive)

    return [c[0] for c in cc[mood][tense]]
