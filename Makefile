test:
	@./tests/test_testimony.sh | diff tests/sample_output.txt -

.PHONY: test
