
# 背景
本家是来自ShaderFallback的[CpuRamGet](https://github.com/ShaderFallback/CpuRamGet)的项目。一个CPU&RAM物理监控表。  
我Fork项目之后在软件层面重新写了一版。包括上位机和Esp32部分。 

因为我目前没有3D打印机，以及并不具备建模的能力，所以模型部分是自己再设计并用亚克力板切割组装而成。  
表盘文件也基于CpuRamGet项目并追加了Rick and Morty表盘。 

这个Fork项目更多的是软件实现层面上的差异。

如果您对项目感兴趣，还请多支持原作者的CpuRamGet。


## 软件实现思路
### 1.上位机程序
本项目使用了Python的psutil包来获取cpu以及ram信息。 
再利用pyserial包通过串口与下位机进行交互。 

作为web软件工程师，原本想使用最熟悉的Java语言来实现上位机的程序。  
但经过调查，发现使用Java进行串口通信的依赖包使用起来比较复杂，  
于是放弃了Java，选择了Python。

并且使用Python后可以利用pyqt5来制作上位机图形界面，也比较容易。


### 2.下位机
下位机接收到文本数据后如何显示在电压表上,也与[CpuRamGet](https://github.com/ShaderFallback/CpuRamGet)稍微不同。   

下位机使用esp32芯片，使用串口通信与上位机进行交互。
开发IDE为arduinoIDE。  
CPU及RAM数值的显示利用了esp32的`ledcwrite`进行PWM。

当然也提供了arduino开发板的版本，在arduino里使用`analogWrite`进行信息的处理。

下位机文件在/board/


## 开发指南
### 1.上位机
上位机采用python开发，图形库为pyqt5。开发IDE为vscode。
#### 启动
1. `cd PC` 进入上位机文件夹
2. `pip install -r requirements.txt` 安装开发依赖
3. `python main.py`  启动上位机
#### 依赖包
使用`pip`新增或变更依赖后请执行下列来更新依赖文件
```
pip freeze > requirements.txt
```
#### 图片资源文件
修改或变更图片资源后，请在根目录执行下列命令来生成和更新resource.py文件 
```
pyrcc5 resource.qrc -o resource.py
```
代码中引用图片资源:  
```
self.searchManualAction.setIcon(QIcon(':/imgs/checked.png'))
```
#### 打包可执行exe文件
目前只在windows10 64位机上测试过
```
pyinstaller -F main.py -i ./icon.ico --noconsole
```
解决windows10打包后图标缓存
```
ie4uinit.exe -show
```
### 2.下位机

通过串口接受到数据，下位机采用PWM的方式控制电压表，由于没有使用Wifi传输
数据，这使得我们可以使用arduino uno等开发板。下位机文件夹里提供了esp32和
arduino的不同实现。

核心区别就是esp32使用了ledcWrite而arduino uno使用的是analogWrite函数。

### ⚠️串口驱动

⚠️初次使用Esp32在电脑上连接的时候，如果扫描不到串口，需要安装串口驱动。⚠️  
(驱动地址)[https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers]  
安装这个驱动: CP210x Windows Drivers with Serial Enumerator

😭看来使用串口方式还是直接用arduino开发板才能即插即用。唉，心累。
