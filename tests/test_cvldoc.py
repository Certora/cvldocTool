from src.CVLDoc import cvldoc_to_json

import json
from pathlib import Path

from deepdiff import DeepDiff
import pytest


SPECS = list(Path(__file__).parent.rglob('*.spec'))


def __file_contents_as_json(path: Path) -> dict:
    with open(path, 'r+') as f:
        content = f.read()

    content.replace('\r\n', '\n')  # normalize line endings
    return json.loads(content)


def __get_diff(absolute_spec_path: Path) -> DeepDiff:
    expected_path = Path(str(absolute_spec_path).replace('.spec', '-expected.json'))
    expected_json = __file_contents_as_json(expected_path)

    output_path = Path(str(absolute_spec_path).replace('.spec', '-cvldoc.json'))
    output_json = __file_contents_as_json(output_path)
    output_path.unlink()

    return DeepDiff(expected_json, output_json, ignore_order=False)



@pytest.mark.parametrize('spec_path', SPECS, ids=[str(s.relative_to(__file__)) for s in SPECS])
def test_cvldoc_generation(spec_path: Path):
    args = ['-u', str(spec_path)]
    cvldoc_to_json.main(args)

    if diff := __get_diff(spec_path):
        assert 0, diff.pretty()
