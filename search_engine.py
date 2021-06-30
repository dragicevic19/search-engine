from FoundedSite import FoundedSite
from dfs import DFS_complete
from graph import *
from my_parser import *
from fnmatch import fnmatch
from trie import *
import re
import pickle
from spellchecker import SpellChecker

stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out',
              'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into',
              'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the',
              'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me',
              'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both',
              'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and',
              'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over',
              'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too',
              'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my',
              'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']
p = Parser()
graph = Graph(directed=True)
verticies = {}
processed_sites = []
spell = SpellChecker()
all_words_trie = Trie()
and_op = []
or_op = []
not_op = []


def pickle_out():
    root = "python-3.8.3-docs-html"
    pattern = "*.html"
    pattern2 = "*.htm"

    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern) or fnmatch(name, pattern2):
                website = os.path.join(path, name)
                if website in processed_sites:
                    new_links(website)
                else:
                    new_vertex_and_links(website)

    pickle_out_struct = open('graph.pickle', 'wb')
    pickle.dump(graph, pickle_out_struct)
    pickle_out_struct.close()
    pickle_out_struct = open('trie.pickle', 'wb')
    pickle.dump(all_words_trie, pickle_out_struct)
    pickle_out_struct.close()


def new_links(website):
    links, words = p.parse(website)
    sec_part(links, website)


def new_vertex_and_links(website):
    processed_sites.append(website)
    links, words = p.parse(website)
    t = Trie()
    t.formTrie(words)
    all_words_trie.formTrie(words)

    verticies[website] = graph.insert_vertex(website, t, words)
    sec_part(links, website)


def sec_part(links, website):
    for link in links:
        if link in processed_sites:
            graph.insert_edge(verticies[website], verticies[link])
        else:
            sec_links, sec_words = p.parse(link)
            sec_t = Trie()
            sec_t.formTrie(sec_words)
            all_words_trie.formTrie(sec_words)

            verticies[link] = graph.insert_vertex(link, sec_t, sec_words)
            graph.insert_edge(verticies[website], verticies[link])
            processed_sites.append(link)


def pickle_in():
    global graph, all_words_trie

    pickle_in_struct = open('graph.pickle', 'rb')
    graph = pickle.load(pickle_in_struct)
    pickle_in_struct.close()
    pickle_in_struct = open('trie.pickle', 'rb')
    all_words_trie = pickle.load(pickle_in_struct)
    pickle_in_struct.close()


def search(query_words):
    founded_sites = []

    for vertex in forest.keys():
        num_of_founded_words = 0
        num_of_repeating = 0
        founded_words = []
        for word in query_words:
            founded = vertex.words_trie().search(word)
            if founded:
                founded_words.append(word)
                num_of_founded_words += 1
                num_of_repeating += founded.repeated

        if num_of_founded_words > 0:
            if check_and_op(founded_words) and check_or_op(founded_words) and check_not_op(founded_words):
                founded = FoundedSite(graph, vertex, num_of_founded_words, num_of_repeating, query_words)
                founded_sites.append(founded)

    return founded_sites


def check_and_op(founded_words):
    i = 0
    for w in and_op:
        for founded_word in founded_words:
            if founded_word in w.split():
                i += 1
    if i == len(and_op) * 2:  # jer u svakom elementu imam 2 reci : python AND sequence -> [python  sequence]
        return True
    return False


def check_or_op(founded_words):
    if not or_op:
        return True

    for w in or_op:
        for founded_word in founded_words:
            if founded_word in w.split():
                return True
    return False


def check_not_op(founded_words):
    if not not_op:
        return True

    first_word_founded = False
    for w in not_op:
        for founded_word in founded_words:
            if founded_word == w.split()[1]:
                return False
            if founded_word == w.split()[0]:
                first_word_founded = True

    return first_word_founded


def get_result(obj):
    return obj.result()


def print_results(founded_sites):
    founded_sites.sort(key=get_result, reverse=True)

    i = 0
    j = 1
    for site in founded_sites:
        founded_text = site.founded_text()

        print('{} --- {}'.format(j, site))
        TGREEN = '\033[32m'
        ENDC = '\033[m'

        for word in founded_text.split():
            if word in site.query_words():
                print(TGREEN + word + ENDC, end=' ')
            else:
                print(word, end=' ')
        print('\n\n')

        if i == 6:
            input('Pritisnite <enter> za prikaz jos rezultata...')
            i = 0
        else:
            i += 1
        j += 1


def replace_misspeled_words(input_words, misspelled):
    for i in range(len(input_words)):
        if input_words[i] in misspelled:
            input_words[i] = spell.correction(input_words[i])


def spellcheck(input_words):
    misspelled = spell.unknown(input_words)
    for word in misspelled:
        print('Da li ste mislili: ' + spell.correction(word) + '?')
    if misspelled:
        while True:
            choise = input('da - y / ne - n >> ').lower().strip()
            if choise == 'y':
                replace_misspeled_words(input_words, misspelled)
                print(input_words)
                break
            elif choise != 'n':
                print('Izaberite opciju!')
            else:
                break


def autocomplete(input_words):
    for word in input_words:
        if '*' in word:
            word = word[:-1]
            comp = all_words_trie.getAutoSuggestions(word)
            if comp == -1:
                print("No other strings found with this prefix\n")
            elif comp == 0:
                print("No string found with this prefix\n")

            return True
    return False


def check_logical_operators(res):
    words = res.split()

    for i in range(len(words) - 2):
        if words[i + 1] == 'AND':
            and_op.append(words[i].lower() + ' ' + words[i + 2].lower())
        elif words[i + 1] == 'OR':
            or_op.append((words[i].lower() + ' ' + words[i + 2].lower()))
        elif words[i + 1] == 'NOT':
            not_op.append(words[i].lower() + ' ' + words[i + 2].lower())


if __name__ == '__main__':
    pickle_out()
    # pickle_out() se poziva samo prvi put i prave se fajlovi graph.pickle i trie.pickle
    # svaki sledeci put kada se pokrece program, samo se ucitavaju ti fajlovi zbog brzine sa pickle_in()
    # pickle_in()
    forest = DFS_complete(graph)

    query = input("Unesite tekst za pretragu >> ").strip()
    res = ' '.join(re.findall("[a-zA-Z0-9*]+", query))
    input_words = res.lower().split()

    while autocomplete(input_words):
        query = input("Unesite tekst za pretragu >> ").strip()
        res = ' '.join(re.findall("[a-zA-Z0-9*]+", query))
        input_words = res.lower().split()

    check_logical_operators(res)
    filtered_words = [w for w in input_words if w not in stop_words]
    spellcheck(filtered_words)
    founded_sites = search(filtered_words)
