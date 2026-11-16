# 构建远程 MCP 服务器 · Cloudflare Agents 文档

> 来源: https://developers.cloudflare.com/agents/guides/remote-mcp-server/

astro:end

# 构建远程 MCP 服务器

本指南将向你展示如何使用 Streamable HTTP 传输（当前的模型上下文协议（MCP）规范标准）在 Cloudflare 上部署你自己的远程 MCP 服务器。你有两种选择：

- 不带身份验证——任何人都可以连接并使用该服务器（无需登录）。
- 带身份验证和授权——用户需要先登录才能访问工具，并且你可以根据用户的权限控制 AI 智能体可以调用哪些工具。

## 选择方案

Agents SDK 提供了多种创建 MCP 服务器的方式。请选择适合你用例的方案：

| 方案 | 有状态？ | 需要 Durable Objects？ | 最适合 |
| --- | --- | --- | --- |
| [createMcpHandler()](https://developers.cloudflare.com/agents/api-reference/mcp-handler-api/) | 否 | 否 | 无状态工具，最简单的设置 |
| [McpAgent](https://developers.cloudflare.com/agents/api-reference/mcp-agent-api/) | 是 | 是 | 有状态工具、按会话状态、引导（elicitation） |
| 原始 `WebStandardStreamableHTTPServerTransport` | 否 | 否 | 完全控制，无 SDK 依赖 |

- createMcpHandler() 是让无状态 MCP 服务器尽快运行起来的最快方式。当你的工具不需要按会话保存状态时，可以使用它。
- McpAgent 为每个会话提供一个 Durable Object，具备内置的状态管理、对引导（elicitation）的支持，以及 SSE 和 Streamable HTTP 两种传输方式。
- 如果你想直接使用 @modelcontextprotocol/sdk 而不借助 Agents SDK 的辅助工具，原始传输方式能给你完全的控制权。

## 部署你的第一个 MCP 服务器

你可以先部署一个不带身份验证的[公共 MCP 服务器 ↗](https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)，之后再添加用户身份验证和范围限定的授权。如果你已经知道你的服务器需要身份验证，可以直接跳到[下一节](https://developers.cloudflare.com/agents/guides/remote-mcp-server/#add-authentication)。

### 通过控制台（dashboard）

下面的按钮将引导你完成将[示例 MCP 服务器 ↗](https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)部署到 Cloudflare 账户所需的全部操作：

一旦部署完成，该服务器将在你的 `workers.dev` 子域名上上线（例如 `remote-mcp-server-authless.your-account.workers.dev/mcp`）。你可以立即使用 [AI Playground ↗](https://playground.ai.cloudflare.com/)（一个远程 MCP 客户端）、[MCP inspector ↗](https://github.com/modelcontextprotocol/inspector) 或[其他 MCP 客户端](https://developers.cloudflare.com/agents/guides/remote-mcp-server/#connect-from-an-mcp-client-via-a-local-proxy)连接它。

系统会在你的 GitHub 或 GitLab 账户上为你的 MCP 服务器创建一个新的 git 代码仓库，并将其配置为每当你推送改动或将拉取请求合并到仓库主分支时自动部署到 Cloudflare。你可以克隆这个代码仓库，进行[本地开发](https://developers.cloudflare.com/agents/guides/remote-mcp-server/#via-the-cli)，并开始用你自己的[工具](https://developers.cloudflare.com/agents/model-context-protocol/tools/)定制这个 MCP 服务器。

### 通过命令行界面（CLI）

你可以使用 [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler) 在本地机器上创建一个新的 MCP 服务器，并将其部署到 Cloudflare。

- 打开终端，运行以下命令：

  ```bash
  npm create cloudflare@latest -- remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
  yarn create cloudflare remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
  pnpm create cloudflare@latest remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
  ```

  在设置过程中，选择以下选项：
  - 对于 "Do you want to add an AGENTS.md file to help AI coding tools understand Cloudflare APIs?"，选择 **No**。
  - 对于 "Do you want to use git for version control?"，选择 **No**。
  - 对于 "Do you want to deploy your application?"，选择 **No**（我们将在部署前先测试服务器）。

  现在，MCP 服务器已经设置完成，依赖项也已安装。

- 进入项目文件夹：

  ```bash
  cd remote-mcp-server-authless
  ```

- 在新项目的目录中，运行以下命令启动开发服务器：

  ```bash
  npm start
  ```

  ```
  ⎔ Starting local server...
  [wrangler:info] Ready on http://localhost:8788
  ```

  查看命令输出中的本地端口。在本例中，MCP 服务器运行在端口 8788 上，MCP 端点 URL 是 http://localhost:8788/mcp。

- 要在本地测试服务器：在一个新终端中，运行 [MCP inspector ↗](https://github.com/modelcontextprotocol/inspector)。MCP inspector 是一个交互式 MCP 客户端，可让你从 web 浏览器连接到你的 MCP 服务器并调用工具：

  ```bash
  npx @modelcontextprotocol/inspector@latest
  ```

  ```
  🚀 MCP Inspector is up and running at: http://localhost:5173/?MCP_PROXY_AUTH_TOKEN=46ab..cd3
  🌐 Opening browser...
  ```

  MCP Inspector 将在你的 web 浏览器中启动。你也可以通过打开浏览器并访问 http://localhost:<PORT> 来手动启动它。查看命令输出中 MCP Inspector 所在的本地端口。在本例中，MCP Inspector 运行在端口 5173 上。在 MCP inspector 中，输入你的 MCP 服务器的 URL（http://localhost:8788/mcp），然后选择 Connect。选择 List Tools 以显示你的 MCP 服务器所暴露的工具。

- 你现在可以将 MCP 服务器部署到 Cloudflare。在项目目录中运行：

  ```bash
  npx wrangler@latest deploy
  ```

  如果你已经通过 git 代码仓库将 MCP 服务器连接到该 Worker，那么只需推送改动或将拉取请求合并到仓库主分支，即可部署你的 MCP 服务器。MCP 服务器将被部署到你的 `*.workers.dev` 子域名，地址为 https://remote-mcp-server-authless.your-account.workers.dev/mcp。

- 要测试远程 MCP 服务器，取你已部署 MCP 服务器的 URL（https://remote-mcp-server-authless.your-account.workers.dev/mcp），并将其输入运行在 http://localhost:5173 上的 MCP inspector。

现在你有了一个可供 MCP 客户端连接的远程 MCP 服务器。

## 通过本地代理从 MCP 客户端连接

现在你的远程 MCP 服务器已经运行起来了，你可以使用 [mcp-remote 本地代理 ↗](https://www.npmjs.com/package/mcp-remote) 将 Claude Desktop 或其他 MCP 客户端连接到它——即使你的 MCP 客户端本身不支持远程传输或授权也能做到。这让你能够用真实的 MCP 客户端测试与远程 MCP 服务器的交互效果。

例如，要从 Claude Desktop 连接：

- 更新你的 Claude Desktop 配置，使其指向你的 MCP 服务器 URL：

  ```json
  {
    "mcpServers": {
      "math": {
        "command": "npx",
        "args": ["mcp-remote", "https://remote-mcp-server-authless.your-account.workers.dev/mcp"]
      }
    }
  }
  ```

- 重启 Claude Desktop 以加载 MCP 服务器。完成后，Claude 就能调用你的远程 MCP 服务器了。

- 要进行测试，让 Claude 使用你的某个工具。例如：你能用 math 工具把 23 和 19 相加吗？Claude 应该会调用该工具，并显示由远程 MCP 服务器生成的结果。

要了解如何与其他 MCP 客户端一起使用远程 MCP 服务器，请参阅[测试远程 MCP 服务器](https://developers.cloudflare.com/agents/guides/test-remote-mcp-server)。

## 添加身份验证

你之前部署的公共 MCP 服务器示例允许任何客户端无需登录即可连接并调用工具。要为你的 MCP 服务器添加用户身份验证，你可以集成 Cloudflare Access 或第三方服务作为 OAuth 提供方。你的 MCP 服务器负责处理安全的登录流程，并签发访问令牌（access token），MCP 客户端可用这些令牌发起经过身份验证的工具调用。用户通过 OAuth 提供方登录，并以范围限定的权限授予其 AI 智能体与使用你的 MCP 服务器所暴露工具进行交互的许可。

### Cloudflare Access OAuth

你可以将 MCP 服务器配置为要求通过 Cloudflare Access 进行用户身份验证。Cloudflare Access 充当身份聚合器，验证用户的电子邮件、来自你现有[身份提供方](https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/)（如 GitHub 或 Google）的信号，以及 IP 地址或设备证书等其他属性。当用户连接到 MCP 服务器时，系统会提示他们登录所配置的身份提供方，只有通过你的[访问策略](https://developers.cloudflare.com/cloudflare-one/access-controls/policies/#selectors)后才能获得访问权限。

有关分步部署指南，请参阅[使用 Access for SaaS 保护 MCP 服务器](https://developers.cloudflare.com/cloudflare-one/access-controls/ai-controls/saas-mcp/)。

### 第三方 OAuth

你可以将 MCP 服务器与任何支持 OAuth 2.0 规范的 [OAuth 提供方](https://developers.cloudflare.com/agents/model-context-protocol/authorization/#2-third-party-oauth-provider)连接，包括 GitHub、Google、Slack、[Stytch](https://developers.cloudflare.com/agents/model-context-protocol/authorization/#stytch)、[Auth0](https://developers.cloudflare.com/agents/model-context-protocol/authorization/#auth0)、[WorkOS](https://developers.cloudflare.com/agents/model-context-protocol/authorization/#workos) 等等。

以下示例演示如何使用 GitHub 作为 OAuth 提供方。

#### 第 1 步 —— 创建新的 MCP 服务器

运行以下命令，创建一个使用 GitHub OAuth 的新 MCP 服务器：

```bash
npm create cloudflare@latest -- my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

```bash
yarn create cloudflare my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

```bash
pnpm create cloudflare@latest my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

现在，MCP 服务器已经设置完成，依赖项也已安装。进入该项目文件夹：

终端窗口

```bash
cd my-mcp-server-github-auth
```

你会注意到，在这个示例 MCP 服务器中，如果你打开 `src/index.ts`，主要区别在于 `defaultHandler` 被设置为了 `GitHubHandler`：

TypeScript

```typescript
import GitHubHandler from "./github-handler";
export default new OAuthProvider({  apiRoute: "/mcp",  apiHandler: MyMCP.serve("/mcp"),  defaultHandler: GitHubHandler,  authorizeEndpoint: "/authorize",  tokenEndpoint: "/token",  clientRegistrationEndpoint: "/register",});
```

这确保你的用户被重定向到 GitHub 进行身份验证。不过，要让它真正工作，你需要按下面的步骤创建 OAuth 客户端应用。

#### 第 2 步 —— 创建 OAuth 应用

要将 GitHub 用作你的 MCP 服务器的身份验证提供方，你需要创建两个 [GitHub OAuth 应用 ↗](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app) —— 一个用于本地开发，一个用于生产环境。

#### 第 2.1 步 —— 为本地开发创建新的 OAuth 应用

- 前往 [github.com/settings/developers ↗](https://github.com/settings/developers) 创建一个新的 OAuth 应用，使用以下设置：
  - Application name（应用名称）：My MCP Server (local)
  - Homepage URL（主页 URL）：http://localhost:8788
  - Authorization callback URL（授权回调 URL）：http://localhost:8788/callback

- 对于刚创建的 OAuth 应用，将该应用的客户端 ID 添加为 GITHUB_CLIENT_ID，并生成一个客户端密钥，将其作为 GITHUB_CLIENT_SECRET 添加到项目根目录下的 .env 文件中，该文件将用于在本地开发中设置密钥：

  终端窗口

  ```bash
  touch .env
  echo 'GITHUB_CLIENT_ID="your-client-id"' >> .env
  echo 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .env
  cat .env
  ```

- 运行以下命令启动开发服务器：

  终端窗口

  ```bash
  npm start
  ```

  你的 MCP 服务器现在运行在 http://localhost:8788/mcp 上。

- 在一个新终端中，运行 [MCP inspector ↗](https://github.com/modelcontextprotocol/inspector)。MCP inspector 是一个交互式 MCP 客户端，可让你从 web 浏览器连接到你的 MCP 服务器并调用工具：

  终端窗口

  ```bash
  npx @modelcontextprotocol/inspector@latest
  ```

- 在 web 浏览器中打开 MCP inspector：

  终端窗口

  ```bash
  open http://localhost:5173
  ```

- 在 inspector 中，输入你的 MCP 服务器的 URL：http://localhost:8788/mcp

- 在右侧的主面板中，点击 OAuth Settings 按钮，然后点击 Quick OAuth Flow。你应该会被重定向到 GitHub 的登录或授权页面。在授权 MCP 客户端（inspector）访问你的 GitHub 账户后，你会被重定向回 inspector。

- 点击侧边栏中的 Connect，你应该会看到 "List Tools" 按钮，它会列出你的 MCP 服务器所暴露的工具。

#### 第 2.2 步 —— 为生产环境创建新的 OAuth 应用

你需要重复第 2.1 步，为生产环境创建一个新的 OAuth 应用。

- 前往 [github.com/settings/developers ↗](https://github.com/settings/developers) 创建一个新的 OAuth 应用，使用以下设置：

  - Application name（应用名称）：My MCP Server (production)
  - Homepage URL（主页 URL）：输入你已部署 MCP 服务器的 workers.dev URL（例如 worker-name.account-name.workers.dev）
  - Authorization callback URL（授权回调 URL）：输入你已部署 MCP 服务器 workers.dev URL 的 /callback 路径（例如 worker-name.account-name.workers.dev/callback）

- 对于刚创建的 OAuth 应用，使用 Wrangler CLI 添加客户端 ID 和客户端密钥：

  终端窗口

  ```bash
  npx wrangler secret put GITHUB_CLIENT_ID
  ```

  终端窗口

  ```bash
  npx wrangler secret put GITHUB_CLIENT_SECRET
  ```

  ```bash
  npx wrangler secret put COOKIE_ENCRYPTION_KEY # add any random string here e.g. openssl rand -hex 32
  ```

- 设置 KV 命名空间：
  a. 创建 KV 命名空间：

  终端窗口

  ```bash
  npx wrangler kv namespace create "OAUTH_KV"
  ```

  b. 用得到的 KV ID 更新 wrangler.jsonc 文件：

  ```json
  {
    "kvNamespaces": [
      {
        "binding": "OAUTH_KV",
        "id": "<YOUR_KV_NAMESPACE_ID>"
      }
    ]
  }
  ```

- 将 MCP 服务器部署到你的 Cloudflare workers.dev 域名：

  终端窗口

  ```bash
  npm run deploy
  ```

- 使用 [AI Playground ↗](https://playground.ai.cloudflare.com/)、MCP Inspector 或[其他 MCP 客户端](https://developers.cloudflare.com/agents/guides/remote-mcp-server/#connect-from-an-mcp-client-via-a-local-proxy)连接到运行在 worker-name.account-name.workers.dev/mcp 的服务器，并通过 GitHub 进行身份验证。

## 后续步骤

[MCP 工具](https://developers.cloudflare.com/agents/model-context-protocol/tools/) 为你的 MCP 服务器添加工具。

[授权](https://developers.cloudflare.com/agents/model-context-protocol/authorization/) 定制身份验证与授权。
