# MCP 社区生态资源汇总整理
## 一、三大核心资源仓库
### 1. Awesome MCP Servers
地址：https://github.com/punkpeye/awesome-mcp-servers
- 社区维护的MCP服务合集清单
- 汇聚各类第三方MCP服务实现
- 按功能分类排版，检索便捷

### 2. MCP Servers Website
地址：https://mcpservers.org/
- MCP官方服务目录站点
- 支持关键词搜索、条件筛选
- 附带每个服务的部署教程、调用示例

### 3. Official MCP Servers（Anthropic官方）
地址：https://github.com/modelcontextprotocol/servers
- Anthropic官方出品MCP服务
- 稳定性最强、文档完善、长期维护
- 覆盖高频刚需基础能力

## 二、官方内置MCP服务（表10.5）
| 服务名称 | 核心能力 | NPM包路径 | 典型使用场景 |
| ---- | ---- | ---- | ---- |
| filesystem | 本地文件系统读写 | @modelcontextprotocol/server-filesystem | 文件读写、目录遍历、本地文档处理 |
| github | GitHub平台API对接 | @modelcontextprotocol/server-github | 仓库检索、代码读取、Issue操作 |
| postgres | PostgreSQL数据库操作 | @modelcontextprotocol/server-postgres | SQL查询、业务数据库数据分析 |
| sqlite | SQLite轻量数据库 | @modelcontextprotocol/server-sqlite | 小型本地数据库读写、轻量化数据存储 |
| slack | Slack消息交互 | @modelcontextprotocol/server-slack | 频道消息发送、历史消息读取 |
| google-drive | 谷歌云盘文件访问 | @modelcontextprotocol/server-google-drive | 云端文件读取、网盘内容解析 |
| brave-search | 网页实时搜索 | @modelcontextprotocol/server-brave-search | 联网实时资讯、外部资料检索 |
| fetch | 网页内容抓取解析 | @modelcontextprotocol/server-fetch | 网页正文提取、静态页面数据爬取 |

## 三、社区热门MCP服务（表10.6）
| 服务名称 | 功能定位 | 仓库/NPM标识 | 核心亮点 |
| ---- | ---- | ---- | ---- |
| Playwright | 浏览器自动化 | @playwright/mcp | 网页自动化操作、页面截图、表单自动填充 |
| Puppeteer | Chrome浏览器控制 | mcp-server-puppeteer | 爬虫、网页PDF导出、前端页面渲染 |
| Screenpipe | 屏幕录制捕获 | mediar-ai/screenpipe | 电脑屏幕/音频录制、画面检索、时间轴定位 |
| Obsidian | Obsidian知识库对接 | calclavia/mcp-obsidian | Markdown笔记读取、知识库全文检索 |
| Notion | Notion协作文档 | Badhansen/notion-mcp | 文档编辑、待办管理、Notion数据表操作 |
| Jira | 项目工单管理 | nguyenvanduocit/jira-mcp | 迭代规划、工单创建、项目流程管控 |
| Tavily | AI专业搜索 | kshern/mcp-tavily | 面向大模型优化的精准检索、事实查证 |
| YouTube | YouTube视频解析 | anaisbetts/mcp-youtube | 视频字幕提取、视频摘要、元数据获取 |
| Spotify | 音乐播放器控制 | marcelmarais/Spotify | 播放切歌、歌单管理、音乐控制 |
| Wolfram Alpha | 科学计算引擎 | ricocf/mcp-wolframalpha | 高数运算、专业科学计算、实时数理知识 |
| Sentry | 程序异常监控 | getsentry/sentry-mcp | 后端报错查看、性能异常定位、故障排查 |
| Grafana | 运维可视化看板 | grafana/mcp-grafana | 监控面板查询、时序指标、运维数据分析 |

## 四、生态使用总结
1. **快速选型建议**
- 基础刚需能力（文件、数据库、联网、Git）：直接用**Official官方MCP服务**，稳定无坑；
- 小众工具、办公软件、浏览器自动化、第三方平台对接：去`awesome-mcp-servers`社区库查找现成实现。
2. **落地价值**
无需从零开发工具对接逻辑，直接通过MCP启动命令一键接入上述全部能力，适配HelloAgents、Cursor、Claude Desktop等所有支持MCP的Agent框架。