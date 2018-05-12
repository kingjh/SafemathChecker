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
Please note there will be no SafeMath256.sol file but SafeMath.sol, which protects uint (uint256) from overflow.
4. All "*.sol" files are valid.
  
## Running environment  
* Windows, Linux  
  
## Software requirement  
* Python3 with Anaconda installed
  
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
3. The program cannot protect the result of **, << from overflow. You can find how to protect them in [Avoiding Integer Overflows: SafeMath Isn't Enough](https://programtheblockchain.com/posts/2018/04/27/avoiding-integer-overflows-safemath-isnt-enough/).  


# Solidity SafeMath Checker - 检查Solidity合同中的是否有数学计算未使用SafeMath并修复
SafeMath是一个专为支持安全数学运算而设计的可靠数学库：安全意味着它在使用uint时防止溢出。你可以在[zeppelin-solidity SafeMath](https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/math/SafeMath.sol)中找到它。

## 工作流程
请将要检查的项目复制到“./to_check”文件夹中，运行：
```shell
python./main.py
```
然后您可以在“./backup”文件夹中找到备份文件，在“./to_check”文件夹中找到应用了SafeMath的新文件。

## 文件要求
1. 要检查的项目中的所有Solidity文件都命名为“*.sol”。
2. 要检查的项目中的所有SafeMath文件都命名为“SafeMath*.sol”，它们的文件名与防止溢出的uint类型相同。例如，SafeMath8.sol将保护uint8计算。
请注意，防止uint和uint256的溢出的是SafeMath.sol，而不是SafeMath256.sol。
4. 所有“*.sol”文件都是合法的。

## 运行环境
* Windows，Linux

## 软件要求
* 安装了Anaconda的Python3

## 逻辑
以“./example”文件夹中的文件为例（“./example/backup”存储了运行程序前的文件，“./example/to_check”存储了运行程序后的文件）：
1. 将所有*.sol文件（不包括SafeMath*.sol文件）复制到“./backup”文件夹中。
2. 检查所有*.sol文件（不包括SafeMath*.sol文件）以记录使用了哪些uint类型。
3. 检查所有SafeMath*.sol文件，找出在没有SafeMath*.sol文件的情况下使用哪些uint类型（来自#1的结果）。例如，C1.sol定义了uint32变量v1，但项目中没有SafeMath32.sol文件。
4. 根据#2的结果，在“./to_check/math”文件夹中创建所有缺少的SafeMath*.sol文件。例如，创建“./to_check/math/SafeMath32.sol”文件。
5. 在*.sol文件的每个文件（不包括SafeMath*.sol文件）中：
5.1. 导入所有SafeMath*.sol文件，并添加“using”语句。例如，添加“using SafeMath8 for uint8;”。
5.2. 更改所有++为添加（1）， --为sub(1)。例如，将“v1++”改变为“v1.add(1)”。

## 局限性
1. 程序不支持数学运算符的左操作数是整数。例如，3*a，会被改变为3.mul(a)，这是非法的。
2. 程序不支持同一数学运算符的左操作数和右操作数跨2行的语句。例如：
if (a>b
+1)
不能被正确地处理
3. 程序无法保护**，<<的结果不会溢出。 
你可以在[Avoiding Integer Overflows: SafeMath Isn't Enough](https://programtheblockchain.com/posts/2018/04/27/avoiding-integer-overflows-safemath-isnt-enough/)中找到保护这些运算的思路。
