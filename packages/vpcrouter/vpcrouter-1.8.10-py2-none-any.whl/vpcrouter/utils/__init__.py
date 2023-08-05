"""
Copyright 2017 Pani Networks Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

#
# Utility functions, which are used by different modules.
#

import ipaddress
import netaddr
import Queue

from vpcrouter.errors import ArgsError


def ip_check(ip, netmask_expected=False):
    """
    Sanity check that the specified string is indeed an IP address or mask.

    """
    try:
        if netmask_expected:
            if "/" not in ip:
                raise netaddr.core.AddrFormatError()
            netaddr.IPNetwork(ip)
        else:
            netaddr.IPAddress(ip)
    except netaddr.core.AddrFormatError:
        if netmask_expected:
            raise ArgsError("Not a valid CIDR (%s)" % ip)
        else:
            raise ArgsError("Not a valid IP address (%s)" % ip)
    except Exception as e:
        raise ArgsError("Invalid format: %s" % str(e))


def check_valid_ip_or_cidr(val, return_as_cidr=False):
    """
    Checks that the value is a valid IP address or a valid CIDR.

    Returns the specified value.

    If 'return_as_cidr' is set then the return value will always be in the form
    of a CIDR, even if a plain IP address was specified.

    """
    is_ip = True
    if "/" in val:
        ip_check(val, netmask_expected=True)
        is_ip = False
    else:
        ip_check(val, netmask_expected=False)

    if return_as_cidr and is_ip:
        # Convert a plain IP to a CIDR
        if val == "0.0.0.0":
            # Special case for the default route
            val = "0.0.0.0/0"
        else:
            val = "%s/32" % val

    try:
        ipaddress.IPv4Network(unicode(val))
    except Exception as e:
        raise ArgsError("Not a valid network: %s" % str(e))

    return val


def is_cidr_in_cidr(small_cidr, big_cidr):
    """
    Return True if the small CIDR is contained in the big CIDR.

    """
    # The default route (0.0.0.0/0) is handled differently, since every route
    # would always be contained in there. Instead, only a small CIDR of
    # "0.0.0.0/0" can match against it. Other small CIDRs will always result in
    # 'False' (not contained).
    if small_cidr == "0.0.0.0/0":
        return big_cidr == "0.0.0.0/0"
    else:
        if big_cidr == "0.0.0.0/0":
            return False

    s = ipaddress.IPv4Network(unicode(small_cidr))
    b = ipaddress.IPv4Network(unicode(big_cidr))
    return s.subnet_of(b)


def read_last_msg_from_queue(q):
    """
    Read all messages from a queue and return the last one.

    This is useful in many cases where all messages are always the complete
    state of things. Therefore, intermittent messages can be ignored.

    Doesn't block, returns None if there is no message waiting in the queue.

    """
    msg = None
    while True:
        try:
            # The list of IPs is always a full list.
            msg = q.get_nowait()
            q.task_done()
        except Queue.Empty:
            # No more messages, all done for now
            return msg


def param_extract(args, short_form, long_form, default=None):
    """
    Quick extraction of a parameter from the command line argument list.

    In some cases we need to parse a few arguments before the official
    arg-parser starts.

    Returns parameter value, or None if not present.

    """
    val = default
    for i, a in enumerate(args):
        # Long form may use "--xyz=foo", so need to split on '=', but it
        # doesn't necessarily do that, can also be "--xyz foo".
        elems = a.split("=", 1)
        if elems[0] in [short_form, long_form]:
            # At least make sure that an actual name was specified
            if len(elems) == 1:
                if i + 1 < len(args) and not args[i + 1].startswith("-"):
                    val = args[i + 1]
                else:
                    val = ""  # Invalid value was specified
            else:
                val = elems[1]
            break

    return val
