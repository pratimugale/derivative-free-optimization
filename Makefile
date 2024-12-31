install: 
	pip install .

uninstall:
	pip uninstall optimizers

run-test:
	python tests/test_module.py

test: install run-test