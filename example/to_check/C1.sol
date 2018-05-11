pragma solidity ^0.4.19;
import ".\math\SafeMath8.sol";
import ".\math\SafeMath16.sol";
import ".\math\SafeMath24.sol";
import ".\math\SafeMath32.sol";
import ".\math\SafeMath128.sol";
import ".\math\SafeMath.sol";

contract C1 {
    using SafeMath8 for uint8;
    using SafeMath16 for uint16;
    using SafeMath24 for uint24;
    using SafeMath32 for uint32;
    using SafeMath128 for uint128;
    using SafeMath for uint;
    uint32 v1=1;
    uint128 v2=1;
    uint v3=1;

    function randMod() internal returns(uint) {
        v1.add(1);
        v1=v1.add(2);
        v1.sub(1);
        v1=v1.sub(2);
        v1=v1.mul(2);
        v1=v1.div(2);
        v1=v1.add(v1);
        for (uint16 i = 0; i < v3; i.add(1)) {
            if((v1.add(2).mul(3)>= v1) || ((v2>=v2.sub(v3)) &&
                (v2.add(v1)>=v2.sub(v3**2)))){
                v3=v3.sub(v3.mul(v1.sub(v2)).div(v3.sub(v1.add(v2))));
            }
        }
        return v1;
    }

}