# Backend Dependency Inventory (Grouped & With Documentation Links)

## 1. Web Framework & API Layer
| Package | Purpose | URL |
|--------|---------|-----|
| fastapi | Async Python web API framework | https://pypi.org/project/fastapi/ |
| uvicorn[standard] | ASGI web server for FastAPI | https://pypi.org/project/uvicorn/ |

## 2. Authentication & User Management
| Package | Purpose | URL |
|--------|---------|-----|
| fastapi-users[oauth,sqlalchemy] | User auth, OAuth, sessions, SQLAlchemy integration | https://pypi.org/project/fastapi-users/ |
| validators | Validation for emails, URLs, IPs | https://pypi.org/project/validators/ |

## 3. Database, ORM & Migrations
| Package | Purpose | URL |
|--------|---------|-----|
| asyncpg | High-performance async PostgreSQL driver | https://pypi.org/project/asyncpg/ |
| pgvector | Vector similarity search support for Postgres | https://pypi.org/project/pgvector/ |
| alembic | SQLAlchemy database schema migrations | https://pypi.org/project/alembic/ |

## 4. Background Processing & Queueing
| Package | Purpose | URL |
|--------|---------|-----|
| celery[redis] | Distributed task queue | https://pypi.org/project/celery/ |
| flower | Celery monitoring dashboard | https://pypi.org/project/flower/ |
| redis | Redis Python client | https://pypi.org/project/redis/ |

## 5. Document Ingestion, Parsing & OCR
| Package | Purpose | URL |
|--------|---------|-----|
| docling | AI-based document parsing + OCR | https://pypi.org/project/docling/ |
| pypdf | PDF text extraction & merging | https://pypi.org/project/pypdf/ |
| unstructured-client | Unstructured.io API client | https://pypi.org/project/unstructured-client/ |
| unstructured[all-docs] | Full unstructured document ingestion | https://pypi.org/project/unstructured/ |
| markdownify | Convert HTML → Markdown | https://pypi.org/project/markdownify/ |

## 6. NLP, Embeddings, Vector Search & Reranking
| Package | Purpose | URL |
|--------|---------|-----|
| sentence-transformers | Embedding models for search & NLP | https://pypi.org/project/sentence-transformers/ |
| spacy | NLP toolkit (tokenization, NER, POS) | https://pypi.org/project/spacy/ |
| en-core-web-sm | spaCy English language model | https://github.com/explosion/spacy-models |
| rerankers[flashrank] | Reranking models for retrieval | https://pypi.org/project/rerankers/ |
| langchain-community | LangChain integrations | https://pypi.org/project/langchain-community/ |
| langchain-unstructured | LangChain → Unstructured bridge | https://pypi.org/project/langchain-unstructured/ |
| langgraph | Build LLM agent workflows/graphs | https://pypi.org/project/langgraph/ |
| langchain-litellm | LiteLLM + LangChain integration | https://pypi.org/project/langchain-litellm/ |
| litellm | Unified client for many LLM providers | https://pypi.org/project/litellm/ |
| faster-whisper | Fast Whisper ASR transcription | https://pypi.org/project/faster-whisper/ |
| pgvector | Vector search for Postgres | https://pypi.org/project/pgvector/ |
| chonkie[all] | Chunk text for LLMs | https://pypi.org/project/chonkie/ |

## 7. LLM / AI Cloud Services
| Package | Purpose | URL |
|--------|---------|-----|
| llama-cloud-services | LlamaIndex cloud-based vector + embedding tools | https://pypi.org/project/llama-cloud-services/ |
| tavily-python | Tavily AI-powered web search | https://pypi.org/project/tavily-python/ |
| linkup-sdk | Linkup AI/ML platform SDK | https://pypi.org/project/linkup-sdk/ |
| firecrawl-py | Firecrawl AI web crawling | https://pypi.org/project/firecrawl-py/ |

## 8. Browser Automation & Crawling
| Package | Purpose | URL |
|--------|---------|-----|
| playwright | Browser automation (Chromium/Firefox/WebKit) | https://pypi.org/project/playwright/ |
| firecrawl-py | AI web crawler & scraper | https://pypi.org/project/firecrawl-py/ |

## 9. Multimedia / Audio / Video Processing
| Package | Purpose | URL |
|--------|---------|-----|
| soundfile | Read/write WAV, FLAC, and OGG | https://pypi.org/project/soundfile/ |
| python-ffmpeg | Python interface to FFmpeg | https://pypi.org/project/python-ffmpeg/ |
| static-ffmpeg | Portable FFmpeg binaries | https://pypi.org/project/static-ffmpeg/ |
| kokoro | Text-to-speech synthesis | https://pypi.org/project/kokoro/ |
| faster-whisper | Voice-to-text transcription | https://pypi.org/project/faster-whisper/ |

## 10. Social, Messaging & External Integrations
| Package | Purpose | URL |
|--------|---------|-----|
| discord-py | Discord bot API client | https://pypi.org/project/discord-py/ |
| slack-sdk | Slack API client | https://pypi.org/project/slack-sdk/ |
| notion-client | Notion API client | https://pypi.org/project/notion-client/ |
| github3.py | GitHub REST API client | https://pypi.org/project/github3.py/ |
| youtube-transcript-api | Fetch YouTube transcripts | https://pypi.org/project/youtube-transcript-api/ |

## 11. Google Cloud / Workspace Integrations
| Package | Purpose | URL |
|--------|---------|-----|
| google-api-python-client | Client for Google APIs | https://pypi.org/project/google-api-python-client/ |
| google-auth-oauthlib | OAuth support for Google auth | https://pypi.org/project/google-auth-oauthlib/ |

## 12. Search & Indexing
| Package | Purpose | URL |
|--------|---------|-----|
| elasticsearch | Elasticsearch/OpenSearch Python client | https://pypi.org/project/elasticsearch/ |
| rerankers | Reranking for search relevance | https://pypi.org/project/rerankers/ |
| pgvector | Vector search for Postgres | https://pypi.org/project/pgvector/ |

## 13. Data Processing & Utility Libraries
| Package | Purpose | URL |
|--------|---------|-----|
| numpy | Numerical computing | https://pypi.org/project/numpy/ |
| markdownify | HTML → Markdown | https://pypi.org/project/markdownify/ |
| chonkie | Chunk text for LLMs | https://pypi.org/project/chonkie/ |
