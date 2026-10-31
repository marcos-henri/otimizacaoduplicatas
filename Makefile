.PHONY: test bench bench-rapido bench-publicar limpar

test:
	python3 -m pytest

bench:
	python3 -m src.benchmark

bench-rapido:
	python3 -m src.benchmark --rapido

bench-publicar:
	python3 -m src.benchmark --publicar

limpar:
	rm -rf .pytest_cache __pycache__ src/__pycache__ tests/__pycache__
