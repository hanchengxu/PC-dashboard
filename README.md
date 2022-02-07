PC-dashboard
## 开发指南
### 上位机
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
### 下位机(ESP32)  
下位机使用esp32芯片，使用串口通信与上位机进行交互。
开发IDE为arduinoIDE。  
CPU及RAM数值的显示利用了esp32的`ledcwrite`进行PWM
