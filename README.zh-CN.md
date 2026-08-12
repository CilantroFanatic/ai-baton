# ai-baton

[English](README.md)

便携、可审计、文件优先的 AI 助手交接协议。

在 Claude Code、Codex CLI、Cursor,或者任何能读写文件的工具之间切换,同一个长期项目不用每次重新解释背景。状态全部存在你自己仓库里的纯 Markdown + YAML 文件里:`memory/` 存长期事实和决定,`status/CURRENT_STATUS.md` 存现在正在做什么,`evidence/` 是只追加的原始记录,`handover/` 存交接快照,`archive/` 存被取代的旧方案。不需要服务器、不需要向量数据库、不需要任何厂商插件——每一次改动都只是一次 git diff。

需要本地文件系统访问权限——适用于跑在你电脑上、或者被授权访问某个文件夹的工具(Claude Code、Codex CLI、Cursor、Windsurf、装了文件系统连接器的 Claude Desktop 等)。纯网页版 ChatGPT 或网页版 Claude.ai 聊天界面,没有文件访问权限,读不到 `PROTOCOL.md`,不管支不支持 Agent Skills 都没用。

不是第一个想做跨工具 AI 记忆的系统——Mem0、OpenMemory、Letta 解决的是类似的问题,靠的是向量库和/或 agent 运行时。这个项目走的是相反的取舍:零基础设施、Git 原生可审计,代价是没有语义搜索和自动抽取。详见 [`docs/comparison.md`](docs/comparison.md)。

## 现状

Pre-alpha。`pip install ai-baton-tool`(PyPI 上的发行包名跟 `ai-baton` 命令不一样——名字被一个不相关的已有包占了)。已经跑通的:协议规范(`SPEC.md`)、`init`/`validate`/`status`/`list`/`workspace set`/`skill install` 这几个 CLI 命令、一套默认工作区约定(`~/ai-baton-workspace/<项目名>/`,根目录只在第一次用的时候问一次、记在 `~/.ai-baton/config.json` 里,换工具/换会话时靠 `ai-baton list` 就能发现已有项目)、一个完整的示例项目(`examples/demo-project/`)、一份 [Agent Skills](https://agentskills.io/) skill——`ai-baton skill install` 会把它放到 Claude Code、Codex CLI、GitHub Copilot 都会找的位置,这三个里都现场验证过能触发(Codex 那次是真实用户测试:能发现 skill、检查工作区、正确建出新项目,但没确认是否遵守了每一条细则,比如 `[baton: held]` 哨兵标记和引导式提问没出现,不确定是 Codex 没遵守规则,还是它本来就没有弹窗能力、按规则正确回退成了纯文字;Copilot 那次也是真实用户测试,并且直接测出了两个真实 bug——把不相关的兄弟项目内容读进了新项目、跳过了该问的整合确认——都已经修复)。Cursor 还没实测过,不过 Cursor 官方文档说它读取 skill 的位置跟这个工具安装进去的 `.agents/skills/`/`.claude/skills/` 是同一批。`validate` 还会检测常见凭证格式(AWS/GitHub/Slack key、私钥块)作为一道启发式安全网,不是完整的密钥扫描工具;`memory/` 变大到会明显增加每次会话的 token 开销时也会警告,阈值可以按项目通过 `.ai-baton.json` 自定义。路径不对时现在会给出人话错误提示,不再是 Python 报错栈。49 个测试本地全过。还没做的:语义搜索(有意不做)、任何自动化的交接效果量化(方法论写在 `docs/metrics.md` 里,还没接进代码)。

## 快速上手

- [`docs/quickstart.md`](docs/quickstart.md) —— 安装和试用(英文)。
- [`SPEC.md`](SPEC.md) —— 协议本身(英文)。
- [`docs/comparison.md`](docs/comparison.md) —— 跟 Mem0 / OpenMemory / Letta / Letta Code 的对比(英文)。
- [`docs/metrics.md`](docs/metrics.md) —— 打算怎么衡量交接效果(英文)。
- [`examples/demo-project/`](examples/demo-project/) —— 完整示例。
- [`.agents/skills/ai-baton/SKILL.md`](.agents/skills/ai-baton/SKILL.md) —— 装一次,AI 工具就会自动遵守协议,不用每次提醒。

## License

MIT —— 见 [`LICENSE`](LICENSE)。
