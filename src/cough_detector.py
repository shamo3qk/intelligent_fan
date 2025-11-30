import librosa
import numpy as np
import sounddevice as sd
import tensorflow as tf

from settings import settings


class CoughDetector:
    def __init__(self, model_path: str) -> None:
        self.model = None
        self.running: bool = True
        # Load model
        try:
            self.model = tf.keras.models.load_model(model_path)
            print(f"info: 已載入訓練好的模型: {settings.model.path}")
        except Exception as e:
            print(f"warning: 尚未有訓練模型，將使用隨機預測: {e}")

        # Display default input device
        try:
            default_input = sd.query_devices(None, "input")
            print(
                f"info: 目前預設輸入裝置: {default_input['name']} (ch={default_input['max_input_channels']})"
            )
        except Exception as e:
            print(f"warning: 無法取得預設輸入裝置資訊: {e}")

    def stop(self):
        self.running = False

    def list_input_devices(self):
        """列出可用的輸入裝置"""
        try:
            devices = sd.query_devices()
            inputs = []
            for idx, device in enumerate(devices):
                if device.get("max_input_channels", 0) > 0:
                    inputs.append((idx, device["name"], device["max_input_channels"]))
            print("\n可用輸入裝置 (index, name, max_input_channels):")
            for idx, name, ch in inputs:
                print(f"  [{idx}] {name} (ch={ch})")
            return inputs
        except Exception as e:
            print(f"error: 列出輸入裝置失敗: {e}")
            return []

    def quick_rms_test(self, duration=0.5, sample_rate=16000, device=None):
        """快速錄一小段並回傳 RMS，方便測試裝置是否有訊號"""
        try:
            audio = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="float32",
                device=device,
            )
            sd.wait()
            audio = audio.flatten()
            rms = float(np.sqrt(np.mean(audio**2))) if audio.size else 0.0
            max_amp = float(np.max(np.abs(audio))) if audio.size else 0.0
            return rms, max_amp
        except Exception as e:
            print(f"error: 裝置 {device} 測試失敗: {e}")
            return 0.0, 0.0

    def auto_select_input_device(self, sample_rate=16000, min_threshold=1e-5):
        """嘗試所有可用輸入裝置，選擇 RMS 最大且有訊號的那個，回傳裝置索引或 None"""
        best_device = None
        best_rms = 0.0
        inputs = self.list_input_devices()
        for idx, name, ch in inputs:
            # 確認此裝置可以 1 聲道輸入
            try:
                sd.check_input_settings(device=idx, samplerate=sample_rate, channels=1)
            except Exception as e:
                # 不相容就跳過
                print(f"[skip] 裝置 [{idx}] {name} 不相容: {e}")
                continue

            rms, max_amp = self.quick_rms_test(
                duration=0.5, sample_rate=sample_rate, device=idx
            )
            print(f"[device] [{idx}] {name} -> RMS={rms:.6f}, MaxAmp={max_amp:.6f}")
            if rms > best_rms:
                best_rms = rms
                best_device = idx

        if best_device is None or best_rms < min_threshold:
            print(
                "error: 無法從任何輸入裝置取得有效訊號，可能是麥克風權限或裝置靜音/未連接"
            )
            return None

        print(f"自動選擇輸入裝置: [{best_device}] (RMS={best_rms:.6f})")
        return best_device

    def record_audio(self, duration=2, sample_rate=16000):
        """錄製音訊（會優先使用自動選擇的輸入裝置）"""
        # 設定預設參數
        sd.default.samplerate = sample_rate
        sd.default.channels = 1
        print("Recording...")
        try:
            # 優先使用自動選擇的裝置
            audio = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="float32",
                device=settings.input_device.selected_imput_device_index,
            )
            sd.wait()
            audio = audio.flatten()
        except Exception as e:
            print(f"error: 錄音失敗: {e}")
            audio = np.zeros(int(duration * sample_rate), dtype=np.float32)

        # 若尚未自動偵測，且錄到的音為全 0，嘗試自動選擇裝置一次
        if not settings.input_device.autoselect_done:
            settings.input_device.autoselect_done = True
            rms = float(np.sqrt(np.mean(audio**2))) if audio.size else 0.0
            if rms == 0.0:
                print("嘗試自動選擇可用的輸入裝置...")
                candidate = self.auto_select_input_device(sample_rate=sample_rate)
                if candidate is not None:
                    settings.input_device.selected_imput_device_index = candidate
                    # 重新錄一次
                    try:
                        audio = sd.rec(
                            int(duration * sample_rate),
                            samplerate=sample_rate,
                            channels=1,
                            dtype="float32",
                            device=settings.input_device.selected_imput_device_index,
                        )
                        sd.wait()
                        audio = audio.flatten()
                    except Exception as e:
                        print(f"error: 自動選擇後錄音仍失敗: {e}")
        return audio

    def check_audio_presence(self, audio, threshold=0.01):
        """檢查是否有收到音頻訊號"""
        # 計算音頻的RMS (Root Mean Square) 值
        rms = np.sqrt(np.mean(audio**2))
        # 計算最大振幅
        max_amplitude = np.max(np.abs(audio))

        # 如果 RMS 值或最大振幅超過閾值，表示有音頻訊號
        has_audio = rms > threshold or max_amplitude > threshold

        return has_audio, rms, max_amplitude

    def extract_mfcc(self, audio, sample_rate=16000, n_mfcc=40, duration=2):
        """把音訊轉換成 MFCC 特徵 - 與訓練時保持一致

        步驟：
        1) 以錄音取樣率 fs 取得音訊，若與訓練取樣率不同，先重採樣到 TRAIN_SR
        2) 依訓練時長度補零/截斷
        3) 計算 MFCC 並標準化
        4) 依模型期望的時間維度修齊（pad/trim）
        5) 擴維到 (1, n_mfcc, time, 1)
        """
        # 1) 重採樣到訓練用取樣率
        if sample_rate != settings.audio.train_sr:
            try:
                audio = librosa.resample(
                    audio, orig_sr=sample_rate, target_sr=settings.audio.train_sr
                )
                fs_proc = settings.audio.train_sr
                print(f"info: 已重採樣: {sample_rate} -> {settings.audio.train_sr}")
            except Exception as e:
                print(f"warning: 重採樣失敗，改以原始取樣率計算 MFCC: {e}")
                fs_proc = sample_rate
        else:
            fs_proc = sample_rate

        # 2) 確保音頻長度與訓練時一致
        samples_per_file = int(settings.audio.train_sr * duration)
        if len(audio) < samples_per_file:
            audio = np.pad(audio, (0, samples_per_file - len(audio)))
        elif len(audio) > samples_per_file:
            audio = audio[:samples_per_file]

        # 3) 計算 MFCC 並標準化
        mfcc = librosa.feature.mfcc(y=audio, sr=fs_proc, n_mfcc=settings.audio.n_mfcc)
        print(f"info: MFCC original shape: {mfcc.shape}")
        mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)

        # 4) 若模型存在，將時間維度修齊到模型期望的大小
        try:
            if (
                self.model is not None
                and hasattr(self.model, "input_shape")
                and len(self.model.input_shape) >= 4
            ):
                target_time = self.model.input_shape[2]
                if (
                    isinstance(target_time, int)
                    and target_time > 0
                    and mfcc.shape[1] != target_time
                ):
                    import librosa.util as lutil

                    mfcc = lutil.fix_length(mfcc, size=target_time, axis=1)
                    print(f"info: 已將時間維度修齊到模型期望: {target_time}")
        except Exception as e:
            print(f"warning: 修齊時間維度時發生例外，將使用原始 MFCC 時間維度: {e}")

        # 5) 加上 batch 和 channel 維度 -> (1, n_mfcc, time, 1)
        mfcc = np.expand_dims(mfcc, axis=(0, -1))
        print(f"info: MFCC final shape: {mfcc.shape}")

        return mfcc

    def predict_cough(self, mfcc, threshold=0.5):
        """使用模型預測是否咳嗽"""
        if self.model is None:
            return "No Model", 0.0  # 沒有模型

        pred = self.model.predict(mfcc, verbose=0)
        confidence = pred[0][0]

        print(f"confidence: {confidence:.4f}")
        print(f"threshold: {threshold}")

        if confidence > threshold:
            result = "Cough"
            print(f"✅ 判斷為咳嗽 (confidence: {confidence:.2%})")
        else:
            result = "Non-cough"
            print(f"❌ 判斷為非咳嗽 (confidence: {(1 - confidence):.2%})")

        return result, confidence

    def detect_cough_in_windows(
        self,
        audio,
        sample_rate: int,
        n_mfcc: int = 40,
        window_duration: int = 2,
        step_duration: float = 0.5,
        threshold: float = 0.3,
    ):
        """
        使用滑動視窗掃描音頻，尋找咳嗽片段

        參數:
            audio: 完整音頻陣列
            fs: 原始取樣率
            n_mfcc: MFCC 特徵數
            settings.audio.window_duration: 每個視窗的長度（秒）
            step_duration: 滑動步進（秒）
            threshold: 判定閾值

        返回:
            has_cough: 是否偵測到咳嗽
            max_confidence: 最高信心度
            detections: 所有檢測結果列表
        """
        if self.model is None:
            return False, 0.0, []

        # 先重採樣到訓練取樣率
        if sample_rate != settings.audio.train_sr:
            audio = librosa.resample(
                audio, orig_sr=sample_rate, target_sr=settings.audio.train_sr
            )
            sample_rate = settings.audio.train_sr

        window_samples = int(settings.audio.window_duration * settings.audio.train_sr)
        step_samples = int(step_duration * settings.audio.train_sr)

        detections = []
        max_confidence = 0.0
        has_cough = False

        # 滑動視窗掃描
        for start in range(0, len(audio) - window_samples + 1, step_samples):
            end = start + window_samples
            window_audio = audio[start:end]

            # 提取 MFCC
            mfcc = librosa.feature.mfcc(
                y=window_audio, sr=settings.audio.train_sr, n_mfcc=settings.audio.n_mfcc
            )
            mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)

            # 修齊時間維度
            try:
                if (
                    hasattr(self.model, "input_shape")
                    and len(self.model.input_shape) >= 4
                ):
                    target_time = self.model.input_shape[2]
                    if (
                        isinstance(target_time, int)
                        and target_time > 0
                        and mfcc.shape[1] != target_time
                    ):
                        import librosa.util as lutil

                        mfcc = lutil.fix_length(mfcc, size=target_time, axis=1)
            except Exception as e:
                print(f"error: failed fix dimension length: {e}")

            # 擴維並預測
            mfcc = np.expand_dims(mfcc, axis=(0, -1))
            pred = self.model.predict(mfcc, verbose=0)
            confidence = float(pred[0][0])

            start_time = start / settings.audio.train_sr
            is_cough = confidence > threshold

            detections.append(
                {
                    "start_time": start_time,
                    "end_time": start_time + settings.audio.window_duration,
                    "confidence": confidence,
                    "is_cough": is_cough,
                }
            )

            if confidence > max_confidence:
                max_confidence = confidence

            if is_cough:
                has_cough = True

        return has_cough, max_confidence, detections

    def run(self):
        while self.running:
            audio = self.record_audio(
                settings.audio.record_duration, settings.audio.sample_rate
            )
            has_audio, rms, max_amplitude = self.check_audio_presence(
                audio, settings.audio.threshold
            )
            if not has_audio:
                print(
                    f"❌ 未收到音頻訊號或音量太小 (RMS: {rms:.4f}, 最大振幅: {max_amplitude:.4f})"
                )
                continue

            print(f"收到音頻訊號 (RMS: {rms:.4f}, 最大振幅: {max_amplitude:.4f})")
            print(
                f"使用滑動視窗分析 (視窗: {settings.audio.window_duration}s, 步進: {settings.audio.window_step}s)..."
            )

            # 使用滑動視窗偵測咳嗽
            has_cough, max_conf, detections = self.detect_cough_in_windows(
                audio,
                settings.audio.sample_rate,
                settings.audio.n_mfcc,
                settings.audio.window_duration,
                settings.audio.window_step,
                threshold=settings.model.threshold,
            )

            # 顯示所有視窗的檢測結果
            print(f"\n共分析 {len(detections)} 個視窗:")
            for i, det in enumerate(detections):
                status = "🟢 咳嗽" if det["is_cough"] else "⚪ 正常"
                print(
                    f"  視窗 {i + 1}: {det['start_time']:.1f}s-{det['end_time']:.1f}s -> {status} (confidence: {det['confidence']:.2%})"
                )

            # 最終判定
            print(f"\nMax confidence: {max_conf:.2%}")
            if has_cough:
                print(
                    f"✅ 最終偵測結果：Cough (在 {settings.audio.record_duration}s 內偵測到咳嗽)"
                )
            else:
                print(
                    f"❌ 最終偵測結果：Non-cough (在 {settings.audio.record_duration}s 內未偵測到咳嗽)"
                )
            print("-" * 50)
