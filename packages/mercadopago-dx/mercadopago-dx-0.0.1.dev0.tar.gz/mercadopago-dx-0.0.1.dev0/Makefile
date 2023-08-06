
all: wheel

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

sdist: clean-pyc
	python setup.py sdist

wheel: sdist
	python setup.py bdist_wheel
