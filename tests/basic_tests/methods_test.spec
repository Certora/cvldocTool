//// # methods_test.spec - Natspec testing file for the methods statement.
//// # contains a few declarations of statements.


/**
 * @title mathematical helpe functions.
 * @notice get the  power of 10 n decimal format
 * @dev do not use this function on floating points.
 */
methods {
    function get10PowerDecimals(uint8) external returns(uint256) envfree;
}


/**
 * @title Specification for core ERC20 tokens.
 * @notice contains all ER20 Interface definitions.
 * @dev includes some extended  interfaces that is not implemented yet.
 */
methods {
	function balanceOf(address) external returns uint256;
	function transfer(address,uint256) external returns bool;
	function transferFrom(address, address, uint256) external returns bool;
	function approve(address, uint256) external returns bool;
	function allowance(address, address) external returns uint256;
	function totalSupply() external returns uint256;
	// Extended API - not implemented
	function mint(address,uint256) external returns bool;
	function burn(address,uint256) external;
	function owner() external returns address;
	function paused() external returns bool;
}
