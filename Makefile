.PHONY: test lint coverage clean

test:
	pytest -v

lint:
	ruff check . --select E,F,W --ignore E501

coverage:
	pytest --cov=quantum_simulator --cov-report=term-missing --cov-report=html

clean:
	rm -rf __pycache__ .pytest_cache htmlcov .coverage
