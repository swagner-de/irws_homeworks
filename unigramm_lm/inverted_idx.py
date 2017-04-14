INTERPOLATION_FACTOR = 0.5


class InvertedIdxDocEntry():

    def __init__(self, doc_id, term, doc, doc_tokens):
        self.doc_id = doc_id
        self.tf = doc.count(term)
        self.doc_tokens = doc_tokens

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
        self.doc_tokens = {}
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
        """
        This will create the inverted idx from an document collection
        :param docs: An array of arrays which represent tokenized docs
        """
        for id in range(len(docs) - 1):
            for term in docs[id]:
                self.add_term(term, id, docs)

    def add_term(self, term, doc_id, docs):
        """
        This will add a given term to the index
        :param term: The term for which the index entry is added
        :param doc_id: Document id that contains the term
        :param docs: The collection of all documents
        """
        if doc_id not in self.doc_tokens:
            self.doc_tokens[doc_id] = len(docs[doc_id])
            self.total_tokens += self.doc_tokens[doc_id]
        entry = InvertedIdxDocEntry(doc_id, term, docs[doc_id], self.doc_tokens[doc_id])
        if term in self.idx:
            self.idx[term].add(entry)
        else:
            self.idx[term] = set([entry])

    def local_unigram(self, term, doc_id):
        """
        This will return the unigram probabilistic model for a given term within a document
        :param term: term for which the probability shall be returned
        :param doc_id: document concerning
        :return: the probability for term t in document t with Jelinek Mercer smoothing
        """
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
        """
        :param term: The term for which the probability is required
        :return: Probability of term in the document collection (based on the index)
        """
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
