test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_pycodestyle_di pycodestyle data_import.py
assert_exit_code 0

run test_pycodestyle_tests pycodestyle tests.py
assert_exit_code 0

run test_overall python data_import.py --folder_name smallData \
--output_file out \
--sort_key hr_small.csv
assert_exit_code 0
rm out5.csv
rm out15.csv

run test_no_folder python data_import.py --folder_name garbage \
--output_file out \
--sort_key hr_small.csv
assert_exit_code 1

mkdir testfolder
touch noduphandle.csv
run test_no_duphandle python data_import.py --folder_name testfolder \
--output_file out \
--sort_key hr_small.csv
assert_exit_code 1
rm testfolder
