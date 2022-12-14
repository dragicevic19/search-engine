class AutoSuggestionWord:

    def __init__(self, word, repeated):
        self.word = word
        self.repeated = repeated

    def repeated(self):
        return self.repeated

    def __str__(self):
        return self.word


class TrieNode:
    def __init__(self):
        # Initialising one node for trie
        self.children = {}
        self.last = False
        self.repeated = 0


class Trie:
    def __init__(self):

        # Initialising the trie structure.
        self.root = TrieNode()
        self.word_list = []

    def formTrie(self, keys):

        # Forms a trie structure with the given set of strings
        # if it does not exists already else it merges the key
        # into it by extending the structure as required
        for key in keys:
            self.insert(key)  # inserting one key to the trie.

    def insert(self, key):

        # Inserts a key into trie if it does not exist already.
        # And if the key is a prefix of the trie node, just
        # marks it as leaf node.
        node = self.root

        for a in list(key):
            if not node.children.get(a):
                node.children[a] = TrieNode()

            node = node.children[a]

        node.last = True
        node.repeated += 1

    def search(self, key):

        # Searches the given key in trie for a full match
        # and returns True on success else returns False.
        node = self.root
        found = True

        for a in list(key):
            if not node.children.get(a):
                found = False
                break

            node = node.children[a]

        if node and node.last and found:
            return node

    def suggestionsRec(self, node, word):

        # Method to recursively traverse the trie
        # and return a whole word.
        if node.last:
            end_word = AutoSuggestionWord(word, node.repeated)
            self.word_list.append(end_word)

        for a, n in node.children.items():
            self.suggestionsRec(n, word + a)

    def getAutoSuggestions(self, key):

        # Returns all the words in the trie whose common
        # prefix is the given key thus listing out all
        # the suggestions for autocomplete.
        node = self.root
        not_found = False
        temp_word = ''
        self.word_list = []

        for a in list(key):
            if not node.children.get(a):
                not_found = True
                break

            temp_word += a
            node = node.children[a]

        if not_found:
            return 0
        elif node.last and not node.children:
            return -1

        self.suggestionsRec(node, temp_word)

        self.word_list.sort(key=get_repeated, reverse=True)

        for s in self.word_list[:11]:
            print(s)

        return 1


def get_repeated(obj):
    return obj.repeated
