flake8:
	nosetests -d -v caspyr/tests/tests_flake8.py
testcoverage:
	nosetests -d -v caspyr --with-coverage --cover-erase --cover-package=caspyr --ignore-files="tests_(plotting|flake8)\.py"
testplotting:
	nosetests -d -v caspyr/tests/tests_plotting.py
test:
	@make flake8
	@make testcoverage
	@make testplotting
clean:
	find -name "*.py[co]" -exec rm \{} \;
	find -type d -name "__pycache__" -exec rm \{} \;
	rm -rf build/ dist/ caspyr.egg-info/ .coverage
build:
	python setup.py sdist --formats=gztar bdist_wheel
