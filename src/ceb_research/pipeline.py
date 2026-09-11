import hashlib
import json
from dataclasses import asdict, dataclass
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

from .format import parse_ceb, unwrap_stream_key
from .pdf import decode_pdf


@dataclass(frozen=True, slots=True)
class ConversionReport:
    source: str
    source_sha256: str
    source_size: int
    magic: str
    version: int
    index_count: int
    page_count: int
    text_chars: int
    extraction: str
    stream_algorithm: int
    stream_key_length: int
    pdf: str
    markdown: str
    text: str
    report: str


def _extract_pages(pdf_data: bytes) -> tuple[str, ...]:
    with BytesIO(pdf_data) as stream:
        document = PdfReader(stream)
        return tuple(page.extract_text() or "" for page in document.pages)


def _markdown(title: str, pages: tuple[str, ...]) -> str:
    sections = [f"# {title}"]
    for index, page in enumerate(pages, start=1):
        sections.extend((f"## 第{index}页", page.rstrip()))
    return "\n\n".join(sections) + "\n"


def convert_file(source: Path, output_dir: Path) -> ConversionReport:
    output_dir.mkdir(parents=True, exist_ok=True)
    document = parse_ceb(source)
    pdf_data = decode_pdf(document)
    pages = _extract_pages(pdf_data)
    stem = source.stem
    pdf_path = output_dir / f"{stem}.pdf"
    markdown_path = output_dir / f"{stem}.md"
    text_path = output_dir / f"{stem}.txt"
    report_path = output_dir / f"{stem}.conversion.json"
    text = "\n\n".join(page.rstrip() for page in pages).strip() + "\n"
    _ = pdf_path.write_bytes(pdf_data)
    _ = markdown_path.write_text(_markdown(stem, pages), encoding="utf-8")
    _ = text_path.write_text(text, encoding="utf-8")
    stream_spec = unwrap_stream_key(document)
    report = ConversionReport(
        source=str(source),
        source_sha256=hashlib.sha256(document.data).hexdigest(),
        source_size=len(document.data),
        magic=document.magic,
        version=document.version,
        index_count=len(document.entries),
        page_count=len(pages),
        text_chars=len(text),
        extraction="text-layer" if text.strip() else "empty-text-layer",
        stream_algorithm=stream_spec.algorithm,
        stream_key_length=len(stream_spec.key),
        pdf=str(pdf_path),
        markdown=str(markdown_path),
        text=str(text_path),
        report=str(report_path),
    )
    _ = report_path.write_text(
        json.dumps(asdict(report), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return report
