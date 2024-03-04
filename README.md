# NeRF - 메타 휴먼 실시간 셍성 및 구동 
: **해당 레포지토리는 메타 휴먼 관련해서 Fay라는 메타휴먼 오픈소스 플랫폼에서 활용할 수 있도록 제작된 Xuniren을 쉽게 활용할 수 있도록 한국어로 작성한 레포지토리 입니다.**  
![](/img/example.gif)

## 한국어 설치 가이드 범위
: 해당 레포지토리는 Windows 설치 과정은 고려하지 않았으며 Ubuntu 환경 기반의 서버에서 활용할 수 있도록 각종 세팅을 제공하고자 합니다.   
또한 작성 시점으로는 Fay를 통한 UI 기반 응용을 하지 않고 로컬 환경에서 추론하는 것만으로 고려하여 작성되었습니다.   
따라서, Windows 환경이나 모델 학습을 원할 경우 아래 블로그 글(중국어)을 확인하여 진행하시기 바랍니다.(추후 업데이트 될 수 있음.)

xuniren windows 설치가이드：[Windows에서 PyTorch3D를 설치하여 Xuniren 프로젝트를 배포하는 단계별 과정 - 중국어 (cnblogs.com)](https://www.cnblogs.com/dm521/p/17469967.html)

모델 훈련 튜토리얼：[Xuniren(Fay 디지털 인물 오픈소스 커뮤니티 프로젝트) NeRF 모델 훈련 튜토리얼 - 중국어](https://blog.csdn.net/aa84758481/article/details/131135823)

## 수정사항
1. python app.py를 실행하여 websocket 기반 통신 과정에서 File Not Found 에러를 방지하기 위해 app.py 코드 추가(55~57 line) + 주석 번역
2. 파일 쓰기에 실패하는 경우를 방지하기 위해 nerf/utils.py에 코드 추가(938 line)
3. 로컬 기반 통신 과정에서 CLI 기반 통신이 가능하도록 communicator.py 코드 작성  
    - 사용법  
        1) python app.py 실행
        2) python communicator.py 실행
        3) CLI에 메타 휴먼이 발화하도록 만들고 싶은 text 입력
        4) data/aud_0.wav가 음성 파일, data/video/results/output_0.mp4가 결과 영상

# Get Started
: 시작하기에 앞서 만약 Ubuntu 기반 GPU Server 환경에서 Docker Container 기반으로 해당 프로젝트를 진행하신다면 ubuntu 환경에서 pyaudio를 활용하기 위해 **portaudio** 및 **requirements.txt**를 설치한 Docker image를 만드는 것을 추천드립니다.

## Installation

원작자: Tested on Ubuntu 22.04, Pytorch 1.12 and CUDA 11.6，or  Pytorch 1.12 and CUDA 11.3  
**새롭게 테스트 진행한 환경: Ubuntu 20.04.06, Pytorch 1.12.1 and CUDA 11.3**

```python
git clone https://github.com/SangJunni/meta-human-xuniren-.git
cd xuniren
```

### Install dependency

```python
# for ubuntu, portaudio is needed for pyaudio to work.(Sudo 권한이 없을 경우 docker에 미리 설치하는 것을 권장합니다.)
sudo apt install portaudio19-dev

pip install -r requirements.txt
# 프로젝트에는 or로 설정했지만 가상환경 dependency 등이 존재해서 가상환경 생성을 권장합니다.
conda env create -f environment.yml 
# install pytorch3d(ubuntu/mac인 경우)
pip install "git+https://github.com/facebookresearch/pytorch3d.git"
```
### **로컬환경에서 실행하기**
위 환경 설정을 완료한 경우 아래 코드를 통해 메타 휴먼 생성기를 시작합니다.

```python
python app.py
```

인터페이스 입출력 관련 정보 [Websoket.md](https://github.com/waityousea/xuniren/blob/main/WebSocket.md)

메타 휴먼 생성 관련 모델 파일

```python
## 모델 파일의 경우 별도 훈련이 필요.
.
├── data
│   ├── kf.json			
│   ├── pretrained
│   └── └── ngp_kg.pth

```
### 실행 과정에서 에러가 발생한 경우
1. ModuleNotFoundError: No module named '_raymarching_face'  
: 실제 Raymarching 라이브러리의 설치가 이루어지지 않은 상태이기 때문에 raymarching을 pip로 install
```
pip install ./raymarching

```
2. RuntimeError: Error building extension '_grid_encoder'  
: 1번과 마찬가지로 gridencoder 라이브러리의 설치가 이루어지지 않은 상태이기 때문에 raymarching을 pip로 install
```
pip install ./gridencoder
```

3. RuntimeError: Error building extension '_sh_encoder'  
: 위와 마찬가지로 shencoder 라이브러리의 설치가 이루어지지 않은 상태이기 때문에 raymarching을 pip로 install
```
pip install ./shencoder
```

4. RuntimeError: Error building extension _freqencoder'  
: 위와 마찬가지로 freqencoder 라이브러리의 설치가 이루어지지 않은 상태이기 때문에 raymarching을 pip로 install
```
pip install ./freqencoder
```
5. werkzeug.routing.exceptions.WebsocketMismatch: 400 Bad Request  
: flask 밑 관련 의존성 패키지의 버전이 맞지 않아서 발생하는 문제.   
아래의 코드대로 라이브러리들을 특정 버전으로 설치해주면 문제해결 가능
```
pip install Werkzeug==1.0.1
pip install Flask==1.1.4
pip install markupsafe==2.0.1

```

### 추론 속도

데스크톱 RTX A4000 or RTX 3080ti 16G에서 비디오 추론 시 35~43fps 처리가 가능. 실제 python app.py 실행시 fp16으로 2.2G 가량의 VRAM을 차지.

# Acknowledgement

- The data pre-processing part is adapted from [AD-NeRF](https://github.com/YudongGuo/AD-NeRF).
- The NeRF framework is based on [torch-ngp](https://github.com/ashawkey/torch-ngp).
- The algorithm core come from  [RAD-NeRF](https://github.com/ashawkey/RAD-NeRF).
- Usage example [Fay](https://github.com/TheRamU/Fay).

학술 교류 관련 원작자와 연락하는 곳：waityousea@126.com
