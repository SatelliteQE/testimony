echo "================"
echo "= print report ="
echo "================"
echo
testimony -n print tests

echo
echo "=================="
echo "= summary report ="
echo "=================="
echo
testimony -n summary tests

echo
echo "============================="
echo "= validate_docstring report ="
echo "============================="
echo
testimony -n validate tests

echo
echo "=========================="
echo "= validate_values report ="
echo "=========================="
echo
testimony -n --tokens="Status,Feature" --minimum-tokens="Status,Feature" --token-configs=tests/validate-values.yaml validate-values tests
