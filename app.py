# server.py
from flask import Flask, request, jsonify
from flask_sockets import Sockets
import base64
import time
import json
import gevent
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from tools import audio_pre_process, video_pre_process, generate_video,audio_process
import os
import re
import numpy as np

import shutil
import asyncio
import edge_tts
app = Flask(__name__)
sockets = Sockets(app)
video_list = []


async def main(voicename: str, text: str, OUTPUT_FILE):
    communicate = edge_tts.Communicate(text, voicename)

    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                pass                


def send_information(path, ws):

        print('데이터 전송 시작!')
        #path = video_list[0]
        ''''''
        with open(path, 'rb') as f:
            video_data = base64.b64encode(f.read()).decode()

        data = {
                'video': 'data:video/mp4;base64,%s' % video_data,
                }
        json_data = json.dumps(data)

        ws.send(json_data)



def txt_to_audio(text_):
    audio_list = []
    audio_path = 'data/audio/aud_0.wav'
    voicename = "zh-CN-YunxiaNeural"
    directory = os.path.dirname(audio_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    # 함께 배워봅시다. Bing은 AI에 의해 지원되므로 예기치 않은 오류가 발생할 수 있습니다. 사실을 확인하고 피드백을 공유해 주시면 우리가 배우고 개선하는 데 도움이 됩니다!
    text = text_
    asyncio.get_event_loop().run_until_complete(main(voicename,text,audio_path))
    audio_process(audio_path)
    
@sockets.route('/dighuman')
def echo_socket(ws):
    # Websocket 객체 가져오기
    #ws = request.environ.get('wsgi.websocket')
    # 만약 가져오지 못했다면, 오류 메시지를 반환합니다.
    if not ws:
        print('통신이 연결되지 않았습니다!')
        return 'Please use WebSocket'
    # 否则，循环接收和发送消息
    else:
        print('통신 연결됨.')
        while True:
            message = ws.receive()           
            
            if len(message)==0:

                return '입력 정보가 비어 있습니다.'
            else:                                
                txt_to_audio(message)                       
                audio_path = 'data/audio/aud_0.wav'
                audio_path_eo = 'data/audio/aud_0_eo.npy'
                video_path = 'data/video/results/ngp_0.mp4'
                output_path = 'data/video/results/output_0.mp4'
                generate_video(audio_path, audio_path_eo, video_path, output_path)
                video_list.append(output_path)
                send_information(output_path, ws)
                

               

if __name__ == '__main__':

    audio_pre_process()
    video_pre_process()
    
    server = pywsgi.WSGIServer(('127.0.0.1', 8800), app, handler_class=WebSocketHandler)
    server.serve_forever()
    
    