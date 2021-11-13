'''
Schema definitions for data models
'''

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flaskserver.database import Base


class Asset_Account(Base):
    """
    Asset Account - 
    main account table back propagated with transactions, and assets
    """
    __tablename__ = 'accounts'
    account_no = Column(Integer, primary_key=True, nullable=False)
    assets = relationship("Asset")
    transactions = relationship("Asset_Transaction")

    def __init__(self, account_no=None):
        self.account_no = account_no

    def __repr__(self):
        return f'<Account no. {self.account_no}>'


class Asset(Base):
    """
    Asset -
    record of all assets ref'd by account no.
    """
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True, nullable=False)
    asset = Column(String(10), nullable=False)
    amount = Column(Float, nullable=False)
    owner_account = Column(Integer, ForeignKey('accounts.account_no'))
    owner = relationship("Asset_Account", back_populates="assets")


class Asset_Transaction(Base):
    """
    Asset Transaction -
    record of every transaction ref'd by acc no
    """
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, nullable=False)
    asset = Column(String(10), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    owner_account = Column(Integer, ForeignKey('accounts.account_no'))
    owner = relationship("Asset_Account", back_populates="transactions")
