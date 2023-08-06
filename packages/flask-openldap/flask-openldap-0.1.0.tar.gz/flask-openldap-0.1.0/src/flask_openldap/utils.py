#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import hashlib
import base64
import random
import string


def create_random_string(chars=string.ascii_letters + string.digits, length=16):
    """Generate a random salt. Default length is 16.
       Originated from mkpasswd in Luma
    """
    return "".join([random.choice(chars) for _ in range(int(length))])


def to_hash(password):
    """Hash password using MD5SUM"""
    return "{MD5}%s" % base64.encodebytes(
        hashlib.md5(str(password).encode()).digest()
    ).strip().decode()
