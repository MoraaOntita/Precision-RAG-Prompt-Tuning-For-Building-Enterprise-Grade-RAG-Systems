all: text_extraction load_texts create_metadata chunk_texts embed_texts upsert_embeddings

text_extraction:
	python scripts/text_extraction.py

load_texts:
	python scripts/load_texts.py

create_metadata:
	python scripts/create_metadata.py

chunk_texts:
	python scripts/chunk_texts.py

embed_texts:
	python scripts/embed_texts.py

upsert_embeddings:
	python scripts/upsert_embeddings.py


