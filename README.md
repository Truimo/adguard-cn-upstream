# adguard-cn-upstream

adguard cn upstream dns file.

adguard 指定某些域名使用特定上游，进行 dns 分流或 cn 加速互联网访问。

规则来自 [felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list) 仓库

## 规则文件

```md
https://raw.githubusercontent.com/Truimo/adguard-cn-upstream/sync/upstream_dns_file.conf
#
https://cdn.jsdelivr.net/gh/Truimo/adguard-cn-upstream@sync/upstream_dns_file.conf
```

## AdGuardHome 使用方法

下载 `upstream_dns_file.conf` 到本地，编辑 `AdGuardHome.yaml` 文件，找到 `upstream_dns_file: ""`，填入 `upstream_dns_file.conf` 所在路径，保存即可。

```yaml
dns:
  upstream_dns_file: /path/upstream_dns_file.conf
```

> 修改 AdGuardHome 配置时，先 `./AdGuardHome -s stop` 停止运行，修改并保存配置文件后，运行 `./AdGuardHome -s start` 重新运行 AdGuardHome 。
