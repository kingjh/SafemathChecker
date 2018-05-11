pragma solidity ^0.4.19;

contract C3 {
    struct S1 {
        uint8 v1;
    }

    S1[] public s1;

    mapping(uint16 => address) public s1ToOwner;

}
