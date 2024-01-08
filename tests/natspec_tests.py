import json
import src.CVLDoc.natspec_to_json as natspec_to_json
from deepdiff import DeepDiff
from pprint import pprint
from pathlib import Path
import os
import argparse


# parser = natspec_to_json.get_parser()
# args = parser.parse_args(test_args + filenames)
# natspec_to_json.natspec_to_json(args)



# run a single test file
def parse_test_dir_path() -> Path:
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='.', help='The path from which to look for tests.')
    return Path(parser.parse_args().path)


def omit_cr_from_file(filename):
    with open(filename, 'r+') as f:
        content = f.read()
        content = content.replace('\\r\\n', '\\n')
        f.seek(0, os.SEEK_SET)
        f.truncate(0)
        f.write(content)
        f.close()


def run_test_file(filename: str):
    test_args = ['-v', filename]

    parser = natspec_to_json.get_parser()
    args = parser.parse_args(test_args)
    natspec_to_json.natspec_to_json(args)
    input_filename, file_extension = os.path.splitext(filename)
    output_filename = os.path.join(input_filename + '-natspec' + '.json')
    expected_filename = os.path.join(input_filename + '-expected' + '.json')
    omit_cr_from_file(output_filename)
    omit_cr_from_file(expected_filename)
    file_output = open(output_filename)
    file_expected = open(expected_filename)
    output_data = json.load(file_output)
    expected_data = json.load(file_expected)
    diff = DeepDiff(expected_data, output_data)
    return diff


def test_full_contract():
    diff = run_test_file(str(Path('basic_tests/full_contract.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0

def test_invariant():
    diff = run_test_file(str(Path('basic_tests/invariant_test.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_function():
    diff = run_test_file(str(Path('basic_tests/function_test.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_rules():
    diff = run_test_file(str(Path('basic_tests/rules_test.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_methods():
    diff = run_test_file(str(Path('basic_tests/methods_test.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_definition():
    diff = run_test_file(str(Path('basic_tests/methods_test.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


# not supported yet.
# def test_using():
#    diff = run_test_file(str(Path('basic_tests/using_test.spec')))
#    if diff:
#        pprint(diff, indent=4)
#        assert 0
# def test_import():
#     diff = run_test_file(str(Path('basic_tests/import_test.spec')))
#     if diff:
#         pprint(diff, indent=4)
#         assert 0

def test_burnable():

    diff = run_test_file(str(Path('customer_code/ERC1155Burnable.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_new():

    diff = run_test_file(str(Path('customer_code/ERC1155New.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_pausable():
    diff = run_test_file(str(Path('customer_code/ERC1155Pausable.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_supply():
    diff = run_test_file(str(Path('customer_code/ERC1155Supply.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_governor():
    diff = run_test_file(str(Path('customer_code/GovernorPreventLateQuorum.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_initializable():
    diff = run_test_file(str(Path('customer_code/Initializable.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


if __name__ == '__main__':
    path = parse_test_dir_path()
    specs = path.rglob('*.spec')

    for spec in specs:
        diff = run_test_file(spec)
        if diff is not None:
            pprint(diff, indent=4)
