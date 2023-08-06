#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, CESNET, z. s. p. o.
# Use of this source is governed by an ISC license, see LICENSE file.

__version__ = '0.1.9'
__author__ = 'Pavel Kácha <pavel.kacha@cesnet.cz>'

import socket
import struct
import numbers
import sys

try:
    basestring
except NameError:
    basestring = str

class Range(object):
    __slots__ = ()

    single = int

    def __len__(self):
        return self.high() - self.low() + 1

    def __eq__(self, other):
        return (self.low() == other.low() and self.high() == other.high())

    def __ne__(self, other):
        return not self.__eq__(other)

    def __contains__(self, other):
        return (self.low() <= other.low() and self.high() >= other.high())

    def __iter__(self):
        for i in range(self.low(), self.high()+1):
            yield self.util.single(i)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return (self.util.single(self.low() + i) for i in range(*key.indices(len(self))))
        else:
            if key < 0:
                idx = self.high() + key + 1
            else:
                idx = self.low() + key
            if self.low() <= idx <= self.high():
                return self.util.single(idx)
            else:
                raise IndexError

    def __repr__(self):
        return "%s('%s')" % (type(self).__name__, str(self))


class IPBase(Range):
    __slots__ = ()

    def __init__(self, s):
        if isinstance(s, basestring):
            rng = self._from_str(s)
        elif isinstance(s, IPBase):
            rng = self._from_range(s)
        else:
            rng = self._from_val(s)
        self._assign(rng)

    def cidr_split(self):
        lo, hi = self.low(), self.high()
        lo, hi = min(lo, hi), max(lo, hi)
        while lo<=hi:
            lower_bits = (~lo & (lo-1)).bit_length()
            size = hi - lo + 1
            size_bits = size.bit_length() - 1
            bits = min(lower_bits, size_bits)
            yield self.util.net((lo, self.util.bit_length-bits))
            lo += 1 << bits

    def _from_val(self, v):
        try:
            a, b = v
            return int(a), int(b)
        except Exception:
            raise ValueError("Two value tuple expected, got %s" % v)


class IPRangeBase(IPBase):
    __slots__ = ("lo", "hi")

    def _from_range(self, r):
        return (r.low(), r.high())

    def _from_str(self, s):
        try:
            ip1, ip2 = s.split("-")
            return (self.util.from_str(ip1), self.util.from_str(ip2))
        except Exception:
            raise ValueError("Wrong range format: %s" % s)

    def _assign(self, v):
        self.lo = min(v)
        self.hi = max(v)

    def low(self): return self.lo

    def high(self): return self.hi

    def __str__(self):
        return "%s-%s" % (self.util.to_str(self.lo), self.util.to_str(self.hi))


class IPNetBase(IPBase):
    __slots__ = ("base", "cidr", "mask")

    def _from_range(self, r):
        lo = r.low()
        mask = len(r) - 1
        if (len(r) & mask) or (lo & mask):
            raise ValueError("%s is not a proper network prefix" % r)
        return lo, self.util.bit_length - mask.bit_length()

    def _from_str(self, s):
        try:
            net, cidr = s.split("/")
            base = self.util.from_str(net)
            cidr = int(cidr)
            return base, cidr
        except Exception:
            raise ValueError("Wrong network format: %s" % s)

    def _assign(self, v):
        self.base, self.cidr = v
        self.mask = (self.util.full_mask << (self.util.bit_length - self.cidr)) & self.util.full_mask

    def low(self): return self.base & self.mask

    def high(self): return self.base | (self.mask ^ self.util.full_mask)

    def __str__(self):
        return "%s/%i" % (self.util.to_str(self.base), self.cidr)


class IPAddrBase(IPBase):
    __slots__ = ("ip")

    def _from_range(self, r):
        if len(r)!=1:
            raise ValueError("Unable to convert network %s to one ip address" % r)
        return r.low()

    def _from_str(self, s): return self.util.from_str(s)

    def _from_val(self, r):
        try:
            return int(r)
        except Exception:
            raise ValueError("Integer expected as IP")

    def _assign(self, v): self.ip = v

    def __str__(self): return self.util.to_str(self.ip)

    def __int__(self): return self.ip

    def low(self): return self.ip

    def high(self): return self.ip


class IP4Util(object):
    __slots__ = ()

    bit_length = 32
    full_mask = 2**bit_length-1

    @staticmethod
    def from_str(s):
        try:
            return struct.unpack("!L", socket.inet_pton(socket.AF_INET, s))[0]
        except Exception:
            raise ValueError("Wrong IPv4 address format: %s" % s)

    @staticmethod
    def to_str(i):
        try:
            return socket.inet_ntop(socket.AF_INET, struct.pack('!L', i))
        except Exception:
            raise ValueError("Unable to convert to IPv6 address: %s" % i)


class IP6Util(object):
    __slots__ = ()

    bit_length = 128
    full_mask = 2**bit_length-1

    @staticmethod
    def from_str(s):
        try:
            hi, lo = struct.unpack("!QQ", socket.inet_pton(socket.AF_INET6, s))
            return hi << 64 | lo
        except Exception:
            raise ValueError("Wrong IPv6 address format: %s" % s)

    @staticmethod
    def to_str(i):
        try:
            hi = i >> 64
            lo = i & 0xFFFFFFFFFFFFFFFF
            return socket.inet_ntop(socket.AF_INET6, struct.pack('!QQ', hi, lo))
        except Exception:
            raise ValueError("Unable to convert to IPv6 address: %s" % i)


class IP4(IPAddrBase):
    __slots__ = ()
    util = IP4Util

    if sys.version_info < (3,):
        def to_ptr_str(self):
            return ".".join(str(ord(s)) for s in (reversed(struct.pack("!L", self.ip)))) + ".in-addr.arpa."
    else:
        def to_ptr_str(self):
            return ".".join(str(s) for s in self.ip.to_bytes(4, "little")) + ".in-addr.arpa."


class IP6(IPAddrBase):
    __slots__ = ()
    util = IP6Util

    def to_ptr_str(self):
        return ".".join(reversed("%016x" % self.ip)) + ".ip6.arpa."


class IP4Range(IPRangeBase):
    __slots__ = ()
    util = IP4Util

class IP6Range(IPRangeBase):
    __slots__ = ()
    util = IP6Util

class IP4Net(IPNetBase):
    __slots__ = ()
    util = IP4Util

class IP6Net(IPNetBase):
    __slots__ = ()
    util = IP6Util

IP4Util.single = IP4
IP6Util.single = IP6
IP4Util.net = IP4Net
IP6Util.net = IP6Net

def from_str(s):
    for t in IP4Net, IP4Range, IP4, IP6Net, IP6Range, IP6:
        try:
            return t(s)
        except ValueError:
            pass
    raise ValueError("%s does not appear as IP address, network or range string" % s)

def from_str_v4(s):
    for t in IP4Net, IP4Range, IP4:
        try:
            return t(s)
        except ValueError:
            pass
    raise ValueError("%s does not appear as IPv4 address, network or range string" % s)

def from_str_v6(s):
    for t in IP6Net, IP6Range, IP6:
        try:
            return t(s)
        except ValueError:
            pass
    raise ValueError("%s does not appear as IPv6 address, network or range string" % s)
