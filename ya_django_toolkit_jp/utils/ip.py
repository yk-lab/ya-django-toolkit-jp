from __future__ import annotations

from .ipv6 import convert_mixed, explode

IPv4 = 'ipv4'
IPv6 = 'ipv6'


# TODO: 下記モジュールを用いるようにリファクタリングする
# https://docs.python.org/ja/3/library/ipaddress.html
# https://netaddr.readthedocs.io/en/latest/introduction.html


def get_version(ip: str):
    return IPv6 if ':' in ip else IPv4


def is_ipv4(ip: str):
    return get_version(ip) == IPv4


def is_ipv6(ip: str):
    return get_version(ip) == IPv6


def _ip_to_number(ip: str, separator='.', group_size=2 ** 8, base=10) -> int:
    parts = ip.split(separator)
    parts = [int(p, base) for p in reversed(parts)]
    nr = 0
    for i, d in enumerate(parts):
        nr += (group_size ** i) * d
    return nr


def to_number(ip: str):
    return ipv6_to_number(ip) if is_ipv6(ip) else ipv4_to_number(ip)


def ipv4_to_number(ip: str):
    return _ip_to_number(ip)


def ipv6_to_number(ip: str):
    if '.' in ip:
        ip = convert_mixed(ip)
    if '::' in ip:
        ip = explode(ip)
    return _ip_to_number(ip, separator=':', group_size=2 ** 16, base=16)


def to_ip(number: int, version=IPv4):
    if version == IPv6:
        separator = ':'
        parts_count = 8
        parts_length = 16
        fmt = '%x'
    else:
        separator = '.'
        parts_count = 4
        parts_length = 8
        fmt = '%d'
    mask = int('1' * parts_length, 2)
    parts = []
    for i in range(parts_count):
        shifted_number = number >> (parts_length * i)
        parts.append(shifted_number & mask)

    return separator.join(map(lambda i: fmt % i, reversed(parts)))


def cidr_to_range(ip: str, prefix_length: int):
    ip_length = 128 if is_ipv6(ip) else 32
    ip_num = to_number(ip)
    start_mask = 0 if prefix_length == 0\
        else int('1' * prefix_length, 2) << (ip_length - prefix_length)
    end_mask = 0 if ip_length == prefix_length\
        else int('1' * (ip_length - prefix_length), 2)
    start = ip_num & start_mask
    end = start | end_mask
    return (start, end)
