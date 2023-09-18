from . import util
import os


def test_erc1155_burnable():
    util.check_single_file("customer_code/ERC1155Burnable.spec")


def test_erc1155_new():
    util.check_single_file("customer_code/ERC1155New.spec")


def test_erc1155_pausable():
    util.check_single_file("customer_code/ERC1155Pausable.spec")


def test_erc1155_supply():
    util.check_single_file("customer_code/ERC1155Supply.spec")


def test_governor_prevent_late_quorum():
    util.check_single_file("customer_code/GovernorPreventLateQuorum.spec")


def test_initializable():
    util.check_single_file("customer_code/Initializable.spec")
