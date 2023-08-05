# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates
from zope.deprecation import deprecation

from ziggurat_foundations.models.base import BaseModel
from ziggurat_foundations.models.base import get_db_session
from ziggurat_foundations.models.services.user_resource_permission import \
    UserResourcePermissionService

__all__ = ['UserResourcePermissionMixin']


class UserResourcePermissionMixin(BaseModel):
    """
    Mixin for UserResourcePermission model
    """
    __table_args__ = (sa.PrimaryKeyConstraint(
        'user_id', 'resource_id', 'perm_name',
        name='pk_users_resources_permissions '),
                      {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})

    _ziggurat_services = [UserResourcePermissionService]

    @declared_attr
    def __tablename__(self):
        return 'users_resources_permissions'

    @declared_attr
    def user_id(self):
        return sa.Column(sa.Integer, sa.ForeignKey('users.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'),
                         primary_key=True)

    @declared_attr
    def resource_id(self):
        return sa.Column(sa.Integer(),
                         sa.ForeignKey('resources.resource_id',
                                       onupdate='CASCADE',
                                       ondelete='CASCADE'),
                         primary_key=True,
                         autoincrement=False)

    @declared_attr
    def perm_name(self):
        return sa.Column(sa.Unicode(64), primary_key=True)

    @validates('perm_name')
    def validate_perm_name(self, key, value):
        if value != value.lower():
            raise AssertionError('perm_name needs to be lowercase')
        return value

    def __repr__(self):
        return '<UserResourcePermission: %s, %s, %s>' % (self.user_id,
                                                         self.perm_name,
                                                         self.resource_id,)

    @classmethod
    @deprecation.deprecate("UserResourcePermission.by_resource_user_and_perm "
                           "will be removed in 0.8, use service instead")
    def by_resource_user_and_perm(cls, user_id, perm_name, resource_id,
                                  db_session=None):
        """

        .. deprecated:: 0.8

        :param user_id:
        :param perm_name:
        :param resource_id:
        :param db_session:
        :return:
        """
        db_session = get_db_session(db_session)
        return UserResourcePermissionService.by_resource_user_and_perm(
            user_id=user_id, perm_name=perm_name, resource_id=resource_id,
            db_session=db_session)
