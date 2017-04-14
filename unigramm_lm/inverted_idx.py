
class InvertedIdxDocEntry():

    def __init__(self, doc_id, term, docs):
        self.doc_id = doc_id
        self.tf = docs[doc_id].count(term)
        self.doc_tokens = len(docs[doc_id])

    def __hash__(self):
        return self.doc_id

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __str__(self):
        return 'id:%s, tf:%s, total_tokens:%s' % (str(self.doc_id), str(self.tf), str(self.doc_tokens))


class InvertedIdx:

    def __init__(self):
        self.idx = {}

    def add_term(self, term, doc_id, docs):
        entry = InvertedIdxDocEntry(doc_id, term, docs)
        if term in self.idx:
            self.idx[term].add(entry)
        else:
            self.idx[term] = set([entry])

    def __str__(self):
        rep = ''
        for k, v in self.idx.items():
            vals = '; '.join([str(i) for i in v])
            rep += "'%s':\t%s\n" % (k, vals)
        return rep
