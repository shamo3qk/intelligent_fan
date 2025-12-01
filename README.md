## Intelligent Fan
Intelligent Fan 是一個結合 [Raspberry Pi](https://www.raspberrypi.com/) 與 [TensorFlow](https://github.com/tensorflow/tensorflow) 的專案

使用 Raspberry Pi 來控制風扇等周邊硬體，搭載 TensorFlow 驅動的咳嗽偵測模型，風扇的風速、轉向能夠依據咳嗽偵測的結果自動調控

本專案使用 [uv](https://docs.astral.sh/uv/) 作為專案管理工具，下載 uv 請參閱 [uv installation](https://docs.astral.sh/uv/getting-started/installation/)
### 如何運行
```bash
git clone https://github.com/shamo3qk/intelligent_fan.git
cd intelligent_fan
```
#### 下載系統依賴
Raspberry Pi OS / Debian / Ubuntu
```bash
sudo apt install portaudio19-dev
```
#### 同步專案依賴
```bash
uv sync
```
#### 運行專案
```bash
uv run src/main.py
```
### 調整參數
修改 src/settings.py 以調整音訊、風扇、模型的參數
