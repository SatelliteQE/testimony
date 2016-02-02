echo "==============="
echo "= auto report ="
echo "==============="
echo
testimony -n auto tests

echo
echo "==============="
echo "= bugs report ="
echo "==============="
echo
testimony -n bugs tests

echo
echo "================="
echo "= manual report ="
echo "================="
echo
testimony -n manual tests

echo
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
echo "==============="
echo "= tags report ="
echo "==============="
echo
testimony -n tags tests

echo
echo "============================="
echo "= validate_docstring report ="
echo "============================="
echo
testimony -n validate_docstring tests
