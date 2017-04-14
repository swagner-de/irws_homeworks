INTERPOLATION_FACTOR = 0.5


class InvertedIdxDocEntry():

    def __init__(self, doc_id, term, docs):
        self.doc_id = doc_id
        self.tf = docs[doc_id].count(term)
        self.doc_tokens = len(docs[doc_id])

    @property
    def unigram_model(self):
        return self.tf/self.doc_tokens

    def __hash__(self):
        return self.doc_id

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __str__(self):
        return 'id:%s, tf:%s, total_tokens:%s' % (str(self.doc_id), str(self.tf), str(self.doc_tokens))


class InvertedIdx:

    def __init__(self):
        self.idx = {}
        self.docs_indexed = []
        self.total_tokens = 0

    def __str__(self):
        rep = ''
        for k, v in self.idx.items():
            vals = '; '.join([str(i) for i in v])
            rep += "'%s':\t%s\n" % (k, vals)
        return rep

    def total_occurrences(self, term):
        """
        :param term: the term for which the occurrences shall be counted in the index
        :return: the total number of occurrences in all documents
        """
        occurrences = 0
        try:
            for doc in self.idx[term]:
                occurrences += doc.tf
            return occurrences
        except KeyError:
            return 0

    def build_idx_from_docs(self, docs):
        for id in range(len(docs) - 1):
            for term in docs[id]:
                self.add_term(term, id, docs)

    def add_term(self, term, doc_id, docs):
        entry = InvertedIdxDocEntry(doc_id, term, docs)
        if term in self.idx:
            self.idx[term].add(entry)
        else:
            self.idx[term] = set([entry])
        if entry.doc_id not in self.docs_indexed:
            self.docs_indexed.append(entry.doc_id)
            self.total_tokens += entry.doc_tokens

    def local_unigram(self, term, doc_id):
        try:
            docs = self.idx[term]
            for doc in docs:
                if doc.doc_id == doc_id:
                    return (INTERPOLATION_FACTOR * doc.unigram_model) +\
                           ((1 - INTERPOLATION_FACTOR) * self.global_unigram(term))
        except KeyError:
            pass
        return 0

    def global_unigram(self, term):
        return self.total_occurrences(term) / self.total_tokens


def build_local_unigram(doc_id, docs, inv_idx):
    unigram = {}
    for term in set(docs[doc_id]):
        unigram[term] = inv_idx.local_unigram(term, doc_id)
    return unigram


def build_global_unigram(inv_idx):
    unigram = {}
    for key in inv_idx.idx:
        unigram[key] = inv_idx.global_unigram(key)
    return unigram
