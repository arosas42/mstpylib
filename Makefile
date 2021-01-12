all: clean
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf dist/
	rm -rf build/

install:
	su mstpylib -c "python3 -m twine upload --verbose --repository gitlab dist/*"