def explode(ip: str):
    if ip.count('::') > 1:
        raise ValueError(
            'Invalid ip address "%s". "::" can appear only once.' % ip)
    pre, post = [[_x for _x in x.split(':') if _x] for x in ip.split('::')]
    return ':'.join(pre + ['0'] * (8 - len(pre) - len(post)) + post)


def convert_mixed(ip: str):
    last_colon = ip.rfind(':')
    ipv6, ipv4 = ip[:last_colon+1], ip[last_colon+1:]
    if ipv4.count('.') != 3:
        raise ValueError(
            'Invalid IPv6 address "%s". Dotted ipv4 part should be at the end.'
            % ip)
    a, b, c, d = ipv4.split('.')
    pre_last = 256 * int(a) + int(b)
    last = 256 * int(c) + int(d)

    return '%s:%x:%x' % (ipv6, pre_last, last)
