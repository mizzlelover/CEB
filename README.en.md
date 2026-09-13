# CEB: Founder CEB to AI-readable files

> **Information security reminder (please read first)**
> This Skill converts files; it does not determine whether a file may be shared. Do not upload internal, confidential, sensitive, restricted, or explicitly non-public enterprise files to an unauthorized online model, third-party service, or public repository. Before use, confirm that the file may enter the selected processing environment under your organization’s information-security, data-classification, confidentiality, and authorization requirements; redact it when necessary. If a local or enterprise-internal large model is available, deploy this Skill inside that controlled environment and apply the organization’s own access, storage, logging, transfer, and output-file controls.

CEB is a native converter and reusable Codex Skill for verified Founder CEB v3 paths. It restores the embedded PDF data and writes standard PDF, page-aware Markdown, plain text, and a structured conversion report.

## Why this exists

In AI-assisted work, people increasingly upload every document before asking for analysis. In state-owned and large enterprise environments, document formats often lag behind the rest of the workflow: legacy DOC files remain common, DOCX adoption can be uneven, and early CEB files are still in circulation.

The dangerous part is that a failed CEB parse may not look like a failure. An AI system can produce an answer without making it obvious that the source text was never available. The problem is discovered only when someone checks the citations and finds that the material was never actually used.

Manual export is not a good fallback. The Founder reader can be slow, its export workflow is inconvenient, and repeated one-file-at-a-time handling becomes painful as soon as a folder contains more than a few documents.

This project started with a real family workflow: my wife gave me a batch of enterprise documents. The upload appeared to work, but the CEB files were not being read correctly. The only practical option was to export them one by one. CEB turns that painful detour into a repeatable batch workflow.

## Features

- Parses the `Founder CEB` header and 17-byte index table.
- Restores the embedded PDF data without requiring the Founder reader.
- Handles the verified content-stream algorithms 1 and 2.
- Writes PDF, page-aware Markdown, plain text, and JSON conversion reports.
- Provides a `ceb batch` command that preserves relative input directories.
- Fails clearly on unsupported structures instead of emitting a misleading pseudo-PDF.

## Install

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/mizzlelover/CEB.git
cd CEB
uv sync
```

Convert one file:

```bash
uv run ceb convert "/path/to/document.ceb" \
  --output-dir ./ceb-output
```

Convert a folder recursively:

```bash
uv run ceb batch "/path/to/ceb-files" \
  --output-dir ./ceb-output
```

Use `--no-recursive` to scan only the supplied directory. Each input produces four artifacts:

```text
document.pdf
document.md
document.txt
document.conversion.json
```

The JSON report records the source SHA-256, source size, CEB version, index count, page count, stream algorithm, extracted text length, and output paths.

## Verified scope

The current implementation targets confirmed Founder CEB v3 files using index types 3/4/5/16 and content-stream algorithms 1/2. During the research phase, 45 file paths from the project corpus were converted through the real batch workflow with 45/45 success: 25 used algorithm 1 and 20 used algorithm 2. The corpus included archived duplicates, so this result is a validation record, not a claim about every CEB file in existence.

Unknown versions, missing indexes, malformed RSA-wrapped keys, unknown stream algorithms, and invalid Flate data fail with a source-specific format error. Scanned-image pages may require OCR after conversion.

## Codex Skill

See [SKILL.md](SKILL.md) for the agent-facing workflow. The Skill prefers batch conversion for folders and requires checking the generated artifacts and conversion reports before claiming that a document was read successfully.

## Agent compatibility

The repository includes project-level discovery entry points for Codex, Claude Code, Trae Code, WorkBuddy, Kimi Code, and opencode. All six load the same core instructions; only the discovery directory and invocation method differ. See [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md).

## Who is the expert

CEB is a “谁是专家” project: a small tool built around a real workflow failure, with the goal of making difficult enterprise material usable in an AI-native process.

- X: [Who Is the Expert](https://x.com/dboy_yi2025)
- Xiaohongshu: [谁是专家](https://www.xiaohongshu.com/user/profile/64dd6c680000000001011d25)
- WeChat: search for “谁是专家”. The QR/search material is included below.

![Search for 谁是专家 on WeChat](assets/wechat-who-is-expert.png)

## Development

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run basedpyright
```

## License

MIT. See [LICENSE](LICENSE).
