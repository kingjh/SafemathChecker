pragma solidity ^0.4.19;
import "./math/SafeMath8.sol";
import "./math/SafeMath16.sol";

contract C3 {
    using SafeMath8 for uint8;
    using SafeMath16 for uint16;
       struct S1 {
               uint8 v1;
       }

       S1[] public s1;

       mapping(uint16 => address) public s1ToOwner;

}
