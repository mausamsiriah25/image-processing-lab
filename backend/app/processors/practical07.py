"""Practical 07 — Lossless Image Compression (JPEG vs PNG, RLE, LZW)."""
from __future__ import annotations

import cv2
import numpy as np

from .base import (
    Output,
    ProcessingError,
    ProcessingResult,
    image_output,
    table_output,
    timed,
    value_output,
)

METHODS = ["jpeg_vs_png", "rle", "lzw"]


def _to_gray(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img


def _rle_encode(flat: np.ndarray) -> list[tuple[int, int]]:
    encoded: list[tuple[int, int]] = []
    if flat.size == 0:
        return encoded
    prev = int(flat[0])
    count = 1
    for value in flat[1:]:
        value = int(value)
        if value == prev:
            count += 1
        else:
            encoded.append((prev, count))
            prev, count = value, 1
    encoded.append((prev, count))
    return encoded


def _rle_decode(encoded: list[tuple[int, int]]) -> np.ndarray:
    values = []
    for value, count in encoded:
        values.extend([value] * count)
    return np.array(values, dtype=np.uint8)


def _lzw_compress(data: list[int]) -> list[int]:
    dictionary = {(i,): i for i in range(256)}
    next_code = 256
    result: list[int] = []
    current = (data[0],) if data else tuple()
    for symbol in data[1:]:
        candidate = current + (symbol,)
        if candidate in dictionary:
            current = candidate
        else:
            result.append(dictionary[current])
            dictionary[candidate] = next_code
            next_code += 1
            current = (symbol,)
    if current:
        result.append(dictionary[current])
    return result


def _lzw_decompress(codes: list[int]) -> list[int]:
    dictionary = {i: (i,) for i in range(256)}
    next_code = 256
    if not codes:
        return []
    result = list(dictionary[codes[0]])
    previous = dictionary[codes[0]]
    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = previous + (previous[0],)
        else:
            raise ProcessingError("Corrupt LZW stream.")
        result.extend(entry)
        dictionary[next_code] = previous + (entry[0],)
        next_code += 1
        previous = entry
    return result


def process(images: dict[str, np.ndarray], params: dict) -> ProcessingResult:
    if "image" not in images:
        raise ProcessingError("An input image is required for this practical.")
    img = images["image"]
    method = params.get("method", "jpeg_vs_png")

    with timed() as t:
        outputs: list[Output] = [image_output("Original Image", img, "practical-07-original.png")]

        if method == "jpeg_vs_png":
            quality = int(params.get("jpegQuality", 90))
            ok_jpg, jpg_buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, quality])
            ok_png, png_buf = cv2.imencode(".png", img, [cv2.IMWRITE_PNG_COMPRESSION, 9])
            if not (ok_jpg and ok_png):
                raise ProcessingError("Failed to encode image for comparison.")
            raw_size = img.size * img.itemsize
            jpg_size = len(jpg_buf)
            png_size = len(png_buf)
            outputs.append(
                table_output(
                    "Compression Comparison",
                    [
                        {"format": "Raw (uncompressed)", "sizeBytes": int(raw_size), "compressionRatio": "1.00x"},
                        {
                            "format": f"JPEG (quality={quality}, lossy)",
                            "sizeBytes": int(jpg_size),
                            "compressionRatio": f"{raw_size / jpg_size:.2f}x",
                        },
                        {
                            "format": "PNG (lossless)",
                            "sizeBytes": int(png_size),
                            "compressionRatio": f"{raw_size / png_size:.2f}x",
                        },
                    ],
                    caption="Lossy JPEG vs lossless PNG size comparison.",
                )
            )
            decoded_png = cv2.imdecode(png_buf, cv2.IMREAD_UNCHANGED)
            lossless = bool(np.array_equal(decoded_png, img))
            outputs.append(value_output("PNG reconstruction is lossless", lossless))
            outputs.append(image_output("Reconstructed from PNG", decoded_png, "practical-07-png-reconstructed.png"))

        elif method == "rle":
            gray = _to_gray(img)
            flat = gray.flatten()
            encoded = _rle_encode(flat)
            decoded = _rle_decode(encoded)
            lossless = bool(np.array_equal(decoded, flat))
            approx_compressed_bytes = len(encoded) * 2  # 1 byte value + 1 byte count (approx.)
            raw_bytes = flat.size
            outputs.append(image_output("Grayscale Source", gray, "practical-07-rle-source.png"))
            outputs.append(
                table_output(
                    "RLE Result",
                    [
                        {"metric": "Original size (bytes)", "value": int(raw_bytes)},
                        {"metric": "RLE run count", "value": len(encoded)},
                        {"metric": "Approx. compressed size (bytes)", "value": int(approx_compressed_bytes)},
                        {
                            "metric": "Approx. compression ratio",
                            "value": f"{raw_bytes / max(approx_compressed_bytes, 1):.2f}x",
                        },
                        {"metric": "Lossless reconstruction verified", "value": lossless},
                    ],
                )
            )
            outputs.append(
                image_output(
                    "Reconstructed from RLE", decoded.reshape(gray.shape), "practical-07-rle-reconstructed.png"
                )
            )

        elif method == "lzw":
            gray = _to_gray(img)
            flat = gray.flatten().tolist()
            compressed = _lzw_compress(flat)
            decompressed = _lzw_decompress(compressed)
            lossless = decompressed == flat
            # Approximate: each LZW code needs enough bits to index the dictionary,
            # here approximated with 2 bytes/code for simplicity/display purposes.
            approx_compressed_bytes = len(compressed) * 2
            raw_bytes = len(flat)
            outputs.append(image_output("Grayscale Source", gray, "practical-07-lzw-source.png"))
            outputs.append(
                table_output(
                    "LZW Result",
                    [
                        {"metric": "Original size (bytes)", "value": int(raw_bytes)},
                        {"metric": "LZW code count", "value": len(compressed)},
                        {"metric": "Approx. compressed size (bytes)", "value": int(approx_compressed_bytes)},
                        {
                            "metric": "Approx. compression ratio",
                            "value": f"{raw_bytes / max(approx_compressed_bytes, 1):.2f}x",
                        },
                        {"metric": "Lossless reconstruction verified", "value": lossless},
                    ],
                )
            )
            reconstructed = np.array(decompressed, dtype=np.uint8).reshape(gray.shape)
            outputs.append(image_output("Reconstructed from LZW", reconstructed, "practical-07-lzw-reconstructed.png"))

        else:
            raise ProcessingError(f"Unsupported method '{method}'.")

    return ProcessingResult(success=True, processing_time=t.elapsed, outputs=outputs, metadata={"method": method})
