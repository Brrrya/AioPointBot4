from sqlalchemy import (
    Column, Integer, String, BigInteger, Boolean, Sequence, ForeignKey, Date
)

from sqlalchemy.orm import relationship

from database.connect import Base


class Admins(Base):
    __tablename__ = 'admins'

    id = Column(Integer, Sequence('admins_id', start=1))
    nick = Column(String, nullable=False)
    tgid = Column(BigInteger, primary_key=True)


class Directors(Base):
    __tablename__ = 'directors'

    id = Column(Integer, Sequence('directors_id', start=1))
    first_name = Column(String(length=30), nullable=False)
    last_name = Column(String(length=30), nullable=False)
    tgid = Column(BigInteger, primary_key=True)
    badge = Column(BigInteger, unique=True, nullable=False)


class Supervisors(Base):
    __tablename__ = 'supervisors'

    id = Column(Integer, Sequence('supervisor', start=1))
    first_name = Column(String(length=30), nullable=False)
    last_name = Column(String(length=30), nullable=False)
    tgid = Column(BigInteger, primary_key=True)
    badge = Column(BigInteger, unique=True, nullable=False)

    sellers = relationship('Sellers', back_populates='sv', order_by='Sellers.last_name')
    shops = relationship('Shops', back_populates='sv', order_by='Shops.title')


class Sellers(Base):
    __tablename__ = 'sellers'

    id = Column(Integer, Sequence('seller_id', start=1))
    first_name = Column(String(length=30), nullable=False)
    last_name = Column(String(length=30), nullable=False)
    tgid = Column(BigInteger, primary_key=True)
    badge = Column(BigInteger, unique=True, nullable=True)
    supervisor = Column(ForeignKey('supervisors.tgid'), nullable=True)

    sv = relationship('Supervisors', back_populates='sellers')


class Shops(Base):
    __tablename__ = 'shops'

    id = Column(Integer, Sequence('shop_id', start=1))
    title = Column(String(length=30), nullable=False)
    bd_title = Column(String(length=30), nullable=False)
    tgid = Column(BigInteger, primary_key=True)
    supervisor = Column(ForeignKey('supervisors.tgid'), nullable=False)
    worker = Column(ForeignKey('sellers.tgid'), nullable=True)
    state = Column(Boolean(), default=False, nullable=False)
    rotate = Column(Boolean(), default=False, nullable=False)
    open_checker = Column(ForeignKey('sellers.tgid'), nullable=True)
    rotate_checker = Column(ForeignKey('sellers.tgid'), nullable=True)
    close_checker = Column(ForeignKey('sellers.tgid'), nullable=True)
    fridges_state = Column(Boolean(), default=False, nullable=False)

    seller = relationship('Sellers', foreign_keys='Shops.worker')
    sv = relationship('Supervisors', back_populates='shops')
    reports = relationship('Reports', back_populates='shops')
    photos = relationship('Photos', back_populates='shops')


class Reports(Base):
    __tablename__ = 'reports'

    id = Column(BigInteger, primary_key=True)
    report_date = Column(Date(), nullable=False)
    seller_tgid = Column(BigInteger, nullable=False)
    shop_tgid = Column(ForeignKey('shops.tgid'), nullable=False)
    rto = Column(Integer, nullable=False)
    ckp = Column(Integer, nullable=False)
    check = Column(Integer, nullable=False)
    dcart = Column(Integer, nullable=False)
    p_rto = Column(Integer, nullable=False)
    p_ckp = Column(Integer, nullable=False)
    p_check = Column(Integer, nullable=False)

    shops = relationship('Shops', back_populates='reports')


class Photos(Base):
    __tablename__ = 'photos'

    id = Column(BigInteger, primary_key=True)
    photo_tgid = Column(String(), nullable=False)
    shop_tgid = Column(ForeignKey('shops.tgid'), nullable=False)
    action = Column(String(length=30), nullable=False)
    p_date = Column(Date(), nullable=False)

    shops = relationship('Shops', back_populates='photos')


class Registers(Base):
    __tablename__ = 'registers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(length=30), nullable=False)
    last_name = Column(String(length=30), nullable=False)
    supervisor = Column(ForeignKey('supervisors.tgid'), nullable=False)
    badge = Column(BigInteger, unique=True, nullable=False)
    reg_code = Column(Integer(), nullable=False)


class Coefs(Base):
    __tablename__ = 'coefs'

    id = Column(Integer, primary_key=True)
    coef = Column(Integer(), nullable=False)
    full_coef = Column(Integer(), nullable=False)
