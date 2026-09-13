# CEB：把 Founder CEB 转成 AI 可处理的材料

> **信息安全提醒（请先阅读）**
> 本 Skill 用于文件转换，不会替你判断文件是否可以公开。请勿把企业内部、涉密、敏感、受限或明确禁止对外的文件，上传到未获授权的在线模型、第三方服务或公共仓库。使用前，请按所在单位的信息安全、数据分类分级、保密和授权要求，确认文件可以进入当前处理环境；必要时先完成脱敏。若已在本地或企业内网部署大模型，可将本 Skill 部署在内部环境使用，并由使用单位自行落实访问控制、存储、日志、传输和输出文件管理。

![公文排版 × CEB：从旧格式读取，到规范排版](punk-assets/punk-cover/gongwen-ceb-collaboration/cover.png)

> **配套工具：** [公文排版](https://github.com/mizzlelover/gongwen-gbt9704-skill) 负责规范整理中文正式材料；[CEB 文件转换](https://github.com/mizzlelover/CEB) 负责读取并转换已验证的 Founder CEB 文件。两个 Skill 可以连成一条“读取 → 整理 → 交付”的工作流。

CEB 是一个原生转换工具，也是一个可复用的 Codex Skill。它针对已验证的 Founder CEB v3 路径，直接恢复 PDF 内容流，再输出 PDF、Markdown、TXT 和结构化报告。

## 为什么做它

在 AI 时代，材料都想先交给 AI。但国企、央企内部的文件格式升级往往很慢：DOC 还很常见，DOCX 未必普及，早期 CEB 更是经常遇到。

麻烦在于：AI 对 CEB 解析失败时，不一定会老老实实报错。你以为它已经读完了，实际可能没有任何可用正文。等到后来核对依据，才发现前面的分析根本没有参考这份材料。

手工处理也不轻松：方正阅读器性能不稳定，导出体验差，而且通常不能一次批量导出。文件一多，就只能重复打开、导出、重命名、再上传。

这个项目的起点很简单：我老婆当时给了我一批材料。我把它们交给 AI，流程看起来很顺，后来才发现 CEB 根本没有被正确读取，只能一个个手工导出。于是把这件事做成一个可以批量处理的 Skill：把文件丢进去，转成 PDF、Markdown、TXT，再交给 AI。

## 能做什么

- 解析 `Founder CEB` 头和 17 字节索引表。
- 恢复 CEB 内部 PDF 数据。
- 解包已验证的内容流密钥，并处理算法 1/2 内容流。
- 输出 PDF、按页 Markdown、纯文本和 JSON 转换报告。
- 通过 `ceb batch` 批量转换，保留输入目录结构。
- 失败时明确指出源文件和原因，不把错误结果伪装成成功。

## 安装与使用

需要 Python 3.13+ 和 [uv](https://docs.astral.sh/uv/)。

```bash
git clone https://github.com/mizzlelover/CEB.git
cd CEB
uv sync
```

转换单个文件：

```bash
uv run ceb convert "/path/to/document.ceb" \
  --output-dir ./ceb-output
```

批量转换目录：

```bash
uv run ceb batch "/path/to/ceb-files" \
  --output-dir ./ceb-output
```

默认递归扫描所有 `.ceb` 文件，并按输入目录保留输出结构。只扫描当前目录时：

```bash
uv run ceb batch "/path/to/ceb-files" \
  --output-dir ./ceb-output \
  --no-recursive
```

## 输出说明

对 `通知.ceb`，输出目录会包含：

```text
通知.pdf
通知.md
通知.txt
通知.conversion.json
```

JSON 报告包含源文件 SHA-256、文件大小、CEB 版本、索引数、页数、内容流算法、文本字符数和各输出文件路径，方便追溯。

## 已验证范围

当前实现针对已确认的 Founder CEB v3、索引类型 3/4/5/16 和算法 1/2。研究阶段对项目内检索到的 45 个文件路径进行了真实批量转换，45/45 成功；其中 25 份使用算法 1，20 份使用算法 2。该统计包含归档重复件，不能外推为所有 CEB 文件都能转换。

未知版本、缺少关键索引、RSA 密钥异常、未知流算法或非法 Flate 数据会直接返回格式错误。扫描图像型页面可能只有空文本层，需要另行 OCR。

## Codex Skill

见根目录 [SKILL.md](SKILL.md)。当任务涉及读取、批量转换或核验 CEB 文件时，Skill 会优先建议批量处理，并要求检查输出文件与转换报告。

## 多平台支持

当前仓库已提供 Codex、Claude Code、Trae Code、WorkBuddy、Kimi Code 和 opencode 的项目级发现入口。六个平台共用同一份核心指令，区别只在安装目录和调用方式，详见 [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md)。

## 谁是专家

CEB 是“谁是专家”把工作流中的小痛点做成工具的一次实践。关注真实材料、真实失败和可以复用的解决方案。

- X：[https://x.com/dboy_yi2025](https://x.com/dboy_yi2025)
- 小红书：[https://www.xiaohongshu.com/user/profile/64dd6c680000000001011d25](https://www.xiaohongshu.com/user/profile/64dd6c680000000001011d25)
- 微信：搜索“谁是专家”，二维码见下方物料。

![微信搜一搜：谁是专家](assets/wechat-who-is-expert.png)

## 开发与验证

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run basedpyright
```

## License

MIT，见 [LICENSE](LICENSE)。
