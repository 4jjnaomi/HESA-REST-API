from typing import List
from sqlalchemy import Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from src import db

class HEI(db.Model):
    __tablename__ = 'hei'
    UKPRN: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    he_name: Mapped[str] = mapped_column(db.Text, primary_key=True)
    region: Mapped[str] = mapped_column(db.Text, nullable = False)
    lat: Mapped[str] = mapped_column(db.Text, nullable = True)
    lon: Mapped[str] = mapped_column(db.Text, nullable = True)
    entries: Mapped[List['Entry']] = relationship(back_populates='hei')

class Entry(db.Model):
    __tablename__ = 'entry'
    entry_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    academic_year: Mapped[str] = mapped_column(db.Text, nullable = False)
    classification: Mapped[str] = mapped_column(db.Text, nullable = False)
    category_marker: Mapped[str] = mapped_column(db.Text, nullable = False)
    category: Mapped[str] = mapped_column(db.Text, nullable = False)
    value: Mapped[str] = mapped_column(db.Text)
    UKPRN: Mapped[int] = mapped_column(db.Integer)
    he_name: Mapped[str] = mapped_column(db.Text)
    __table_args__ = (
        ForeignKeyConstraint(
            ['UKPRN', 'he_name'],
            ['hei.UKPRN', 'hei.he_name']
        ),
    )
    #add relationship to HEI table
    hei: Mapped['HEI'] = relationship('HEI', back_populates='entries')

class User(db.Model):
    user_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.Text, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.Text, unique=True, nullable=False)
    saved_charts: Mapped[List['SavedChart']] = relationship( back_populates='user')

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
    
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

class SavedChart(db.Model):
    chart_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    chart_name: Mapped[str] = mapped_column(db.Text, nullable=True)
    chart: Mapped[bytes] = mapped_column(db.LargeBinary, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user: Mapped['User'] = relationship('User', back_populates='saved_charts')

# TODO: Add lat and lon data to dataset
