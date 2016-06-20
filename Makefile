lint:
	flake8 testimony

package:
	python setup.py sdist bdist_wheel --universal

package-clean:
	rm -rf build dist testimony.egg-info

publish: package
	twine upload dist/*
test:
	@./tests/test_testimony.sh | diff tests/sample_output.txt -

.PHONY: package package-clean publish test
