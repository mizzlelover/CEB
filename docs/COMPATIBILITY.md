# CEB Skill compatibility

## 兼容结论

CEB 使用跨平台的 Agent Skills 目录结构：一个带 YAML frontmatter 的 `SKILL.md`，配合可选的脚本和资源。当前仓库已经为以下六个平台提供项目级发现入口：

| Agent | 项目级入口 | 手动调用或导入 |
| --- | --- | --- |
| Codex | `.agents/skills/ceb/SKILL.md` | 在 Codex 中使用 `$ceb` 或让它按描述自动选择 |
| Claude Code | `.claude/skills/ceb/SKILL.md` | 在 Claude Code 中使用 `/ceb` 或让它自动选择 |
| Trae Code | `.trae/skills/ceb/SKILL.md` | 在技能面板导入 `ceb` 文件夹或其中的 `SKILL.md` |
| WorkBuddy | `.agents/skills/ceb/SKILL.md`；另有带 WorkBuddy 元数据的 `platforms/workbuddy/ceb/SKILL.md` 和 `.codebuddy/skills/ceb/SKILL.md` | 在 Skill 市场导入 `platforms/workbuddy/ceb` 文件夹或 ZIP |
| Kimi Code | `.kimi-code/skills/ceb/SKILL.md`；也支持 `.agents/skills/ceb/SKILL.md` | 使用 `/skill:ceb` 或让它自动选择 |
| opencode | `.opencode/skills/ceb/SKILL.md`；也支持 `.agents` / `.claude` 兼容入口 | 使用原生 `skill` 工具或按描述自动加载 |

六个入口的内容保持一致，根目录 [SKILL.md](../SKILL.md) 是唯一规范源文件。同步副本通过 `scripts/sync-skill-entrypoints.sh` 生成。

## 运行前提

Skill 的加载格式是跨平台的；实际转换还需要在当前工作区具备 Python 3.13+ 和 `uv`，并从 CEB 工程目录运行：

```bash
uv sync
uv run ceb convert "/path/to/file.ceb" --output-dir ./ceb-output
uv run ceb batch "/path/to/folder" --output-dir ./ceb-output
```

这意味着“支持某个平台”包含两层：平台能够发现并加载 Skill；平台能够访问当前工作区的文件和命令行。若某个托管环境不允许执行本地命令，它仍然可以读取 Skill 指令，但不能完成原生转换。

## 安装方式

### Codex、Kimi Code 和共享 Agent Skills 目录

```bash
cp -R .agents/skills/ceb ~/.agents/skills/
```

### Claude Code

```bash
cp -R .claude/skills/ceb ~/.claude/skills/
```

### Trae Code

```bash
cp -R .trae/skills/ceb ~/.trae-cn/skills/
```

也可以直接在 Trae 的“技能与命令”中导入 `ceb` 文件夹或 ZIP。

### WorkBuddy

WorkBuddy 支持从技能市场导入本地技能包。推荐选择带有 WorkBuddy 专用展示字段的 `platforms/workbuddy/ceb` 文件夹，或把该文件夹压缩成 ZIP 后导入。若使用腾讯 CodeBuddy Code 兼容目录，可使用 `.codebuddy/skills/ceb`；项目级共享入口仍保留在 `.agents/skills/ceb`。

### opencode

```bash
cp -R .opencode/skills/ceb ~/.config/opencode/skills/
```

也可以直接把整个 CEB 工程作为项目打开；opencode 会从 `.opencode/skills`、`.claude/skills` 或 `.agents/skills` 发现同一个 Skill。

## 依据

- [Codex: Build skills](https://developers.openai.com/codex/skills/)
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Trae Code: 技能（Skill）](https://docs.trae.cn/ide_skills)
- [WorkBuddy: Skill](https://open.workbuddy.cn/en/docs/skill)
- [Kimi Code: Agent Skills](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)
- [opencode: Agent Skills](https://opencode.ai/docs/skills)

## English

CEB uses the portable Agent Skills shape: one `SKILL.md` with YAML frontmatter, plus optional scripts and assets. This repository includes project-level discovery copies for Codex, Claude Code, Trae Code, WorkBuddy, Kimi Code, and opencode.

The conversion logic itself remains one Python CLI. All hosts can load the same instructions, but the host must be able to access the checked-out repository and execute Python 3.13+ with `uv` to perform a real conversion.

The root [SKILL.md](../SKILL.md) is canonical. Keep the platform copies synchronized with:

```bash
scripts/sync-skill-entrypoints.sh
```

For the detailed host-specific paths and installation options, use the table above. The linked official documentation is the authority if a host changes its discovery rules.
