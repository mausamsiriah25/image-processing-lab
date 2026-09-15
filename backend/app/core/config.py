"""Application configuration, driven by environment variables."""
import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    app_name: str = "Image Processing Lab API"
    environment: str = os.getenv("ENVIRONMENT", "development")
    cors_origins: list[str] = field(
        default_factory=lambda: [
            origin.strip()
            for origin in os.getenv(
                "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
            ).split(",")
            if origin.strip()
        ]
    )
    max_upload_size_bytes: int = int(os.getenv("MAX_UPLOAD_SIZE_BYTES", str(15 * 1024 * 1024)))
    max_image_dimension: int = int(os.getenv("MAX_IMAGE_DIMENSION", "6000"))
    allowed_image_types: tuple[str, ...] = ("image/jpeg", "image/png", "image/webp")
    content_dir: str = os.getenv(
        "CONTENT_DIR",
        os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "content", "practicals")),
    )


settings = Settings()
