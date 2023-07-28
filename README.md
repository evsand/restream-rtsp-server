# RTSP SERVER [TEST TASK]
Необходимо написать программный модуль, исполняемый консольно. Пример запуска:</br>
run.py [RTSP-поток входящий] [порт, по которому будет транслироваться входящий поток во внутреннюю сеть по протоколу RTSP]</br>
</br>

## Installation Instructions

### Installation

#### Step-1 Install GStreamer-1.0 and related plugins

```
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```
#### Step-2 Install RTSP server

```
sudo apt-get install libglib2.0-dev libgstrtspserver-1.0-dev gstreamer1.0-rtsp
```

Requirement

    Python 3.x
    Opencv 3.x or above ( pip install opencv-python )

### HOW TO USE
- python run.py RTSP-stream PORT </br>
  ``python run.py rtsp://zephyr.rtsp.stream/pattern?streamKey=6bd4a501d69abf02ce2fa7515188480f 8544``
- open media player with stream link (for example ffmpeg):
  ``ffplay rtsp://127.0.0.1:8544/``


## TODO
- [ ] Write tests
- [ ] Problems connecting multiple users to the server
