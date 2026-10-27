# Docker 局域网试用

需要 Docker Compose v2。在独立目录克隆本仓库，复制 `.env.lan.example` 为 `.env`，
将 `BIND_ADDRESS` 改为服务器的局域网 IP。`WEB_PORT` 默认是 `18080`，使用前确认未被占用。

```sh
docker compose -p eventernote-watcher -f compose.lan.yml up -d --build
docker compose -p eventernote-watcher -f compose.lan.yml ps
```

访问 `http://服务器局域网IP:18080/`。在「出演者」中添加想跟踪的艺人，
然后点击「立即抓取」。首次抓取建立基线，通知渠道默认关闭。
当前 WebUI 初次启动为空名单，不会读取仓库的 `actors.json`。

日历订阅位于 `/api/calendar.ics`，「活动」页可复制链接。局域网地址可供
能访问该网络的本机日历客户端订阅；Google Calendar 服务器无法读取内网地址。

数据保存在部署目录的 `data/`，更新或重建容器时保留。查看日志：

```sh
docker compose -p eventernote-watcher -f compose.lan.yml logs --tail=100
```

更新前备份数据，再运行：

```sh
git pull --ff-only
docker compose -p eventernote-watcher -f compose.lan.yml up -d --build
```

停止试用实例（保留数据）：

```sh
docker compose -p eventernote-watcher -f compose.lan.yml down
```

该配置只发布到指定的服务器地址，不配置公网代理或端口转发。
如需公网访问，先设置 `.env` 的 `AUTH_PASSWORD` 和 `ICS_TOKEN`，并配置 HTTPS。
