# Architecture
> Freshness date: <!-- update when architecture changes -->

## System Overview
```
Request -> main.py -> pipeline.py -> core/validator.py
                                  -> services/processor.py
                                  -> services/retriever.py (optional)
```

## Extension Points
| What to add | Where |
|---|---|
| New AI provider | services/client.py â€” implement ServiceClient Protocol |
| Semantic retrieval | services/retriever.py â€” replace _score_documents() |
| New endpoint | main.py |
| ML inference | New bounded context src/app/ml/ |

See docs/BOUNDED_CONTEXTS.md for module rules.
