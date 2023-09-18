import json
from typing import Optional
from src.CVLDoc import cvldoc_to_json
from deepdiff import DeepDiff
from pathlib import Path
import os

tests_dir = os.path.join(os.path.dirname(__file__))


def file_contents_as_json(path: Path) -> dict:
    with open(path, "r+") as f:
        content = f.read()

    content.replace("\r\n", "\n")  # normalize line endings
    return json.loads(content)


def get_diff(absolute_path) -> DeepDiff:
    input_filename, _ = os.path.splitext(absolute_path)

    expected_path = os.path.join(input_filename + "-expected" + ".json")
    expected_json = file_contents_as_json(expected_path)

    output_path = os.path.join(input_filename + "-cvldoc" + ".json")
    output_json = file_contents_as_json(output_path)
    os.remove(output_path)

    diff = DeepDiff(expected_json, output_json, ignore_order=False)
    return diff


def check_single_file(spec_path):
    absolute_path = os.path.join(tests_dir, spec_path)

    args = ["-u", absolute_path]
    cvldoc_to_json.main(args)

    if diff := get_diff(absolute_path):
        assert 0, diff.pretty()
