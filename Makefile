help:
	@echo "Please use \`make <target>', where <target> is one of"
	@echo "  help           to show this message"
	@echo "  lint           to check the codebase for errors"
	@echo "  package        to generate installable Python packages"
	@echo "  package-clean  to remove generated Python packages"
	@echo "  publish        to upload dist/* to PyPi"
	@echo "  test           to run unit tests"

lint:
	flake8 testimony

package:
	python setup.py sdist bdist_wheel

package-clean:
	rm -rf build dist testimony.egg-info

publish: package
	twine upload dist/*

test:
	@./tests/test_testimony.sh | diff tests/sample_output.txt -

.PHONY: help lint package package-clean publish test
