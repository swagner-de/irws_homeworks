class Result:

    def __init__(self, doc_id, doc_liklihood):
        self.doc_id = doc_id
        self.doc_likelihood = doc_liklihood

    def __str__(self):
        return 'docId: %s, likelihood: %s' % (self.doc_id, self.doc_likelihood)


class Query:

    def __init__(self, query_terms, docs, inv_idx):
        self.query_terms = query_terms
        self. docs = docs
        self.inv_idx = inv_idx

    def __str__(self):
        return 'Query on %s documents with query terms "%s"' % (str(len(self.docs)), ', '.join(self.query_terms))

    @property
    def prefiltered_docs(self):
        relevant_docs = set()
        for term in self.query_terms:
            try:
                for entry in self.inv_idx.idx[term]:
                    relevant_docs.add(entry.doc_id)
            except KeyError:
                pass
        return relevant_docs

    def doc_likelihood(self):
        ranked = []
        for id in self.prefiltered_docs:
            res_doc = Result(id, 1)
            for term in self.query_terms:
                if term in self.query_terms:
                    res_doc.doc_likelihood *= self.inv_idx.local_unigram(term, id)
            ranked.append(res_doc)
        return sorted(ranked, key=lambda x: x.doc_likelihood, reverse=True)
