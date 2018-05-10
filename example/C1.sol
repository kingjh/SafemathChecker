pragma solidity ^0.4.19;

contract C1 {
    uint32 v1=1;
    uint128 v2=1;
    uint v3=1;

    function randMod() internal returns(uint) {
        v1++;
        v1+=2;
        v1--;
        v1-=2;
        v1*=2;
        v1/=2;
        v1+=v1;
        for (uint16 i = 0; i < v3; i++) {
            if(((v1+2)*3 >= v1) || ((v2>=v2-v3) &&
                (v2+v1>=v2-v3))){
                v3-=v3*(v1-v2)/(v3-(v1+v2));
            }
        }
        return v1;
    }

}
