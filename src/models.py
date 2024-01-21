from typing import List
from sqlalchemy import Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src import db

class HEI(db.Model):
    __tablename__ = 'hei'
    UKPRN: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    he_name: Mapped[str] = mapped_column(db.Text, primary_key=True)
    region: Mapped[str] = mapped_column(db.Text, nullable = False)
    lat: Mapped[float] = mapped_column(db.Float, nullable = True)
    lon: Mapped[float] = mapped_column(db.Float, nullable = True)
    # add relationship to Entry table
    entries: Mapped[List['Entry']] = relationship(back_populates='hei')

class Entry(db.Model):
    __tablename__ = 'entry'
    academic_year: Mapped[str] = mapped_column(db.Text, primary_key=True)
    classification: Mapped[str] = mapped_column(db.Text, primary_key=True)
    category_marker: Mapped[str] = mapped_column(db.Text, primary_key=True)
    category: Mapped[str] = mapped_column(db.Text, primary_key=True)
    value: Mapped[str] = mapped_column(db.Text, nullable = False)
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
    password: Mapped[str] = mapped_column(db.Text, unique=True, nullable=False)
    saved_charts: Mapped[List['SavedChart']] = relationship( back_populates='user')

# TODO: Change password to be a hashed password
    def __init__(self, email: str, password: str):
        """
        Create a new User object using the plain text password.
        :type password_string: str
        :type email: str
        :returns None
        """
        self.email = email
        self.password = password

class SavedChart(db.Model):
    chart_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    chart_name: Mapped[str] = mapped_column(db.Text, nullable=True)
    chart: Mapped[bytes] = mapped_column(db.LargeBinary, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user: Mapped['User'] = relationship('User', back_populates='saved_charts')


