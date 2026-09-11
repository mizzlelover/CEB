import re
import zlib

from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives.ciphers import Cipher

try:
    from cryptography.hazmat.decrepit.ciphers.modes import CFB, OFB
except ModuleNotFoundError:
    from cryptography.hazmat.primitives.ciphers.modes import CFB, OFB

from .format import (
    CebDocument,
    CebFormatError,
    decrypt_pdf_data,
    unwrap_stream_key,
)

STREAM_ALGORITHM_OFB: int = 1
STREAM_ALGORITHM_CFB: int = 2
STREAM_KEY_LENGTH: int = 24


def _stream_length(data: bytes, dictionary: bytes, path: CebDocument) -> int:
    indirect = re.search(rb"/Length\s+(\d+)\s+0\s+R", dictionary)
    if indirect is not None:
        object_number = int(indirect.group(1))
        pattern = (
            rb"(?<!\d)" + str(object_number).encode() + rb"\s+0\s+obj\s*(\d+)\s*endobj"
        )
        value = re.search(pattern, data)
        if value is None:
            raise CebFormatError(path.path, "stream length object is missing")
        return int(value.group(1))
    direct = re.search(rb"/Length\s+(\d+)(?!\s+0\s+R)", dictionary)
    if direct is None:
        raise CebFormatError(path.path, "stream length is missing")
    return int(direct.group(1))


def _stream_ranges(data: bytes, path: CebDocument) -> tuple[tuple[int, int, bool], ...]:
    ranges: list[tuple[int, int, bool]] = []
    cursor = 0
    while True:
        stream = data.find(b"stream", cursor)
        if stream < 0:
            return tuple(ranges)
        if stream > 0 and data[stream - 1] == ord("d"):
            cursor = stream + 6
            continue
        line_end = data.find(b"\n", stream + 6)
        if line_end < 0:
            raise CebFormatError(path.path, "stream marker has no line ending")
        data_start = line_end + 1
        endstream = data.find(b"endstream", data_start)
        if endstream < 0:
            raise CebFormatError(path.path, "stream marker has no endstream")
        dictionary_start = data.rfind(b"endobj", 0, stream)
        dictionary = data[dictionary_start + 6 : stream]
        length = _stream_length(data, dictionary, path)
        data_end = data_start + length
        if data_end > endstream or data[data_end:endstream].strip(b"\r\n"):
            raise CebFormatError(path.path, "stream length does not match endstream")
        ranges.append((data_start, data_end, b"/FlateDecode" in dictionary))
        cursor = endstream + 9


def _decrypt_stream(data: bytes, key: bytes, algorithm: int) -> bytes:
    output = bytearray()
    for offset in range(0, len(data), 256):
        chunk = data[offset : offset + 256]
        if algorithm == STREAM_ALGORITHM_OFB:
            cipher = Cipher(TripleDES(key), OFB(key[:8]))
        else:
            cipher = Cipher(TripleDES(key), CFB(key[:8]))
        context = cipher.decryptor()
        output.extend(context.update(chunk))
        output.extend(context.finalize())
    return bytes(output)


def _blank_encrypt_reference(match: re.Match[bytes]) -> bytes:
    return b" " * len(match.group(0))


def decode_pdf(document: CebDocument) -> bytes:
    pdf_data = bytearray(decrypt_pdf_data(document))
    spec = unwrap_stream_key(document)
    if spec.algorithm == 0:
        return re.sub(
            rb"/Encrypt\s+\d+\s+0\s+R",
            _blank_encrypt_reference,
            bytes(pdf_data),
        )
    if (
        spec.algorithm not in (STREAM_ALGORITHM_OFB, STREAM_ALGORITHM_CFB)
        or len(spec.key) != STREAM_KEY_LENGTH
    ):
        raise CebFormatError(document.path, "unsupported CEB stream cipher")
    for start, end, is_flate in _stream_ranges(bytes(pdf_data), document):
        decrypted = _decrypt_stream(
            bytes(pdf_data[start:end]), spec.key, spec.algorithm
        )
        if is_flate:
            try:
                _ = zlib.decompress(decrypted)
            except zlib.error as exc:
                raise CebFormatError(
                    document.path, "content stream is not valid Flate data"
                ) from exc
        pdf_data[start:end] = decrypted
    return re.sub(
        rb"/Encrypt\s+\d+\s+0\s+R",
        _blank_encrypt_reference,
        bytes(pdf_data),
    )
