#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import string
import ldap
from cdumay_error import InternalError, ValidationError, NotFound

from flask_openldap import MESSAGE_MAP
from random import randint
from flask import current_app
from flask_simpleldap import LDAP
from text_unidecode import unidecode
from flask_openldap.user import LDAPUser
from flask_openldap.utils import create_random_string, to_hash


class LDAPManager(LDAP):
    """LDAPManager"""

    @staticmethod
    def init_app(app):
        app.config.setdefault('LDAP_USER_PREFIX', "")
        app.config.setdefault('LDAP_USER_MAIL', "user@example.com")
        LDAP.init_app(app)

    @staticmethod
    def to_bytes(value):
        return str(value).encode('UTF-8')

    @staticmethod
    def value_to_ldap(value):
        if isinstance(value, (list, tuple)):
            return [LDAPManager.to_bytes(x) for x in value]
        else:
            return [LDAPManager.to_bytes(value)]

    @staticmethod
    def to_ldap(data):
        res = list()
        for key, value in data.items():
            res.append((key, LDAPManager.value_to_ldap(value)))
        return res

    def create_username(self):
        """docstring for create_username"""
        for _ in range(0, 5000):
            username = "{}{}".format(
                current_app.config['LDAP_USER_PREFIX'],
                create_random_string(string.digits, 5)
            )
            if self.exists(uid=username) is False:
                return username
        raise InternalError(
            message=MESSAGE_MAP["FailedToCreateUsername"],
            extra=dict(factory="openldap", msgid="FailedToCreateUsername")
        )

    def get_ids(self):
        """return used uid & gid"""
        users = self.list_user()
        return (
            [int(getattr(x, 'uidNumber')) for x in users],
            [int(getattr(x, 'gidNumber')) for x in users]
        )

    def get_random_ids(self):
        """create random uid & gid for a new user"""
        ids = self.get_ids()
        uids = [x for x in range(15000, 20000) if x not in ids[0]]
        gids = [x for x in range(15000, 20000) if x not in ids[1]]

        return uids[randint(0, len(uids) - 1)], gids[randint(0, len(gids) - 1)]

    # noinspection PyUnresolvedReferences
    def list_user(self):
        """docstring for list_user"""
        conn = self.bind
        try:
            query_filter = "(objectclass=inetOrgPerson)"
            records = conn.search_s(
                current_app.config['LDAP_BASE_DN'], ldap.SCOPE_SUBTREE,
                "(&%s)" % query_filter,
                ['*']
            )
            conn.unbind_s()
            if records:
                return [LDAPUser(x[0], **x[1]) for x in dict(records).items()]
            else:
                return list()

        except ldap.LDAPError as err:
            raise exceptions.ValidationError(
                message=str(getattr(err, 'message', err))
            )
        except Exception as err:
            raise exceptions.ValidationError(message=str(err))

    def exists(self, **kwargs):
        """docstring for exists"""
        try:
            return True if self.get_user(**kwargs) else False
        except ValidationError:
            return False

    # noinspection PyUnresolvedReferences
    def get_user(self, **kwargs):
        """docstring for get_user"""
        conn = self.bind
        try:
            query_filter = "(objectclass=inetOrgPerson)"
            for item in kwargs.items():
                query_filter += "(%s=%s)" % item

            records = conn.search_s(
                current_app.config['LDAP_BASE_DN'], ldap.SCOPE_SUBTREE,
                "(&%s)" % query_filter,
                ['*']
            )
            conn.unbind_s()

            if records:
                return LDAPUser(records[0][0], **records[0][1])

        except ldap.LDAPError as err:
            raise exceptions.ValidationError(
                message=str(getattr(err, 'message', err))
            )
        except Exception as err:
            raise exceptions.ValidationError(message=str(err))

    # noinspection PyUnresolvedReferences
    def add_user(self, username, mail=None, password=None, lastname=None,
                 firstname=None, description=None):
        """docstring for add_user"""
        conn = self.bind
        try:
            if not password:
                password = create_random_string()
            if not mail:
                mail = current_app.config['LDAP_USER_MAIL']

            dn = 'uid=%s,%s' % (username, current_app.config['LDAP_BASE_DN'])
            uid, gid = self.get_random_ids()
            data = dict(
                uid=username,
                objectclass=current_app.config['LDAP_USER_OBJECT_CLASSES'],
                loginShell='/bin/bash',
                userPassword=to_hash(password),
                uidNumber=uid,
                gidNumber=gid,
                mail=mail,
                homeDirectory="/home/%s" % username,
                shadowExpire="-1",
                sn=unidecode(lastname) if lastname else mail,
                givenName=unidecode(firstname) if firstname else username,
                cn=mail
            )
            if description:
                data['description'] = description

            conn.add_s(dn, LDAPManager.to_ldap(data))
            conn.unbind_s()

            return {"email": mail, "password": password, "username": username}
        except (ldap.INVALID_SYNTAX, ldap.OBJECT_CLASS_VIOLATION) as exc:
            raise exceptions.ValidationError(extra=exc.args[0])
        except Exception as err:
            raise exceptions.ValidationError(message=str(err))

    def update_password(self, username, password=None):
        """docstring for update_password"""
        luser = self.get_user(uid=username)
        if luser is None:
            raise NotFound(
                message=MESSAGE_MAP["UserDoesNotExists"], extra=dict(
                    factory="openldap", msgid="UserDoesNotExists",
                    long_message="User '{}' doesn't exists !".format(username)
                )
            )

        if password in (None, ""):
            password = create_random_string()

        res = self.update_attribute(
            username, "userPassword", getattr(luser, 'userPassword', ""),
            to_hash(password)
        )
        return {
            "email": getattr(luser, 'mail', ""),
            "password": res['new'],
            "username": getattr(luser, 'uid', '')
        }

    def update_status(self, username, status):
        """docstring for update_status"""
        luser = self.get_user(uid=username)
        if luser is None:
            raise NotFound(
                message=MESSAGE_MAP["UserDoesNotExists"], extra=dict(
                    factory="openldap", msgid="UserDoesNotExists",
                    long_message="User '{}' doesn't exists !".format(username)
                )
            )

        return self.update_attribute(
            username, "shadowExpire", getattr(luser, 'shadowExpire', "-1"),
            status
        )

    def add_transport(self, username, transport):
        """add_transport"""
        luser = self.get_user(uid=username)
        if luser is None:
            raise NotFound(
                message=MESSAGE_MAP["UserDoesNotExists"], extra=dict(
                    factory="openldap", msgid="UserDoesNotExists",
                    long_message="User '{}' doesn't exists !".format(username)
                )
            )

        if hasattr(luser, 'destinationIndicator'):
            transports = getattr(luser, 'destinationIndicator', list())
            if transport not in transports:
                new_transports = transports + [transport]
            else:
                return {"old": transports, "new": transports}
        else:
            transports = list()
            new_transports = transport

        return self.update_attribute(
            username, 'destinationIndicator', transports, new_transports
        )

    def remove_transport(self, username, transport):
        """remove transport"""
        luser = self.get_user(uid=username)
        if luser is None:
            raise NotFound(
                message=MESSAGE_MAP["UserDoesNotExists"], extra=dict(
                    factory="openldap", msgid="UserDoesNotExists",
                    long_message="User '{}' doesn't exists !".format(username)
                )
            )

        if hasattr(luser, 'destinationIndicator'):
            transports = getattr(luser, 'destinationIndicator', list())
            if isinstance(transports, (str, bytes)):
                transports = [transports]

            if transport in transports:
                new_transports = list(transports)
                new_transports.remove(transport)
            else:
                return {"old": transports, "new": transports}
        else:
            return {"old": list(), "new": list()}

        return self.update_attribute(
            username, 'destinationIndicator', transports, new_transports
        )

    # noinspection PyUnresolvedReferences
    def update_attribute(self, username, attr, old, new):
        """docstring for update_status"""
        conn = self.bind
        try:
            dn = "uid=%s,%s" % (username, current_app.config['LDAP_BASE_DN'])
            if old in ("", None, list()):
                mod_attrs = [
                    (ldap.MOD_ADD, attr, LDAPManager.value_to_ldap(new))
                ]
            elif new in ("", None, list()):
                mod_attrs = [
                    (ldap.MOD_DELETE, attr, LDAPManager.value_to_ldap(old))
                ]
            else:
                mod_attrs = [
                    (ldap.MOD_REPLACE, attr, LDAPManager.value_to_ldap(new))
                ]

            conn.modify_s(str(dn), mod_attrs)
            conn.unbind_s()

            return {"old": old, "new": new}

        except ldap.LDAPError as err:
            raise exceptions.ValidationError(
                message=str(getattr(err, 'message', err))
            )
        except Exception as err:
            raise exceptions.ValidationError(message=str(err))

    # noinspection PyUnresolvedReferences
    def delete_user(self, username):
        """docstring for delete_user"""
        user = self.get_user(uid=username)
        if user is None:
            raise exceptions.NotFound(
                message=MESSAGE_MAP["UserDoesNotExists"], extra=dict(
                    factory="openldap", msgid="UserDoesNotExists",
                    long_message="User '{}' doesn't exists !".format(username)
                )
            )

        conn = self.bind
        try:
            dn = "uid=%s,%s" % (username, current_app.config['LDAP_BASE_DN'])
            conn.delete_s(dn)
            conn.unbind_s()
            return user

        except ldap.LDAPError as err:
            raise exceptions.ValidationError(
                message=str(getattr(err, 'message', err))
            )
        except Exception as err:
            raise exceptions.ValidationError(message=str(err))
