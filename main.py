#!/usr/bin/env python3

import re
import time

import requests

conf_url = 'https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf'

default_dns = [
    'https://dns.20mo.cn/dns-query'
]
cn_dns = 'quic://dns.alidns.com tls://dns.alidns.com'
conf_file = 'accelerated-domains.china.conf'
save_file = 'upstream_dns_file.conf'

if __name__ == '__main__':
    new_time = time.ctime()
    rules = set()
    line = [
        '# https://github.com/Truimo/adguard-cn-upstream',
        f'# update @ {new_time}',
        '# default dns',
        *default_dns,
        '# all cn',
        f'[/cn/]{cn_dns}',
        '# cn domains',
    ]

    r = requests.get(conf_url)
    with open(conf_file, 'wb') as f:
        f.write(r.content)

    with open(conf_file, 'r') as f:
        for it in f.readlines():
            if it[0] == '#':
                continue
            rule = re.sub(r'^server=/(\S+)/[\s\S]+', rf'[/\1/]{cn_dns}', it)
            rules.add(rule)

    rules = list(rules)
    rules.sort()
    out_line = [*line, *rules]

    with open(save_file, 'w') as f:
        for it in out_line:
            f.write(it)
            f.write('\n')

    print('done.')
