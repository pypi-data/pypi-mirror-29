clean:
	rm -rf dist/
	rm -rf build/

build:
	python setup.py sdist

install: clean build
	pip install dist/*

uninstall:
	pip uninstall -y junc

upload: clean build
	twine upload dist/*
