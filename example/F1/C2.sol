pragma solidity ^0.4.19;

contract C2 {
    uint8 v1=1;
    uint128 v2=1;
    uint v3=1;

    function randMod(uint _modulus) internal returns(uint) {
        v1++;
        v1--;
        v1+=2;
        v1-=2;
        v1*=2;
        v1/=2;
        v1+=v1;
        if((v1<=v1+2) || (v2>=v2-v3)){
            v3-=v3*(v1-v2)/(v3-(v1+v2));
        }
        return v1;
    }

}
