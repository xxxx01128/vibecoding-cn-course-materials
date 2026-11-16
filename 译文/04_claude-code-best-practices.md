# Claude Code 概览 - Claude Code 文档

> 来源: https://www.anthropic.com/engineering/claude-code-best-practices

Claude Code 是一款由 AI 驱动的编码助手，帮助你构建功能、修复 bug 并自动化开发任务。它理解你的整个代码库，能够跨多个文件和工具协同工作以完成任务。

## 快速开始

选择你的使用环境来开始。大多数平台都需要一个 [Claude 订阅](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=overview_pricing) 或 [Anthropic Console](https://console.anthropic.com/) 账号。Terminal CLI 和 VS Code 还支持 [第三方提供商](https://www.anthropic.com/docs/en/third-party-integrations)。
- Terminal（终端）
- VS Code
- 桌面应用
- Web
- JetBrains

功能最全的 CLI，可让你直接在终端里使用 Claude Code。通过命令行编辑文件、运行命令并管理整个项目。要安装 Claude Code，请使用以下方法之一：
- 原生安装（推荐）
- Homebrew
- WinGet

macOS、Linux、WSL：

```
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell：

```
irm https://claude.ai/install.ps1 | iex
```

Windows CMD：

```
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

如果你看到 `The token '&&' is not a valid statement separator`，说明你在 PowerShell 而不是 CMD 中。请改用上面的 PowerShell 命令。当你在 PowerShell 中时，提示符会显示 `PS C:\`。Windows 需要 [Git for Windows](https://git-scm.com/downloads/win)。如果还没有安装，请先安装。

原生安装会在后台自动更新，让你始终使用最新版本。

```
brew install --cask claude-code
```

Homebrew 安装不会自动更新。定期运行 `brew upgrade claude-code` 以获取最新功能和安全修复。

```
winget install Anthropic.ClaudeCode
```

WinGet 安装不会自动更新。定期运行 `winget upgrade Anthropic.ClaudeCode` 以获取最新功能和安全修复。

然后在任意项目中启动 Claude Code：

```
cd your-project
claude
```

首次使用时系统会提示你登录。就这么简单！[继续阅读快速入门 →](https://www.anthropic.com/docs/en/quickstart)

有关安装选项、手动更新或卸载说明，请参阅 [高级设置](https://www.anthropic.com/docs/en/setup)。如果遇到问题，请访问 [故障排查](https://www.anthropic.com/docs/en/troubleshooting)。

VS Code 扩展可直接在你的编辑器中提供行内 diff、@-提及、计划评审和对话历史。
- 安装 VS Code 版
- 安装 Cursor 版

或者在扩展视图中搜索「Claude Code」（Mac 上为 `Cmd+Shift+X`，Windows/Linux 上为 `Ctrl+Shift+X`）。安装后，打开命令面板（`Cmd+Shift+P`/`Ctrl+Shift+P`），输入「Claude Code」，然后选择「在新标签页中打开」。[开始使用 VS Code →](https://www.anthropic.com/docs/en/vs-code#get-started)

这是一个独立应用，让你在 集成开发环境（IDE）或终端之外运行 Claude Code。以可视化方式评审 diff、并排运行多个会话、安排周期性任务，并启动云端会话。下载并安装：
- macOS（Intel 与 Apple Silicon）
- Windows（x64）
- Windows ARM64（仅限远程会话）

安装后，启动 Claude，登录，然后点击 Code 标签页即可开始编码。需要 [付费订阅](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=overview_desktop_pricing)。[了解更多关于桌面应用的信息 →](https://www.anthropic.com/docs/en/desktop-quickstart)

在浏览器中运行 Claude Code，无需本地设置。启动长时间运行的任务，完成后再回来查看；处理你本地没有的代码仓库，或并行运行多个任务。可在桌面浏览器和 Claude iOS 应用上使用。前往 [claude.ai/code](https://claude.ai/code) 开始编码。[开始在 Web 上使用 →](https://www.anthropic.com/docs/en/claude-code-on-the-web#getting-started)

这是一个适用于 IntelliJ IDEA、PyCharm、WebStorm 及其他 JetBrains IDE 的插件，提供交互式 diff 查看和选中内容上下文共享。从 JetBrains Marketplace 安装 [Claude Code 插件](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) 并重启你的 IDE。[开始使用 JetBrains →](https://www.anthropic.com/docs/en/jetbrains)

## 你能做什么

以下是你可以使用 Claude Code 的一些方式：

自动化那些你一直拖延的工作

Claude Code 处理那些占用你一天时间的繁琐任务：为未经测试的代码编写测试、修复整个项目中的 lint 错误、解决合并冲突、更新依赖，以及编写发布说明。

```
claude "write tests for the auth module, run them, and fix any failures"
```

构建功能并修复 bug

用日常语言描述你想要什么。Claude Code 会规划方案、跨多个文件编写代码，并验证其可运行。对于 bug，粘贴一条错误消息或描述症状。Claude Code 会在你的代码库中追踪问题、定位根本原因并实施修复。更多示例请参阅 [常见工作流](https://www.anthropic.com/docs/en/common-workflows)。

创建提交和拉取请求（PR）

Claude Code 直接与 git 协作。它暂存改动、编写提交信息、创建分支并打开拉取请求。

```
claude "commit my changes with a descriptive message"
```

在 持续集成/持续交付（CI/CD）中，你可以用 [GitHub Actions](https://www.anthropic.com/docs/en/github-actions) 或 [GitLab CI/CD](https://www.anthropic.com/docs/en/gitlab-ci-cd) 自动化代码评审和 issue 分流。

用模型上下文协议（MCP）连接你的工具

[模型上下文协议（Model Context Protocol，MCP）](https://www.anthropic.com/docs/en/mcp) 是一项开放标准，用于把 AI 工具连接到外部数据源。借助 MCP，Claude Code 可以读取你在 Google Drive 中的设计文档、更新 Jira 中的工单、从 Slack 拉取数据，或使用你自己的定制工具。

用指令、技能和钩子进行定制

[CLAUDE.md](https://www.anthropic.com/docs/en/memory) 是一个你添加到项目根目录的 Markdown 文件，Claude Code 会在每次会话开始时读取它。用它来设定编码规范、架构决策、偏好的库和评审清单。Claude 在工作时还会建立 [自动记忆](https://www.anthropic.com/docs/en/memory#auto-memory)，跨会话保存诸如构建命令和调试心得等学到的内容，无需你写任何东西。创建 [自定义命令](https://www.anthropic.com/docs/en/skills) 来打包团队可共享的可重复工作流，比如 `/review-pr` 或 `/deploy-staging`。[钩子（Hooks）](https://www.anthropic.com/docs/en/hooks) 让你可以在 Claude Code 操作之前或之后运行 shell 命令，比如每次编辑文件后自动格式化，或在提交前运行 lint。

运行智能体团队并构建自定义智能体

派生出 [多个 Claude Code 智能体](https://www.anthropic.com/docs/en/sub-agents)，让它们同时处理任务的不同部分。一个主导智能体负责协调工作、分配子任务并合并结果。对于完全定制的工作流，[Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 让你构建由 Claude Code 的工具和能力驱动的自己的智能体，并完全掌控编排、工具访问权限和权限设置。

用 CLI 进行管道、脚本化和自动化

Claude Code 是可组合的，遵循 Unix 哲学。你可以把日志管道输入给它、在 CI 中运行它，或把它与其他工具串联：

```
# Analyze recent log output
tail -200 app.log | claude -p "Slack me if you see any anomalies"

# Automate translations in CI
claude -p "translate new strings into French and raise a PR for review"

# Bulk operations across files
git diff main --name-only | claude -p "review these changed files for security issues"
```

完整的命令和标志集合请参阅 [CLI 参考](https://www.anthropic.com/docs/en/cli-reference)。

安排周期性任务

按计划运行 Claude，自动化那些重复性的工作：早晨的 PR 评审、通宵的 CI 失败分析、每周的依赖审计，或在 PR 合并后同步文档。
- 云端计划任务运行在 Anthropic 管理的基础设施上，因此即使你的电脑关机，它们也会继续运行。可以从 Web、桌面应用创建，或在 CLI 中运行 /schedule 来创建。
- 桌面计划任务运行在你自己的机器上，可直接访问你的本地文件和工具
- /loop 在 CLI 会话内重复某个提示词，便于快速轮询

随时随地工作

会话不局限于单一平台。随着上下文变化，你可以在不同环境之间转移工作：
- 离开办公桌后，用远程控制（Remote Control）在手机或任意浏览器上继续工作
- 用手机上的 Message Dispatch 分派任务，并打开它创建的桌面会话
- 在 Web 或 iOS 应用上启动长时间运行的任务，然后用 `claude --teleport` 把它拉到你的终端里
- 用 /desktop 把终端会话交给桌面应用，进行可视化 diff 评审
- 从团队聊天中分派任务：在 Slack 中提及 @Claude 并附上 bug 报告，就能得到一个拉取请求

## 随处使用 Claude Code

每个平台都连接到同一个底层 Claude Code 引擎，因此你的 CLAUDE.md 文件、设置和 MCP 服务器在所有平台上都通用。除了上面的 [Terminal（终端）](https://www.anthropic.com/docs/en/quickstart)、[VS Code](https://www.anthropic.com/docs/en/vs-code)、[JetBrains](https://www.anthropic.com/docs/en/jetbrains)、[Desktop（桌面）](https://www.anthropic.com/docs/en/desktop) 和 [Web](https://www.anthropic.com/docs/en/claude-code-on-the-web) 环境之外，Claude Code 还与 持续集成/持续交付（CI/CD）、聊天和浏览器工作流集成：

| 我想要…… | 最佳选择 |
| --- | --- |
| 从手机或其他设备继续本地会话 | [远程控制（Remote Control）](https://www.anthropic.com/docs/en/remote-control) |
| 把来自 Telegram、Discord、iMessage 或我自己 webhook 的事件推入会话 | [频道（Channels）](https://www.anthropic.com/docs/en/channels) |
| 在本地启动任务，在移动端继续 | [Web](https://www.anthropic.com/docs/en/claude-code-on-the-web) 或 [Claude iOS 应用](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| 按周期运行 Claude | [云端计划任务](https://www.anthropic.com/docs/en/web-scheduled-tasks) 或 [桌面计划任务](https://www.anthropic.com/docs/en/desktop#schedule-recurring-tasks) |
| 自动化 PR 评审和 issue 分流 | [GitHub Actions](https://www.anthropic.com/docs/en/github-actions) 或 [GitLab CI/CD](https://www.anthropic.com/docs/en/gitlab-ci-cd) |
| 在每个 PR 上获得自动代码评审 | [GitHub Code Review](https://www.anthropic.com/docs/en/code-review) |
| 把 Slack 中的 bug 报告流转成拉取请求 | [Slack](https://www.anthropic.com/docs/en/slack) |
| 调试线上 Web 应用 | [Chrome](https://www.anthropic.com/docs/en/chrome) |
| 为你自己的工作流转构建自定义智能体 | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) |

## 后续步骤

安装好 Claude Code 后，这些指南能帮助你更深入：

- 快速入门：走完你的第一个真实任务，从探索代码库到提交修复
- 存储指令与记忆：用 CLAUDE.md 文件和自动记忆为 Claude 提供持久化指令
- 常见工作流与最佳实践：帮助你充分发挥 Claude Code 价值的模式
- 设置：根据你的工作流定制 Claude Code
- 故障排查：常见问题的解决方案
- code.claude.com：演示、定价和产品详情
