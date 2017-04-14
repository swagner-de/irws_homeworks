
class InvertedIdxDocEntry():

    def __init__(self, doc_id, term, docs):
        self.doc_id = doc_id
        self.tf = docs[doc_id].count(term)
        self.doc_tokens = len(docs[doc_id])

    @property
    def unigramm_model(self):
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

    def total_occurences(self, term):
        """
        :param term: the term for which the occurences shall be counted in the index
        :return: the total number of occurences in all documents
        """
        occurences = 0
        try:
            for doc in self.idx[term]:
                occurences += doc.tf
            return occurences
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

    def local_unigramm(self, term, doc_id):
        try:
            docs = self.idx[term]
            for doc in docs:
                if doc.doc_id == doc_id:
                    return doc.unigramm_model
        except KeyError:
            return 0

    def global_unigramm(self, term):
        return self.total_occurences(term) / self.total_tokens

    def prefilter_docs(self, query_terms):
        relevant_docs = set()
        for term in query_terms:
            try:
                for entry in self.idx[term]:
                    relevant_docs.add(entry.doc_id)
            except KeyError:
                pass
        return relevant_docs

def build_local_unigram(doc_id, docs, inv_idx):
    unigramm = {}
    for term in set(docs[doc_id]):
        unigramm[term] = inv_idx.local_unigramm(term, doc_id)
    return unigramm

def build_global_unigram(inv_idx):
    unigramm = {}
    for key in inv_idx.idx:
        unigramm[key] = inv_idx.global_unigramm(key)
    return unigramm
