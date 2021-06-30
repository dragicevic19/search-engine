class FoundedSite:

    def __init__(self, graph, site_vertex, num_of_founded_words, num_of_repeating, words):
        self._graph = graph
        self._site_vertex = site_vertex
        self._num_of_founded_words = num_of_founded_words
        self._num_of_repeating = num_of_repeating
        self._query_words = words
        self._result = self.calculate_result()
        self._founded_text = self.find_text()

    def __str__(self):
        return str(self._site_vertex)

    def result(self):
        return self._result

    def founded_text(self):
        return self._founded_text

    def query_words(self):
        return self._query_words

    def calculate_result(self):
        result = 0
        if len(self._query_words) == self._num_of_founded_words:
            result += 1000
        result += 500 * self._num_of_repeating
        result += self.adjacent_words()
        result += 20 * self._graph.degree(self._site_vertex, False)
        result += 50 * self.result_from_linked_sites()
        return result

    def adjacent_words(self):
        counted = []
        for i in range(len(self._site_vertex.words())):
            if self._site_vertex.words()[i] == self._query_words[0]:
                count = 1
                for j in range(1, len(self._query_words)):
                    try:
                        i += 1
                        if self._site_vertex.words()[i] == self._query_words[j]:
                            count += 1
                        else:
                            break
                    except IndexError:
                        break
                if count > 1:
                    counted.append(count)
        res = 1
        for i in counted:
            res += 10000 * i
        return res

    def result_from_linked_sites(self):
        num_of_linked_site_words = 0
        for link in self._graph.incident_edges(self._site_vertex, False):
            origin, dest = link.endpoints()
            for word in self._query_words:
                founded = origin.words_trie().search(word)
                if founded:
                    num_of_linked_site_words += 1
        return num_of_linked_site_words

    def find_text(self):
        site_words = self._site_vertex.words()
        for i in range(len(site_words)):
            if site_words[i] in self._query_words:
                if i - 15 >= 0:
                    return ' '.join(site_words[i - 15:i + 15])
                else:
                    return ' '.join(site_words[i:i + 30])
