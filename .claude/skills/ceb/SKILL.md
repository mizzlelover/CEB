---
name: ceb
description: Convert verified Founder CEB files to PDF, Markdown, and TXT for AI-readable document workflows, including single-file and batch processing. Use when a task involves reading or validating .ceb files; do not use for unrelated PDF conversion.
metadata:
  display_name: "CEB 文件转换"
  display_name_en: "CEB Converter"
  description_zh: "将已验证的 Founder CEB 文件转换为 PDF、Markdown 和 TXT，适用于单文件、批量处理与读取核验。"
  description_en: "Convert verified Founder CEB files to PDF, Markdown, and TXT for single-file, batch, and validation workflows."
  version: "0.1.0"
  author: "谁是专家"
  compatibility: "Requires Python 3.13+ and uv; run commands from a checkout of the CEB repository."
  platforms: "codex, claude-code, trae-code, workbuddy, kimi-code, opencode"
  distribution: "Agent Skills SKILL.md"
---

# CEB Skill

## 中文

### 触发条件

当用户要读取、转换、批量处理或核验 `.ceb` / Founder CEB 文件时，使用本 Skill。

### 工作流

1. 先确认输入路径、文件数量和是否需要保留目录结构。
2. 单个文件使用 `ceb convert`；目录使用 `ceb batch`。
3. 默认输出 PDF、Markdown、TXT 和 `.conversion.json`，不要只输出一个“看起来成功”的结论。
4. 检查转换报告、页数、文本字符数和输出文件是否存在。
5. 发现格式错误、空文本层或不支持的算法时，明确报告源文件和原因；不要把猜测内容当成正文。

### 命令

```bash
uv run ceb convert "/path/to/file.ceb" --output-dir ./ceb-output
uv run ceb batch "/path/to/folder" --output-dir ./ceb-output
uv run ceb batch "/path/to/folder" --output-dir ./ceb-output --no-recursive
```

### 多平台加载

本文件是唯一规范入口。仓库同时提供与各平台发现目录一致的同步副本，详见 [CEB compatibility guide](https://github.com/mizzlelover/CEB/blob/main/docs/COMPATIBILITY.md)。修改指令后，从仓库根目录运行 `scripts/sync-skill-entrypoints.sh` 更新副本，不要只改某个平台目录。

### 支持边界

当前实现针对已验证的 Founder CEB v3、索引类型 3/4/5/16 和内容流算法 1/2。未知版本、关键索引缺失、密钥异常、未知算法和非法 Flate 数据必须失败关闭。扫描图像页面转换后可能没有文本，需要另外做 OCR。

### 给 AI 的核验要求

- 转换失败时，不要声称已经阅读原文。
- 输出 Markdown 为空或文本字符数为 0 时，提醒用户这可能是扫描件或无文本层。
- 引用正文前，优先读取生成的 `.md` / `.txt`，并保留源文件路径。
- 批量任务结束时，报告成功数、失败数和失败文件列表。

## English

### When to use

Use this Skill when a task involves reading, converting, batch-processing, or validating `.ceb` / Founder CEB files.

### Workflow

1. Confirm the input path, file count, and whether relative directories must be preserved.
2. Use `ceb convert` for one file and `ceb batch` for a directory.
3. Expect PDF, Markdown, TXT, and `.conversion.json` outputs. Do not report success from a command exit alone.
4. Inspect the conversion report, page count, text length, and output files.
5. If a format error, empty text layer, or unsupported algorithm appears, report the source and reason. Never treat guessed text as source content.

### Commands

```bash
uv run ceb convert "/path/to/file.ceb" --output-dir ./ceb-output
uv run ceb batch "/path/to/folder" --output-dir ./ceb-output
uv run ceb batch "/path/to/folder" --output-dir ./ceb-output --no-recursive
```

### Cross-platform loading

This file is the canonical entry point. The repository also contains synchronized copies in the discovery directories used by the supported agents; see the [CEB compatibility guide](https://github.com/mizzlelover/CEB/blob/main/docs/COMPATIBILITY.md). After changing the instructions, run `scripts/sync-skill-entrypoints.sh` from the repository root instead of editing one platform copy in isolation.

### Support boundary

The current implementation targets verified Founder CEB v3 files using index types 3/4/5/16 and content-stream algorithms 1/2. Unknown versions, missing indexes, malformed keys, unknown algorithms, and invalid Flate data must fail closed. Scanned pages may need OCR after conversion.

### Agent verification requirements

- Do not claim to have read a source file when conversion failed.
- If Markdown is empty or the extracted text length is zero, tell the user it may be a scan or have no text layer.
- Read the generated `.md` / `.txt` before citing document content, and keep the source path in the result.
- At the end of a batch, report successes, failures, and failed file paths.
