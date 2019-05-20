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
echo "========================================="
echo "= validate_docstring with config report ="
echo "========================================="
echo
testimony -n --config tests/config-full.yaml validate tests

echo
echo "===================================="
echo "= config should overwrite defaults ="
echo "===================================="
echo
echo -n "default summary report length: "
testimony -n summary tests |wc -l
echo -n "--config summary report length: "
testimony -n --config tests/config-basic.yaml summary tests |wc -l

echo
echo "===================================="
echo "= tokens should overwrite defaults ="
echo "===================================="
echo
echo -n "default summary report length: "
testimony -n summary tests |wc -l
echo -n "--tokens summary report length: "
testimony -n --tokens "bz,assert,feature,test" summary tests |wc -l

echo
echo "============================================"
echo "= minimum-tokens should overwrite defaults ="
echo "============================================"
echo
echo -n "default summary report length: "
testimony -n summary tests |wc -l
echo -n "--minimum-tokens summary report length: "
testimony -n --minimum-tokens "test" summary tests |wc -l

echo
echo "=========================================================="
echo "= tokens and minimum-tokens should be merged with config ="
echo "=========================================================="
echo
echo -n "default summary report length: "
testimony -n summary tests |wc -l
echo -n "--tokens --minimum-tokens --config summary report length: "
testimony -n --tokens "bz" --minimum-tokens "status" --config tests/config-basic.yaml summary tests |wc -l
