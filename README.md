## 如何运行

1. 安装 python
2. 安装 python 相关依赖

```shell
pip install -r requirements.txt
```

3. 安装 JDK、allure，allure 运行需要 JDK
4. 运行脚本

```shell
python run_case.py
```

## 项目依赖管理

1. 安装 pipreqs 工具

```shell
pip install pipreqs
```

2. 执行 pipreqs 命令生成依赖列表

```shell
pipreqs ./ --encoding=utf-8 --force
```

3. 自动安装所有依赖包

```shell
pip install -r requirements.txt
```

## 目录说明

* src/case 是测试 case 目录
* src/common 工具包
* src/api 服务的接口封装，以及跟业务相关的方法

## case 顺序

1. 测试的模板 src/case 模块
2. pytest 执行测试的顺序是，先执行模块下的 conftest.py 文件，假如有
3. 按照文件顺序，执行模块下以 test 开头的py 文件
4. 按照子模块的顺序，挨个执行子模块
5. 只会执行以 test、Test 等开头的文件、类、方法

## pytest 用法简介

1. pytest 会递归的遍历并执行以 test 开头或结尾的文件、类、方法
2. `@pytest.mark.skip(reason='out-of-date api')` 可以跳过测试
3. `@pytest.mark.skipif(conn.__version__ < '0.2.0', reason='not supported until v0.2.0')`，按照指定条件跳过
4. `pytest.mark.parametrize(argnames, argvalues)` 可以参数化测试，每组参数都是独立的一次测试，详细示例见 example/pytest/pytest_mark_parametrize
5. `@pytest.fixture()`，表示固件，用于 pytest 在执行测试函数之前后之后加载他们
6. 作用域是为了更精细化控制固件
    * `function` : 函数级，每个测试函数都会执行一次固件；
    * `class` : 类级别，每个测试类执行一次，所有方法都可以使用；
    * `module` : 模块级，每个模块执行一次，模块内函数和方法都可使用；
    * `session` : 会话级，一次测试只执行一次，所有被找到的函数和方法都可用。
