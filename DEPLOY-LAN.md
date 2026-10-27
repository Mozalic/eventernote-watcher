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

也可以在「出演者 → 从用户关注导入艺人」输入 Eventernote 用户名或个人主页链接，
直接追加该用户公开收藏的声优／艺人。重复导入会跳过已有艺人，保留暂停状态、
活动和抓取记录。该操作是一次性导入，关注列表变化后可再次导入；不会删除已有艺人。
导入完成后点击「立即抓取」获取活动。不需要提供 Eventernote 登录密码。

打开页面默认进入「活动日历」，可按月份浏览已抓取的活动，点击日期查看当天详情。
支持出演者筛选、只看未来、今天和最近活动跳转，以及月历／列表切换；共同出演的
同一活动合并显示。日期未定的活动可通过单独入口查看。
月历活动块直接显示艺人名字，并按艺人分配颜色；同场多人分别显示彩色名字，
当天详情和列表使用相同配色，切换月份或筛选不会改变颜色。
日历只使用已有抓取数据，切换月份不会重新请求 Eventernote；点击「刷新活动」可读取最新缓存。

日历订阅位于 `/api/calendar.ics`，「活动日历 → 外部日历订阅」可复制链接。局域网地址可供
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
