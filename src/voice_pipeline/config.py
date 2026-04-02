from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="VOICE_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    host: str = "127.0.0.1"
    port: int = 8000
    ws_path: str = "/ws"
    sample_rate: int = 16000
    blocksize: int = 256
    channels: int = 1
    dtype: str = "int16"
    portaudio_latency: str | None = "low"
    tx_queue_maxsize: int = 2
    ws_compression: bool = False
    ws_max_queue: int = 4

    @property
    def ws_url(self) -> str:
        return f"ws://{self.host}:{self.port}{self.ws_path}"


settings = Settings()
