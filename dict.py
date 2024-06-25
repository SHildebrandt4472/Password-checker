word_list = {}

def load_word_list():
    with open('words.txt') as f:
        for line in f:
            word = line.strip().lower()
            length = len(word)
            if length not in word_list:
                word_list[length] = set()  # Use a SET to make lookups faster
            word_list[length].add(word)


def word_exists(word):
    length = len(word)
    word = word.lower()
    if length not in word_list:
        return False
    if word in word_list[length]:
        return True
    return False