class Query:

    def __init__(self, query_terms, docs, inv_idx):
        self.query_terms = query_terms
        self. docs = docs
        self.inv_idx = inv_idx
        self.prefiltered_docs = inv_idx.prefilter_docs(self.query_terms)
        print(self.prefiltered_docs)