import json
import os
import sys
import inflection
import cvldoc_parser
from cvldoc_parser import CvlElement, DocumentationTag, AstKind, TagKind
from argparse import ArgumentParser
from typing import Dict, List, Any, Optional
from loguru import logger
from pathlib import Path


def write_to_file(path: Path, path_dicts: List[Dict[str, Any]]):
    if not path_dicts:
        return

    json_string = json.dumps(path_dicts, indent=4)

    input_filename, _ = os.path.splitext(path)
    output_filename = os.path.join(input_filename + "-cvldoc" + ".json")

    with open(output_filename, "w") as json_file:
        json_file.write(json_string)


def handle_freeform_comment(cvl_element: CvlElement) -> Dict[str, str]:
    comment_text = cvl_element.ast.data["text"]
    if comment_text:
        return {"type": "text", "text": comment_text}
    else:
        return {}


def handle_element(
    cvl_element: CvlElement, include_undocumented: bool
) -> Dict[str, str]:
    if cvl_element.ast.kind == AstKind.FreeFormComment:
        return handle_freeform_comment(cvl_element)

    if not cvl_element.doc and not include_undocumented:
        return {}

    element_dict: Dict[str, Any] = {
        "content": cvl_element.raw(),
        "type": str(cvl_element.ast.kind),
    }

    if name := cvl_element.element_name():
        element_dict["id"] = name
        element_dict["title"] = inflection.humanize(inflection.titleize(name))

    if params := cvl_element.element_params():
        element_dict["params"] = [{"type": type, "name": name} for type, name in params]

    if returns := cvl_element.element_returns():
        element_dict["return"] = {"type": returns}

    for doc_tag in cvl_element.doc:
        handle_tag(element_dict, doc_tag)

    return element_dict


def handle_tag(doc_dict: Dict[str, Any], tag: DocumentationTag):
    """
    handle a single documentation tag.
    @dev tags will be joined to a single tag.
    """

    if tag.kind in [TagKind.Title, TagKind.Notice, TagKind.Formula]:
        doc_dict[str(tag.kind)] = tag.description
    elif tag.kind == TagKind.Dev:
        dev_description = tag.description.strip()
        if "dev" in doc_dict:
            doc_dict["dev"] += "\n"
            doc_dict["dev"] += dev_description
        else:
            doc_dict["dev"] = dev_description
    elif tag.kind == TagKind.Return:
        doc_dict.setdefault("return", {}).update({"comment": tag.description})
    elif tag.kind == TagKind.Param:
        params = doc_dict.setdefault("params", {})

        if name_and_description := tag.param_name_and_description():
            param_name, param_description = name_and_description
            if param := find_param_by_name(params, param_name):
                param["comment"] = param_description


def find_param_by_name(
    params: List[Dict[str, str]], param_name: str
) -> Optional[Dict[str, str]]:
    for param in params:
        if param["name"] == param_name:
            return param
    return None


def package_version(package_name: str) -> Optional[str]:
    """
    there might be better ways to do this,
    but that's as far as I'm willing to care about python idiosyncrasies
    """

    from distutils.core import run_setup
    from importlib import metadata

    # attempts to get version by querying `setup.py`, if it exists in a parent dir.
    # no side effects here - actual setup is stopped before any installation steps occur
    try:
        distribution = run_setup("./setup.py", stop_after="init")
        return distribution.get_version()
    except (FileNotFoundError, RuntimeError):
        pass

    # if this package is installed in current env, return the installed version
    # (even if this isn't where the script has been ran from!)
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        pass

    return None


def argument_parser() -> ArgumentParser:
    package_name = "CVLDoc"

    version = package_version(package_name)
    version_str = f"{package_name} {version}" if version else package_name

    parser = ArgumentParser(
        prog=package_name, description="export CVLDoc comments to JSON"
    )
    parser.add_argument(
        dest="input_files", help="path to input spec file(s) ", type=Path, nargs="+"
    )
    parser.add_argument(
        "-u",
        "--include_undocumented",
        help="include parsed elements that have no CVLDoc block",
        action="store_true",
    )
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    parser.add_argument("--version", action="version", version=version_str)

    # the following arguments are currently unimplemented
    # parser.add_argument(
    #     "-dev", "--development", help="produce developer report", action="store_true"
    # )
    # parser.add_argument(
    #     "-user", "--user", help="produce end user report", action="store_true"
    # )

    return parser


def init_logger(verbose: bool):
    logger.remove()  # remove default logger

    if verbose:
        logger_level = (
            "INFO"  # extend this if we wish to support severity as a program arg
        )

        logger_format = (
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<level>{message}</level>"
        )

        logger.add(sys.stderr, format=logger_format, level=logger_level)


def main(args: Optional[List[str]] = None):
    parsed_args = argument_parser().parse_args(args)

    init_logger(parsed_args.verbose)

    for path in parsed_args.input_files:
        logger.info(f"processing: {path}")

        try:
            cvl_elements = cvldoc_parser.parse(path)
        except OSError:
            logger.warning(f"skipping invalid file: {path}")
            continue
        except RuntimeError:
            logger.error(f"failed to parse file: {path}")
            continue

        path_dicts = []
        for element in cvl_elements:
            if processed := handle_element(element, parsed_args.include_undocumented):
                path_dicts.append(processed)

        write_to_file(path, path_dicts)

    logger.info("finished processing files")


if __name__ == "__main__":
    main()
