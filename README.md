# CVLDoc
CLI interface for [`cvldoc_parser`](https://github.com/Certora/cvldoc_parser), compatible with Linux (x64), macOS (Intel/ARM) and Windows (x64). Uses `cvldoc_parser` to dump a `.spec` file's `CVLDoc` comments to JSON, along with additional metadata.

# Installation
Current versions of this tool (2.0 and later) are only available on Test `PyPi` and can be installed by running

`pip install --pre --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple CVLDoc`

Alternatively, it can be installed locally (with `pip`).

Earlier versions (1.x) are no longer maintained.

# Usage

```
cvldoc [-h] [-u] [-v] [--version] input_files [input_files ...]

options:
  -h, --help            show help message and exit
  -u, --include_undocumented
                        include parsed elements that have no CVLDoc block
  -v, --verbose         increase output verbosity
  --version             show program's version number and exit
```

