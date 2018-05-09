# Solidity SafeMath Checker - 检查Solidity合同中的是否有数学计算未使用SafeMath并修复
SafeMath是一个专为支持安全数学运算而设计的可靠数学库：安全意味着它在使用uint时防止溢出。你可以在[zeppelin-solidity SafeMath]中找到它（https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/math/SafeMath.sol）。

## 要求
1. 要检查的项目中的所有Solidity文件都命名为“*.sol”。
2. 要检查的项目中的所有SafeMath文件都命名为“SafeMath*.sol”，它们的文件名与防止溢出的uint类型相同。例如，SafeMath8.sol将保护uint8计算。
3. SafeMath.sol是#2的例外，它防止溢出的uint类型是uint（也是uint256）。

## 运行环境
* Windows，Linux

## 软件要求
*与Anaconda lib的Python3

## 工作流程
请将要检查的项目复制到“./to_check”文件夹中，运行：
```shell
python./main.py
```
然后您可以在“./bk”文件夹中找到备份文件，在“./to_check”文件夹中找到应用了SafeMath的新文件。

## 逻辑
以“./example”文件夹中的文件为例：
1. 将所有*.sol文件（不包括SafeMath*.sol文件）复制到“./bk”文件夹中。
2. 检查所有*.sol文件（不包括SafeMath*.sol文件）以记录使用了哪些uint类型。
3. 检查所有SafeMath*.sol文件，找出在没有SafeMath*.sol文件的情况下使用哪些uint类型（来自#1的结果）。例如，C1.sol定义了uint8变量v1，但项目中没有SafeMath8.sol文件。
4. 根据#2的结果，在“./to_check/math”文件夹中创建所有缺少的SafeMath*.sol文件。例如，创建“./to_check/math/SafeMath8.sol”文件。
5. 在*.sol文件的每个文件（不包括SafeMath*.sol文件）中：
5.1. 导入所有SafeMath*.sol文件，并添加“using”语句。例如，添加“using SafeMath8 for uint8;”。
5.2. 更改所有++为添加（1）， --为sub(1)。例如，将“v1++”改变为“v1.add(1)”。
5.3. 如果运算符号之前/之后没有空格，则更改+， - ，*，/添加sub，mul，div，程序将在运算符号之前/之后添加“ ”。例如，将“v1<=v1 + 2”改变为“v1 <= v1.add(2)”。
