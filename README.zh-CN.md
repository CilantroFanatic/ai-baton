# ai-baton

[English](README.md)

便携、可审计、文件优先的 AI 助手交接协议。

在 Claude Code、Codex CLI、Cursor、GitHub Copilot,或者任何能读写文件的工具之间切换,同一个长期项目不用每次重新解释背景。状态全部存在你自己仓库里的纯 Markdown + YAML 文件里,能直接 `git diff` 看改动。不需要服务器、不需要向量数据库、不需要任何厂商插件。

## 什么时候用得上

- **同一个项目,换了个 AI 工具接着做。** 你在 Claude Code 里跟一个项目聊了两周,定好了技术选型、踩过的坑都摸清楚了,现在想换到 Cursor 里写代码——不想把这两周的决定重新讲一遍。
- **同一个项目,来回换着用几个工具。** 白天在公司用 Cursor,晚上回家用 Claude Code;或者你俩一个用 Codex 一个用 Claude Code 协作同一个仓库——大家读的是同一份文件,不用互相同步"现在做到哪了"。
- **对话记录太长,已经没法直接翻。** 开新会话(为了省 token,或者因为上下文太长回答质量会变差)不该等于丢掉之前的一切——几百字提炼好的状态,比重新塞一整段聊天记录划算。

## 怎么运作

- `PROTOCOL.md` —— 这个项目该遵守的规则
- `memory/` —— 沉淀下来的事实和决定,一个文件一条,标注 `confidence: verified` 或 `unverified`
- `status/CURRENT_STATUS.md` —— 现在在做什么(每次覆盖写,不是追加)
- `evidence/` —— 值得留存的原始细节,只追加
- `handover/` / `archive/` —— 交接快照 / 被取代的旧方案——不会删除任何东西

装一次 [Agent Skills](https://agentskills.io/) skill(`ai-baton skill install`),支持的 AI 工具就会自动照做:按正确顺序读文件、写之前先问、及时更新状态——不用每次提醒。

需要本地文件系统访问权限——适用于跑在你电脑上、或者被授权访问某个文件夹的工具(Claude Code、Codex CLI、Cursor、Windsurf、装了文件系统连接器的 Claude Desktop 等)。纯网页版 ChatGPT 或网页版 Claude.ai 聊天界面,没有文件访问权限,读不到 `PROTOCOL.md`,不管支不支持 Agent Skills 都没用。

## 现状

Pre-alpha。

**已经跑通的:**
- 协议规范(`SPEC.md`)和 CLI —— `pip install ai-baton-tool`(PyPI 上的发行包名跟 `ai-baton` 命令不一样,名字被一个不相关的已有包占了,但命令本身还是 `ai-baton`):`init` / `validate` / `status` / `list` / `workspace set` / `skill install`
- 一套默认工作区约定 —— `~/ai-baton-workspace/<项目名>/`,根目录只在第一次用的时候问一次、记住,换工具/换会话时靠 `ai-baton list` 就能发现已有项目
- 一个完整的示例项目(`examples/demo-project/`)
- `validate` 会检测常见凭证格式(启发式安全网,不是完整的密钥扫描工具),`memory/` 变大到会明显增加每次会话的 token 开销时也会警告(阈值可以按项目通过 `.ai-baton.json` 自定义)
- 路径不对时给出人话错误提示,不是 Python 报错栈
- 49 个测试本地全过

**现场验证过**(真实用户测试,不只是设计review):在 Claude Code、Codex CLI、GitHub Copilot 里都确认能触发。Copilot 那次测试直接测出、并推动修复了两个真实 bug——把不相关的兄弟项目内容读进了新项目、跳过了该问的整合确认。Codex CLI 里没确认 `[baton: held]` 哨兵标记和引导式提问是否出现过,不确定是真的没遵守规则,还是它本来就没有弹窗能力、按规则正确回退成了纯文字。Cursor 还没实测过,不过 Cursor 官方文档说它读取 skill 的位置跟这个工具安装进去的位置是同一批。

**还没做的:** 语义搜索(有意不做,见下面的取舍说明)、任何自动化的交接效果量化(方法论写在 `docs/metrics.md` 里,还没接进代码)。

不是第一个想做跨工具 AI 记忆的系统——Mem0、OpenMemory、Letta 解决的是类似的问题,靠的是向量库和/或 agent 运行时。这个项目走的是相反的取舍:零基础设施、Git 原生可审计,代价是没有语义搜索和自动抽取。详见 [`docs/comparison.md`](docs/comparison.md)。

## 快速上手

- [`docs/quickstart.md`](docs/quickstart.md) —— 安装和试用(英文)。
- [`SPEC.md`](SPEC.md) —— 协议本身(英文)。
- [`docs/comparison.md`](docs/comparison.md) —— 跟 Mem0 / OpenMemory / Letta / Letta Code 的对比(英文)。
- [`docs/metrics.md`](docs/metrics.md) —— 打算怎么衡量交接效果(英文)。
- [`examples/demo-project/`](examples/demo-project/) —— 完整示例。
- [`.agents/skills/ai-baton/SKILL.md`](.agents/skills/ai-baton/SKILL.md) —— 装一次,AI 工具就会自动遵守协议,不用每次提醒。

## License

MIT —— 见 [`LICENSE`](LICENSE)。
