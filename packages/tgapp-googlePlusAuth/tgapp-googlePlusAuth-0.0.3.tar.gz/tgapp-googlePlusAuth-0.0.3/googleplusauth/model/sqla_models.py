# -*- coding: utf-8 -*-

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean, String
from sqlalchemy.orm import backref, relation, deferred
from googleplusauth.model import DBSession
from tgext.pluggable import app_model, primary_key


DeclarativeBase = declarative_base()


class GoogleAuth(DeclarativeBase):
    __tablename__ = 'googleplusauth_info'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    registered = Column(Boolean, default=False, nullable=False)
    just_connected = Column(Boolean, default=False, nullable=False)
    profile_picture = Column(String(512), nullable=True)

    user_id = Column(Integer, ForeignKey(primary_key(app_model.User)), nullable=False)
    user = relation(app_model.User, backref=backref('googleplusauth', uselist=False, cascade='all, delete-orphan'))

    google_id = Column(Unicode(255), nullable=False, index=True, unique=True)
    access_token = Column(Unicode(1200), nullable=False)
    access_token_expiry = Column(DateTime, nullable=False)

    @classmethod
    def ga_user_by_google_id(cls, google_id):
        google_auth_user = DBSession.query(cls).filter_by(google_id=google_id).first()
        return google_auth_user

    @classmethod
    def googleplusauth_user(cls, user_id):
        return DBSession.query(cls).filter_by(user_id=user_id).first()
