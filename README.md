# CEB

![公文排版 × CEB：从旧格式读取，到规范排版](punk-assets/punk-cover/gongwen-ceb-collaboration/cover.png)

> **配套工具：** [公文排版](https://github.com/mizzlelover/gongwen-gbt9704-skill) 负责把中文正式材料整理成符合 GB/T 9704-2012 的可编辑 DOCX；[CEB 文件转换](https://github.com/mizzlelover/CEB) 负责把已验证的 Founder CEB 文件转换为 PDF、Markdown、TXT。两个 Skill 可以连成一条“读取 → 整理 → 交付”的工作流。

**Founder CEB → PDF / Markdown / TXT**

把老格式公文，变成 AI 真正能读的材料。

[中文说明](README.zh-CN.md) · [English](README.en.md) · [Skill 使用说明](SKILL.md) · [跨平台兼容](docs/COMPATIBILITY.md) · [项目介绍](ABOUT.md)

## 这是什么

CEB 是一个面向 Founder CEB 文件的原生转换工具和 Codex Skill。它不要求安装方正阅读器，直接解析已验证的 Founder CEB v3 路径，并输出常规 PDF、按页 Markdown、纯文本和结构化转换报告。

它解决的是一个很具体、但在国企和央企材料处理中非常费时间的问题：文件看起来已经“喂给 AI”了，AI 却可能没有读到 CEB 正文，而且未必会明确告诉你解析失败。

## 30 秒开始

```bash
uv sync

# 转换一个文件
uv run ceb convert "/path/to/document.ceb" --output-dir ./ceb-output

# 批量转换整个目录，保留输入目录结构
uv run ceb batch "/path/to/ceb-files" --output-dir ./ceb-output
```

每个文件会生成：

- `*.pdf`：可用常规 PDF 工具打开的文件
- `*.md`：按页组织、适合 AI 处理的 Markdown
- `*.txt`：连续纯文本
- `*.conversion.json`：源文件哈希、版本、索引数、页数、算法和输出路径

## 当前边界

当前版本针对已验证的 Founder CEB v3、索引类型 3/4/5/16，以及内容流算法 1/2。遇到未知版本、缺少关键索引、密钥封装异常或非法数据时会明确失败，不输出伪 PDF。扫描图像型页面仍需要 OCR 或后续图像处理。

## 由谁是专家发起

这个项目来自一次真实的家庭场景：一批国企材料需要交给 AI 处理，DOC、DOCX、PDF 都不难，偏偏早期 CEB 让流程卡住；方正阅读器慢，导出不稳定，也不适合十几个文件逐个手工操作。于是把一次性转换整理成一个可复用的 Skill。

> “谁是专家”关注的不是把 AI 说得多神，而是把真实工作流里那些不起眼、却会反复消耗人的阻力清掉。

X：[谁是专家](https://x.com/dboy_yi2025) · 小红书：[谁是专家](https://www.xiaohongshu.com/user/profile/64dd6c680000000001011d25)

![微信搜一搜：谁是专家](assets/wechat-who-is-expert.png)

更多双语宣传文案见 [docs/PROMOTION.zh-CN.md](docs/PROMOTION.zh-CN.md) 和 [docs/PROMOTION.en.md](docs/PROMOTION.en.md)。

## License

MIT

---

**Founder CEB → PDF / Markdown / TXT**

Turn legacy enterprise documents into material that AI can actually process.

CEB is a native converter and Codex Skill for verified Founder CEB v3 paths. It produces standard PDF, page-aware Markdown, plain text, and a structured conversion report without requiring the Founder reader.

Read the full English guide in [README.en.md](README.en.md).
