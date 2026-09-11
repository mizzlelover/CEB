from io import BytesIO
from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from ceb_research.cli import batch, iter_ceb_files
from ceb_research.format import (
    CebFormatError,
    decrypt_pdf_data,
    parse_ceb,
    unwrap_stream_key,
)
from ceb_research.pdf import decode_pdf
from ceb_research.pipeline import convert_file

MAGIC = b"Founder CEB\x00"
HEADER_SIZE = 31
INDEX_SIZE = 17


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


def _write_synthetic_ceb(path: Path, algorithm: int = 0) -> None:
    writer = PdfWriter()
    _ = writer.add_blank_page(width=595, height=842)
    pdf_stream = BytesIO()
    _ = writer.write(pdf_stream)
    pdf_data = pdf_stream.getvalue()
    rc4_key = b"public-test-key"
    entries = (
        (3, _rc4_block(pdf_data, rc4_key)),
        (4, rc4_key),
        (5, b"test-stream-key"),
        (16, algorithm.to_bytes(4, "little")),
    )
    table_end = HEADER_SIZE + len(entries) * INDEX_SIZE
    payload = bytearray(table_end)
    payload[: len(MAGIC)] = MAGIC
    payload[14:16] = (3).to_bytes(2, "little")
    payload[20:22] = len(entries).to_bytes(2, "little")
    offset = table_end
    for index, (kind, value) in enumerate(entries):
        index_offset = HEADER_SIZE + index * INDEX_SIZE
        payload[index_offset : index_offset + 4] = offset.to_bytes(4, "little")
        payload[index_offset + 4 : index_offset + 8] = len(value).to_bytes(4, "little")
        payload[index_offset + 8 : index_offset + 12] = kind.to_bytes(4, "little")
        payload.extend(value)
        offset += len(value)
    _ = path.write_bytes(payload)


@pytest.fixture
def ceb_fixture(tmp_path: Path) -> Path:
    path = tmp_path / "sample.ceb"
    _write_synthetic_ceb(path)
    return path


def test_parse_ceb_recovers_header_and_index_count(ceb_fixture: Path) -> None:
    document = parse_ceb(ceb_fixture)

    assert document.magic == "Founder CEB"
    assert document.version == 3
    assert len(document.entries) == 4


def test_native_decryption_recovers_pdf_and_stream_key(ceb_fixture: Path) -> None:
    document = parse_ceb(ceb_fixture)

    pdf_data = decrypt_pdf_data(document)
    stream_key = unwrap_stream_key(document)

    assert pdf_data.startswith(b"%PDF-")
    assert stream_key.algorithm == 0
    assert stream_key.key == b"test-stream-key"


def test_decode_pdf_keeps_a_valid_pdf(ceb_fixture: Path) -> None:
    document = parse_ceb(ceb_fixture)

    pdf_data = decode_pdf(document)
    reader = PdfReader(BytesIO(pdf_data))

    assert len(reader.pages) == 1


def test_decode_pdf_rejects_unknown_stream_algorithm(ceb_fixture: Path) -> None:
    _write_synthetic_ceb(ceb_fixture, algorithm=99)

    with pytest.raises(CebFormatError, match="unsupported CEB stream cipher"):
        _ = decode_pdf(parse_ceb(ceb_fixture))


def test_convert_file_writes_ai_ready_artifacts(
    ceb_fixture: Path, tmp_path: Path
) -> None:
    report = convert_file(ceb_fixture, tmp_path)

    assert report.page_count == 1
    assert (tmp_path / "sample.pdf").is_file()
    assert (tmp_path / "sample.md").is_file()
    assert (tmp_path / "sample.txt").is_file()
    assert (tmp_path / "sample.conversion.json").is_file()


def test_iter_ceb_files_supports_recursive_and_flat_scans(tmp_path: Path) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    first = tmp_path / "first.ceb"
    second = nested / "second.ceb"
    first.touch()
    second.touch()

    assert iter_ceb_files(tmp_path, recursive=False) == (first,)
    assert iter_ceb_files(tmp_path, recursive=True) == (first, second)


def test_batch_preserves_input_subdirectories(
    ceb_fixture: Path, tmp_path: Path
) -> None:
    input_dir = tmp_path / "input"
    nested = input_dir / "nested"
    nested.mkdir(parents=True)
    source = nested / "sample.ceb"
    _ = source.write_bytes(ceb_fixture.read_bytes())

    batch(input_dir, tmp_path / "output", recursive=True)

    output_dir = tmp_path / "output" / "nested"
    assert (output_dir / "sample.pdf").is_file()
    assert (output_dir / "sample.md").is_file()
    assert (output_dir / "sample.txt").is_file()
    assert (output_dir / "sample.conversion.json").is_file()
