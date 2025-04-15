#!/usr/bin/env python3

import re
import time

import requests

conf_urls = [
    'https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf',
    'https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/apple.china.conf'
]
domestic_url = 'https://ruleset.skk.moe/List/non_ip/domestic.conf'

default_dns = [
    'quic://dns.nextdns.io',
    'tls://dns.nextdns.io',
]
cn_dns = 'tls://dns.alidns.com quic://dns.alidns.com https://dns.alidns.com/dns-query tls://dot.pub https://doh.pub/dns-query'
conf_file = 'domains.china.conf'
save_file = 'upstream_dns_file.conf'

if __name__ == '__main__':
    new_time = time.ctime()
    rules = set()
    line = [
        '# https://github.com/Truimo/adguard-cn-upstream',
        f'# update @ {new_time}',
        '# default dns',
        *default_dns,
        '# cn suffix (on demand)',
        f'# [/cn/]{cn_dns}',
        '# cn domains',
    ]

    # felixonmars/dnsmasq-china-list
    for conf in conf_urls:
        r = requests.get(conf)
        with open(conf_file, 'wb') as f:
            f.write(r.content)

        with open(conf_file, 'r') as f:
            for it in f.readlines():
                if it[0] == '#':
                    continue
                rule = re.sub(r'^server=/(\S+)/[\s\S]+', rf'[/\1/]{cn_dns}', it)
                rules.add(rule)

    # ruleset.skk.moe
    r = requests.get(domestic_url)
    with open(conf_file, 'wb') as f:
        f.write(r.content)

    with open(conf_file, 'r') as f:
        for it in f.readlines():
            if it[0] == '#':
                continue
            if '.' not in it:
                continue
            if it.endswith('.ruleset.skk.moe\n'):
                continue
            if it.startswith('DOMAIN-SUFFIX,'):
                rule = re.sub(r'^DOMAIN-SUFFIX,(\S+)\n', rf'[/\1/]{cn_dns}', it)
                rules.add(rule)
                continue
            if it.startswith('DOMAIN,'):
                rule = f'[/{it[7:-1]}/]{cn_dns}'
                rules.add(rule)

    rules = list(rules)
    rules.sort()
    out_line = [*line, *rules]

    with open(save_file, 'w') as f:
        for it in out_line:
            f.write(it)
            f.write('\n')

    print('done.')
