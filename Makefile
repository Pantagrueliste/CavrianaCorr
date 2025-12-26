# Makefile for CavrianaCorr development tasks

.PHONY: help install test lint validate parse heatmap clean

help:
	@echo "Available targets:"
	@echo "  install    - Install Python dependencies"
	@echo "  test       - Run unit tests"
	@echo "  lint       - Run pre-commit hooks on all files"
	@echo "  validate   - Run all validation scripts"
	@echo "  parse      - Parse letters and generate metadata CSV"
	@echo "  heatmap    - Generate heatmap visualization"
	@echo "  clean      - Remove generated files and caches"

install:
	pip install -r requirements.txt
	pip install pre-commit
	pre-commit install

test:
	pytest tests/ -v

lint:
	pre-commit run --all-files

validate:
	python scripts/validate_references.py
	python scripts/validate_consistency.py

parse:
	python scripts/letter_parser.py

heatmap:
	python scripts/generate_heatmap.py

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc */*.pyc
	rm -rf .mypy_cache
