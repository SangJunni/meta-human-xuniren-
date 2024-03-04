from websocket import create_connection

def client_handle():
    ws = create_connection('ws://127.0.0.1:8800/dighuman')
    while True:
        # 연결이 된 경우 지속적으로 입력 텍스트에 대한 음성, 영상을 만들 수 있도록 설정
        if ws.connected:
            line = input()
            ws.send(line)
            result = ws.recv()
            print(f"client received:{result}")
            # ws.close()

if __name__ == "__main__":
    client_handle()