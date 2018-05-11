pragma solidity ^0.4.19;

import "./F11/C2.sol";
import ".\math\SafeMath8.sol";
import ".\math\SafeMath16.sol";
import ".\math\SafeMath24.sol";
import ".\math\SafeMath32.sol";
import ".\math\SafeMath.sol";

contract C2 is C3 {
    using SafeMath8 for uint8;
    using SafeMath16 for uint16;
    using SafeMath24 for uint24;
    using SafeMath32 for uint32;
    using SafeMath for uint;
    struct S2 {
        uint24 v1;
    }

    S2[] public s2;

    mapping(uint32 => address) public s2ToOwner;

    function copy() external view returns(S1[]) {
        for (uint i=0; i < s1ToOwner.length; i.add(1)) {
            s2[i].v1=s2[i].v1.mul(s1[i].v1.sub(s1[i].v1.add(s1[i].v1.div(s1[i].v1))));
        }
    }

}