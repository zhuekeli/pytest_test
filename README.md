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

src/case 是测试 case 目录
src/common 工具包
src/api 服务的接口封装
