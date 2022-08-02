/**
 * @title testing the natspec parser.
 * @notice  This is made by Gabriel  it contains all
 * known tags
 **/
methods {
    get5() returns uint envfree
    init_state() envfree
    setX(uint256) envfree
    getX() returns uint envfree
    getXCanRevert(uint256) returns uint envfree
    twoReturns(uint256) returns (uint256,uint256) envfree
    threeReturns(uint256,uint256) returns (uint256,uint256,uint256)
}

/**
 * @title callGet5 function calling get5
 * @notice no parameters
 **/
function callGet5() {
    assert get5() == 5;
}

/**
 * @title takeTwoEnvs function
 * @param e1 - first environment
 * @param e2 - second environment
 **/
function takeTwoEnvs(env e1, env e2) {
    require e1.msg.value == 0;
    require e1.msg.sender == e2.msg.sender;
}

/**
 * @title my_invariant invariant!
 * @notice ensuring get5 is always equal 5
 **/
invariant my_invariant() get5() == 5 {
    preserved init_state() {
        require getX() == 20;
    }
}

rule wrapper() {
    callGet5();
    assert true;
}

rule inlineInvoke() {
    uint n;
    // invoke as a command
    setX(n);
    // invoke as an expression
    assert getX() == n;
}

rule inlineInvokeCanRevert() {
    uint n;
    uint m;
    // invoke as a command
    setX(n);
    // invoke as an expression
    assert getXCanRevert@withrevert(m) == n;
}

rule inlineInvokeCanRevertSafe() {
    uint n;
    uint m;
    // invoke as a command
    setX(n);
    // invoke as an expression
    assert getXCanRevert@norevert(m) == n;
}

rule parametric(method f) {
    env e;
    calldataarg args;
    f(e, args);
    assert true;
}

rule parametricWithRevert(method f) {
    env e;
    calldataarg args;
    f@withrevert(e, args);
    assert !lastReverted;
}

rule parametricNoRevert(method f) {
    env e;
    calldataarg args;
    f@norevert(e, args);
    assert !lastReverted;
}

rule twoReturns(uint256 n) {
    uint256 x;
    uint256 nPlusX;
    require n < 107982;
    x, nPlusX = twoReturns(n);
    require x < 123549817;
    assert nPlusX == n + x;
}

rule threeReturns(uint256 n, uint256 m) {
    env e;
    uint256 nPlusX;
    uint256 nPlusXPlusM;
    uint256 x;
    x, nPlusX, nPlusXPlusM = threeReturns(e, n, m);
    require x < 10987098;
    require n < 150293879209;
    require m < 1203958240;
    assert nPlusX == x + n;
    assert nPlusXPlusM == nPlusX + m;
}

rule multipleEnvToCVLFunction(env e1, env e2) {
    takeTwoEnvs(e1, e2);
    assert e1.msg.value == 0 && e1.msg.sender == e2.msg.sender;
}