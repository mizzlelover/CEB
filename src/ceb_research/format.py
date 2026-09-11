from dataclasses import dataclass
from pathlib import Path
from typing import Final, override

MAGIC: Final = b"Founder CEB\x00"
HEADER_SIZE: Final = 31
INDEX_SIZE: Final = 17
PDFDATA: Final = 3
RC4KEY: Final = 4
STREAM_KEY: Final = 5
STREAM_ALGORITHM: Final = 16
RSA_MODULUS: Final = bytes.fromhex(
    "".join(
        (
            "91437cd83d0722ce410bd96ca80cff34",
            "895a315e25128bc32529d5f614e45097",
            "e12e450c68daf1ad8d8e740ab708564f",
            "4f317b8012c44856de567d58522497db",
        )
    )
)
RSA_EXPONENT: Final = bytes.fromhex(
    "".join(
        (
            "f384ff17a8165a0eceb0a526f54412a9",
            "9a88ec6968b5e14faf7a08bee92ffde3",
            "5b18c54697d86ecc639700e642bc9175",
            "7e522dc5ef4c95ccd746d2d259db00c5",
        )
    )
)
MAX_STREAM_KEY_LENGTH: Final = 32


class CebFormatError(Exception):
    def __init__(self, path: Path, reason: str) -> None:
        self.path: Path = path
        self.reason: str = reason
        super().__init__(path, reason)

    @override
    def __str__(self) -> str:
        return f"{self.path}: {self.reason}"


@dataclass(frozen=True, slots=True)
class CebIndexItem:
    offset: int
    length: int
    kind: int
    marker: bytes


@dataclass(frozen=True, slots=True)
class StreamCipherSpec:
    algorithm: int
    key: bytes


@dataclass(frozen=True, slots=True)
class CebDocument:
    path: Path
    data: bytes
    magic: str
    version: int
    entries: tuple[CebIndexItem, ...]

    def find(self, kind: int) -> CebIndexItem | None:
        for entry in self.entries:
            if entry.kind == kind:
                return entry
        return None

    def payload(self, entry: CebIndexItem) -> bytes:
        return self.data[entry.offset : entry.offset + entry.length]


def _read_u32(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 4], "little")


def parse_ceb(path: Path) -> CebDocument:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise CebFormatError(path, f"cannot read file: {exc}") from exc
    if len(data) < HEADER_SIZE or data[: len(MAGIC)] != MAGIC:
        raise CebFormatError(path, "missing Founder CEB header")
    version = int.from_bytes(data[14:16], "little")
    count = int.from_bytes(data[20:22], "little")
    table_end = HEADER_SIZE + count * INDEX_SIZE
    if table_end > len(data):
        raise CebFormatError(path, "index table extends beyond file")
    entries: list[CebIndexItem] = []
    for index in range(count):
        offset = HEADER_SIZE + index * INDEX_SIZE
        item_offset = _read_u32(data, offset)
        item_length = _read_u32(data, offset + 4)
        marker = data[offset + 8 : offset + INDEX_SIZE]
        if item_offset + item_length > len(data):
            raise CebFormatError(path, f"index {index} payload extends beyond file")
        entries.append(
            CebIndexItem(
                offset=item_offset,
                length=item_length,
                kind=_read_u32(marker, 0),
                marker=marker,
            )
        )
    return CebDocument(path, data, MAGIC[:-1].decode("ascii"), version, tuple(entries))


def _rc4_block(data: bytes, key: bytes) -> bytes:
    seed = bytes(value | 0xAA for value in key)
    state = list(range(256))
    index = 0
    for position in range(256):
        index = (index + seed[position % len(seed)] + state[position]) % 256
        state[position], state[index] = state[index], state[position]
    x = 0
    y = 0
    output = bytearray(data)
    for position in range(len(output)):
        x = (x + 1) % 256
        y = (state[x] + y) % 256
        old = state[x]
        state[x] = state[y]
        state[y] = state[old]
        output[position] ^= state[(state[x] + state[y]) % 256]
    return bytes(output)


def decrypt_pdf_data(document: CebDocument) -> bytes:
    pdf_item = document.find(PDFDATA)
    key_item = document.find(RC4KEY)
    if pdf_item is None or key_item is None:
        raise CebFormatError(document.path, "PDFDATA or RC4KEY index is missing")
    key = document.payload(key_item)
    encrypted = document.payload(pdf_item)
    return b"".join(
        _rc4_block(encrypted[offset : offset + 65536], key)
        for offset in range(0, len(encrypted), 65536)
    )


def unwrap_stream_key(document: CebDocument) -> StreamCipherSpec:
    key_item = document.find(STREAM_KEY)
    algorithm_item = document.find(STREAM_ALGORITHM)
    if key_item is None or algorithm_item is None:
        raise CebFormatError(document.path, "stream key or algorithm index is missing")
    raw_algorithm = int.from_bytes(document.payload(algorithm_item), "little")
    encrypted_key = document.payload(key_item)
    if raw_algorithm & 0x80000000:
        modulus = int.from_bytes(RSA_MODULUS, "little")
        exponent = int.from_bytes(RSA_EXPONENT, "little")
        value = pow(int.from_bytes(encrypted_key, "little"), exponent, modulus)
        decoded = value.to_bytes(len(RSA_MODULUS), "little")
        length = int.from_bytes(decoded[:4], "little")
        if length > MAX_STREAM_KEY_LENGTH or length + 4 > len(decoded):
            raise CebFormatError(document.path, "RSA stream key length is invalid")
        key = decoded[4 : length + 4]
    else:
        if len(encrypted_key) > MAX_STREAM_KEY_LENGTH:
            raise CebFormatError(document.path, "plain stream key is too long")
        key = encrypted_key
    return StreamCipherSpec(raw_algorithm & 0x7FFFFFFF, key)
