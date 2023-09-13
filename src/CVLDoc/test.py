import json
from . import cvldoc_to_json
from deepdiff import DeepDiff
from pathlib import Path
import os

tests_dir = os.path.join(os.path.dirname(__file__), "../../tests")

basic_tests = [
    os.path.join(tests_dir, "basic_tests/definition_test.spec"),
    os.path.join(tests_dir, "basic_tests/full_contract.spec"),
    os.path.join(tests_dir, "basic_tests/function_test.spec"),
    os.path.join(tests_dir, "basic_tests/import_test.spec"),
    os.path.join(tests_dir, "basic_tests/invariant_test.spec"),
    os.path.join(tests_dir, "basic_tests/methods_test.spec"),
    os.path.join(tests_dir, "basic_tests/rules_test.spec"),
    os.path.join(tests_dir, "basic_tests/use_test.spec"),
    os.path.join(tests_dir, "basic_tests/using_test.spec"),
]

customer_code_tests = [
    os.path.join(tests_dir, "customer_code/ERC1155Burnable.spec"),
    os.path.join(tests_dir, "customer_code/ERC1155New.spec"),
    os.path.join(tests_dir, "customer_code/ERC1155Pausable.spec"),
    os.path.join(tests_dir, "customer_code/ERC1155Supply.spec"),
    os.path.join(tests_dir, "customer_code/GovernorPreventLateQuorum.spec"),
    os.path.join(tests_dir, "customer_code/Initializable.spec"),
]


def file_contents_as_json(path: Path):
    with open(path, "r+") as f:
        content = f.read()

    content.replace("\r\n", "\n")  # normalize line endings
    return json.loads(content)


def get_diff(spec_path) -> DeepDiff:
    input_filename, _ = os.path.splitext(spec_path)

    expected_path = os.path.join(input_filename + "-expected" + ".json")
    expected_json = file_contents_as_json(expected_path)

    output_path = os.path.join(input_filename + "-cvldoc" + ".json")
    output_json = file_contents_as_json(output_path)
    os.remove(output_path)

    diff = DeepDiff(expected_json, output_json)
    return diff


def check_single_file(spec_path: str):
    args = ["-u", spec_path]
    cvldoc_to_json.main(args)

    if diff := get_diff(spec_path):
        print(diff.pretty())
        assert 0

    def definition_test():
        path = "basic_tests/definition_test.spec"
        check_single_file(path)

    def full_contract_test():
        path = "basic_tests/full_contract.spec"
        check_single_file(path)

    def function_test():
        path = "basic_tests/function_test.spec"
        check_single_file(path)

    def import_test():
        path = "basic_tests/import_test.spec"
        check_single_file(path)

    def invariant_test():
        path = "basic_tests/invariant_test.spec"
        check_single_file(path)

    def methods_test():
        path = "basic_tests/methods_test.spec"
        check_single_file(path)

    def rules_test():
        path = "basic_tests/rules_test.spec"
        check_single_file(path)

    def use_test():
        path = "basic_tests/use_test.spec"
        check_single_file(path)

    def using_test():
        path = "basic_tests/using_test.spec"
        check_single_file(path)

    def ERC1155Burnable_test():
        path = "customer_code/ERC1155Burnable.spec"
        check_single_file(path)

    def ERC1155New_test():
        path = "customer_code/ERC1155New.spec"
        check_single_file(path)

    def ERC1155Pausable_test():
        path = "customer_code/ERC1155Pausable.spec"
        check_single_file(path)

    def ERC1155Supply_test():
        path = "customer_code/ERC1155Supply.spec"
        check_single_file(path)

    def GovernorPreventLateQuorum_test():
        path = "customer_code/GovernorPreventLateQuorum.spec"
        check_single_file(path)

    def Initializable_test():
        path = "customer_code/Initializable.spec"
        check_single_file(path)


def check_all():
    for path in basic_tests + customer_code_tests:
        check_single_file(path)

    print("finished running all tests")


if __name__ == "__main__":
    check_all()
