# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates
from zope.deprecation import deprecation

from ziggurat_foundations.models.base import BaseModel
from ziggurat_foundations.models.base import get_db_session
from ziggurat_foundations.models.services.user_permission import \
    UserPermissionService

__all__ = ['UserPermissionMixin']


class UserPermissionMixin(BaseModel):
    """
    Mixin for UserPermission model
    """
    __table_args__ = (sa.PrimaryKeyConstraint('user_id', 'perm_name',
                                              name='pk_users_permissions'),
                      {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})

    _ziggurat_services = [UserPermissionService]

    @declared_attr
    def __tablename__(self):
        return 'users_permissions'

    @declared_attr
    def user_id(self):
        return sa.Column(sa.Integer,
                         sa.ForeignKey('users.id', onupdate='CASCADE',
                                       ondelete='CASCADE'), primary_key=True)

    @declared_attr
    def perm_name(self):
        return sa.Column(sa.Unicode(64), primary_key=True)

    @validates('perm_name')
    def validate_perm_name(self, key, value):
        if value != value.lower():
            raise AssertionError('perm_name needs to be lowercase')
        return value

    def __repr__(self):
        return '<UserPermission: %s>' % self.perm_name

    @classmethod
    @deprecation.deprecate("UserPermission.by_user_and_perm "
                           "will be removed in 0.8, use service instead")
    def by_user_and_perm(cls, user_id, perm_name, db_session=None):
        """

        .. deprecated:: 0.8

        :param user_id:
        :param perm_name:
        :param db_session:
        :return:
        """
        db_session = get_db_session(db_session)
        return UserPermissionService.by_user_and_perm(
            user_id=user_id, perm_name=perm_name, db_session=db_session)
