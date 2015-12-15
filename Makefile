test:
	@py.test --pep8 -v test_pyspin.py pyspin/

create:
	@python setup.py sdist bdist_wheel

upload:
	@python setup.py sdist bdist_wheel upload
