.PHONY: clean clean-pyc clean-build


GUIDE_API_HOST=http://localhost:5002
ES_HOST=http://localhost:9202

TEST_OPTIONS= -s --cov-report term --cov=guide_search  --cov-report=html:cover

TESTDEBUG_OPTIONS= -s
# pytest switches:
# -s : disable capture of stdout & stdin so can attach debugger
# -v : show full diff

test: clean-pyc
	@export GUIDE_API_HOST="${GUIDE_API_HOST}"; \
	export ES_HOST="${ES_HOST}"; \
	python3 -m pytest ${TEST_OPTIONS} unit_tests/*

testdebug:
	@export GUIDE_API_HOST="${GUIDE_API_HOST}"; \
	export ES_HOST="${ES_HOST}"; \
	python3 -m pytest ${TESTDEBUG_OPTIONS} unit_tests/*



dist: clean-build
	@python setup.py sdist bdist_wheel

clean: clean-build clean-pyc

clean-build:
	-@rm -fr build/
	-@rm -fr dist/
	-@rm -fr *.egg-info
	-@rm -fr cover/
	-@rm -fr test-reports

clean-pyc:
	-@find . -name '*.pyc' -exec rm -f {} +
	-@find . -name '*.pyo' -exec rm -f {} +
	-@find . -name '*~' -exec rm -f {} +
	-@find . -name '__pycache__' -exec rm -fr {} +

publish:
	@twine upload dist/*

