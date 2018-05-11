pragma solidity ^0.4.19;

import "./F11/C2.sol";

contract C2 is C3 {
    struct S2 {
        uint24 v1;
    }

    S2[] public s2;

    mapping(uint32 => address) public s2ToOwner;

    function copy() external view returns(S1[]) {
        for (uint i=0; i < s1ToOwner.length; i++) {
            s2[i].v1*=s1[i].v1-(s1[i].v1+s1[i].v1/s1[i].v1);
        }
    }

}
