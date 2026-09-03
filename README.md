<div align="center">
  <img src="./assets/hero.svg?v=20260903-2" width="100%" alt="Ranavar — backend systems, developer tools and MCP infrastructure" />
  <br /><br />
  <a href="https://github.com/NikitaRTN/mcp-stack/actions/workflows/test.yml"><img alt="MCP Hub tests" src="https://img.shields.io/github/actions/workflow/status/NikitaRTN/mcp-stack/test.yml?branch=main&style=flat-square&label=tests&labelColor=0E1628&color=4FE1E8" /></a>
  <a href="https://github.com/NikitaRTN/NikitaRTN/actions/workflows/live-profile.yml"><img alt="Live GitHub signal" src="https://img.shields.io/github/actions/workflow/status/NikitaRTN/NikitaRTN/live-profile.yml?branch=main&style=flat-square&label=live%20telemetry&labelColor=0E1628&color=806CFF" /></a>
  <a href="https://github.com/NikitaRTN/mcp-stack/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/github/license/NikitaRTN/mcp-stack?style=flat-square&labelColor=0E1628&color=806CFF" /></a>
</div>

## `01 / CURRENT BUILD`

### [MCP Hub 3](https://github.com/NikitaRTN/mcp-stack) — control plane для MCP-сервисов

Self-hosted рабочее пространство для запуска, публикации и наблюдения за локальными и удалёнными MCP-серверами.

- единая HTTPS-точка входа через Caddy;
- MCP Studio и Tools Explorer без отдельного frontend build step;
- Token, OAuth introspection и OAuth Client Credentials;
- потоковый JSON-RPC, SSE-события и журнал вызовов в SQLite/WAL;
- backend на стандартной библиотеке Python, тесты на Windows и Linux.

<div align="center">
  <a href="https://github.com/NikitaRTN/mcp-stack"><b>Открыть исходный код →</b></a>
</div>

<br />
<img src="./assets/project-map.svg?v=20260903-2" width="100%" alt="Архитектура MCP Hub 3" />

## `02 / LIVE SIGNAL`

<img src="./assets/live-stats.svg" width="100%" alt="Live GitHub API statistics for NikitaRTN" />

<sub>Карточка генерируется из GitHub REST + GraphQL API каждые 6 часов. Heatmap, вклад, коммиты, репозитории, звёзды и подписчики не редактируются вручную.</sub>

## `03 / SELECTED WORK`

| Проект | Роль | Проверяемый фокус |
|:--|:--|:--|
| **[mcp-stack](https://github.com/NikitaRTN/mcp-stack)** | Автор | Python backend, JS UI, OAuth, SSE, SQLite, GitHub Actions |
| **[SkHttp-Rework](https://github.com/RiseShieldDev/SkHttp-Rework)** | Администратор и разработчик | Java-аддон для HTTP/HTTPS в Minecraft Skript |
| **[SkriptWebAPI](https://github.com/RiseShieldDev/SkriptWebAPI)** | Администратор и контрибьютор | Java API и интеграции для Skript |

## `04 / ENGINEERING PRINCIPLES`

- **Inspectable by default** — запросы, процессы и ошибки должны быть видимы.
- **Secure by default** — закрыто, пока пользователь явно не опубликовал сервис.
- **Dependency-light** — зависимость должна оправдывать своё присутствие.
- **Local-first** — контроль и данные остаются у владельца инфраструктуры.

## `05 / WORKING STACK`

`Python` · `JavaScript` · `Java` · `GitHub Actions` · `HTTP/2` · `SSE` · `OAuth` · `SQLite/WAL`

---

<div align="center"><sub>Все числа и технические заявления привязаны к открытым репозиториям или GitHub API.</sub></div>
