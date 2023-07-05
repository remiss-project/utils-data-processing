import unicodedata


def strip_accents(text):
    text = unicodedata.normalize('NFD', text)
    text = [c for c in text if unicodedata.category(c) != 'Mn']
    return ''.join(text).lower()
