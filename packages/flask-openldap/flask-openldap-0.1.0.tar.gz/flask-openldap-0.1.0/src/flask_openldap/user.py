#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""


class LDAPUser(object):
    """A LDAP user
    """

    def __init__(self, path, **kwargs):
        """docstring for __init__"""
        self._ldap_path = path
        for key, values in kwargs.items():
            if len(values) > 1:
                setattr(self, key, [x.decode('UTF-8') for x in values])
            else:
                setattr(self, key, values[0].decode('UTF-8'))
