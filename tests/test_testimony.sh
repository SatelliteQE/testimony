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
