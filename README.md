# Solidity SafeMath Checker - check and fix if any math calculations in your solidity contracts don't use SafeMath
SafeMath is a solidity math library especially designed to support safe math operations: safe means that it prevents overflow when working with uint. You can find it in [zeppelin-solidity SafeMath](https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/math/SafeMath.sol).  
  
## Workflow  
Please copy the project to be checked to "./to_check" folder, the run:  
```shell  
python ./main.py  
```  
Then you can find the backup files in "./backup" folder, the new files applying SafeMath in "./to_check" folder.
  
## File Requirements  
1. All Solidity files in the project to be checked are named as "*.sol".
2. All SafeMath files in the project to be checked are named as "SafeMath*.sol", and their file names are the same as the uint type they protect from overflow. e.g., SafeMath8.sol is to protect the uint8 calculation.
3. SafeMath.sol is an exception of #2, it protects uint (uint256) from overflow.
4. All "*.sol" files are valid.
  
## Running environment  
* Windows, Linux  
  
## Software requirement  
* Python3 with Anaconda lib  
  
## Logic  
Take the files in "./example" folder as an example ("./example/backup" stores the files before running the program, "./example/to_check" stores the files after running):  
1. Copy all *.sol files (excluding SafeMath*.sol files) to "./backup" folder.  
2. Check all *.sol files (excluding SafeMath*.sol files) to record how many uint types are used.  
3. Check all SafeMath*.sol files, find out which uint types are used (from the result of #1) without SafeMath*.sol file. e.g., C1.sol defines a uint32 variable v1, but the are no SafeMath32.sol file in the project.  
4. According to the result of #2, create all missing SafeMath*.sol files in "./to_check/math" folder. e.g., create "./to_check/math/SafeMath32.sol" file.  
5. In each file of *.sol files (excluding SafeMath*.sol files):  
5.1. Import all SafeMath*.sol files, and add "using" statements. e.g., add "using SafeMath8 for uint8;".
5.2. Change all ++ to add(1), -- to sub(1). e.g., change "v1++" to "v1.add(1)".  

## Limitation
1. The program doesn't support the left operand of a math operator is integer literal. e.g., 3*a will be changed to 3.mul(a) which is invalid. 
2. The program doesn't support a statement with the left and right operands of a math operator across 2 lines. e.g.,
if (a>b
+1)
cannot be parsed correctly.
3. The program cannot protect the result of **, <<, >> from overflow.