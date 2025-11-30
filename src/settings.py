from dataclasses import dataclass, field


@dataclass
class AudioConfig:
    record_duration: int = 5
    threshold: float = 0.01
    window_duration: int = 2
    window_step: float = 0.5
    sample_rate: int = 44100
    n_mfcc: int = 40
    train_sr: int = 16000


@dataclass
class InputDeviceConfig:
    selected_imput_device_index: int = 0
    autoselect_done: bool = False


@dataclass
class ModelConfig:
    path: str = "models/cough_model.h5"
    threshold: float = 0.1


@dataclass
class Settings:
    audio: AudioConfig = field(default_factory=AudioConfig)
    input_device: InputDeviceConfig = field(default_factory=InputDeviceConfig)
    model: ModelConfig = field(default_factory=ModelConfig)


settings: Settings = Settings()
