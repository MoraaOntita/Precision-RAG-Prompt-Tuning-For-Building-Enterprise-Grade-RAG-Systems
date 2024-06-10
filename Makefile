# Original tasks
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

# Docker-related tasks
build_prompt_generation_service:
	docker build -t prompt_generation_service ./path/to/prompt_generation_service

build_automatic_evaluation_service:
	docker build -t automatic_evaluation_service ./path/to/automatic_evaluation_service

build_prompt_testing_and_ranking_service:
	docker build -t prompt_testing_and_ranking_service ./path/to/prompt_testing_and_ranking_service

build_all: build_prompt_generation_service build_automatic_evaluation_service build_prompt_testing_and_ranking_service

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose down && docker-compose up -d

logs:
	docker-compose logs -f

# Clean up Docker containers, images, and volumes
clean:
	docker-compose down --volumes --rmi all
	docker system prune -f

# Rebuild and restart all services
rebuild: clean build_all up

# Test target
test:
	python -m unittest discover tests

.PHONY: all text_extraction load_texts create_metadata chunk_texts embed_texts upsert_embeddings \
	build_prompt_generation_service build_automatic_evaluation_service build_prompt_testing_and_ranking_service \
	build_all up down restart logs clean rebuild test

