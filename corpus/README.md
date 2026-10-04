# Attributed evidence corpus

[`sources.json`](sources.json) contains **12 project-authored factual summaries attributed to six official Rick Riordan pages**. They are short original paraphrases, not book excerpts or website quotations. Claims were checked against the page attached to each record; attribution applies to that summary, not to the application's separate database facts.

## Source coverage

| Official source | Record IDs |
|---|---|
| [Percy Jackson](https://rickriordan.com/character/percy-jackson/) | `percy-parentage`, `percy-roles` |
| [Annabeth Chase](https://rickriordan.com/character/annabeth-chase/) | `annabeth-family` |
| [Poseidon](https://rickriordan.com/character/poseidon-2/) | `poseidon-sea` |
| [Athena](https://rickriordan.com/character/athena-2/) | `athena-wisdom` |
| [Camp Half-Blood cabins](https://rickriordan.com/extra/camp-half-blood-cabins/) | `percy-water-powers`, `annabeth-strategy`, `camp-hermes-guests`, `camp-hera-tribute` |
| [Percy Jackson and the Olympians](https://rickriordan.com/series/percy-jackson-and-the-olympians/) | `lightning-thief-quest`, `sea-monsters-camp`, `labyrinth-invasion` |

Coverage includes selected parentage, relationships, roles, powers, cabins, and three quest synopses. It is deliberately narrow, not an exhaustive or authoritative reference. No fan-wiki material or generated lore is used to fill gaps.

## Record contract

The UTF-8 JSON array is validated by `Source` in [retrieval.py](../retrieval.py):

- `source_id`, `title`, `reference`, and `text`: required nonblank strings.
- `source_url`: required HTTP(S) URL without credentials.
- `provenance`: required literal `"attributed_summary"`.
- `tags`: optional list of strings, defaulting to an empty list.

Extra fields and duplicate source IDs are rejected. Keep IDs stable when editing a summary. Any future change should retain only claims supported by that record's linked page; database coverage is not a reason to invent evidence.

## Retrieval

```python
from retrieval import retrieve

for result in retrieve("Who are Percy Jackson's parents?", top_k=3):
    print(result.source.source_id, result.score)
    print(result.source.source_url)
    print(result.source.text)
```

TF-IDF cosine similarity ranks title, text, and tags. Matching ignores case, punctuation, and a small set of common English words. Results contain the complete record and similarity score, ordered by descending score and then source ID. Only positive matches are returned, up to `top_k`.

Blank or unmatched queries return `[]`; invalid query types, limits, or corpus records raise errors. No database, indexing command, embeddings, or model server is required for retrieval. The corpus is loaded and scored on each call; `corpus_path` can select another JSON file.

Scores measure lexical similarity, not factual confidence. The [offline evaluation](../evaluation/results.json) retains a known paraphrase miss: “Which hero can stay submerged without needing air?” fails to retrieve `percy-water-powers`. Evaluation cases and corpus should not be silently adjusted to conceal such failures.
