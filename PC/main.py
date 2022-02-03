import serial
import serial.tools.list_ports
import time
import psutil

# 校验字符串
handshakeStr = 'handshake'
# 初始化port为空
targetPort = None


# 串口握手工具方法
# 一个串口头两次通信response空，不知道为什么。所以发三次每次间隔1s
def handshake(arduino):
    i = 0
    while i < 3:
        arduino.write(bytes(handshakeStr, 'utf-8'))
        time.sleep(1)
        i = i + 1
    return arduino.readline()


# 获取目标串口 频率10s扫描一次
def getTargetPort():
    # 获取所有串口
    portList = list(serial.tools.list_ports.comports())
    if len(portList) > 0:
        # 遍历所有串口
        for port in portList:
            arduino = serial.Serial(port.name, baudrate=115200, timeout=.1)
            data = handshake(arduino)
            # 串口握手校验
            if data.decode().strip() == handshakeStr:
                arduino.close()
                print(port.name + " is usable")
                return port
    else:
        # 没有任何串口
        print("no any port")
        time.sleep(10)


# 上位机核心逻辑
while True:
    if targetPort is None:
        targetPort = getTargetPort()
    else:
        try:
            # 握手成功后 进行通信
            arduino = serial.Serial(targetPort.name, baudrate=115200, timeout=.1)
            message = "0,0"
            while True:
                message = str(round(psutil.cpu_percent(0))) + "," + (str)(round(psutil.virtual_memory().percent))
                print(message)
                time.sleep(1)
                arduino.write(bytes(message, 'utf-8'))
                time.sleep(1)
                data = arduino.readline()
                print("response:" + data.decode())
        except Exception:
            # 有异常后停止通信并再次 获取目标串口
            targetPort = getTargetPort()
