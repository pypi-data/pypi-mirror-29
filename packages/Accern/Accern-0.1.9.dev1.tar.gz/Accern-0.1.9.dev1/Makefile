help:
	@echo "The following make targets are available:"
	@echo "dev	install all deps for dev env"
	@echo "docs	create pydocs for all relveant modules"
	@echo "test	run all tests with coverage"

clean:
	rm -rf dist/*

dev:
	pip install coverage
	pip install codecov
	pip install pylint
	pip install twine
	pip install -e .

docs:
	$(MAKE) -C docs html

package:
	python setup.py sdist
	python setup.py bdist_wheel

test:
	coverage run -m unittest discover
	coverage html
