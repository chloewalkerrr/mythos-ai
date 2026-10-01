# Local evidence corpus

`sources.json` is a UTF-8 JSON array with one curated passage per record:
`source_id`, `title`, `reference`, and `text` are required nonblank strings;
`tags` is an optional list of strings. IDs must be unique. Keep an ID stable
when editing its passage; give a new passage a new ID.

The six starter passages are project-authored summaries of records in
`scripts/populate_data.py`, not quotations from books or independently
verified primary sources. Each reference identifies the underlying records.
Percy Jackson setting notes are labeled separately from mythology notes.
Add further short, self-contained passages with honest source references to
this same file; no indexing command or running database is required.

```python
from retrieval import retrieve

for result in retrieve("Which monster turns people to stone?", top_k=2):
    print(result.source.source_id, result.score)
    print(result.source.reference)
    print(result.source.text)
```

Retrieval uses TF-IDF cosine similarity over title, text, and tags. It ignores
case, punctuation, and a small set of common English words. Results contain
the complete source record and a similarity score, sorted by descending score
and then source ID for ties. Only positive matches are returned, up to `top_k`.
Blank/unmatched queries return `[]`; non-string queries raise `TypeError` and
invalid result limits raise `ValueError`. Malformed corpus records are rejected.

This is lexical matching, without synonym expansion, embeddings, or generated
answers. A score measures word overlap, not factual confidence. The tiny corpus
is loaded and scored on each call; `corpus_path` can select another JSON file.
