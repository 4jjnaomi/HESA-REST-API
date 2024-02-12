"""
This module contains the database models for the application.

The models define the structure and relationships between the database tables.

Classes:
- HEI: Represents a Higher Education Institution (HEI).
- Entry: Represents an entry in the database.
- User: Represents a user in the system.
- SavedChart: Represents a saved chart in the database.
"""
from typing import List
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from src import db


class HEI(db.Model):
    """
    Represents a Higher Education Institution (HEI).

    Attributes:
        UKPRN (int): The UK Provider Reference Number of the HEI.
        he_name (str): The name of the HEI.
        region (str): The region where the HEI is located.
        lat (str): The latitude coordinate of the HEI's location.
        lon (str): The longitude coordinate of the HEI's location.
        entries (List[Entry]): A list of Entry objects associated with the HEI.
    """
    __tablename__ = 'hei'
    UKPRN: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    he_name: Mapped[str] = mapped_column(db.Text, primary_key=True)
    region: Mapped[str] = mapped_column(db.Text, nullable=False)
    lat: Mapped[str] = mapped_column(db.Text, nullable=True)
    lon: Mapped[str] = mapped_column(db.Text, nullable=True)
    entries: Mapped[List['Entry']] = relationship(back_populates='hei')


class Entry(db.Model):
    """
    Represents an entry in the database.

    Attributes:
        entry_id (int): The ID of the entry (primary key).
        academic_year (str): The academic year of the entry.
        classification (str): The classification of the entry.
        category_marker (str): The category marker of the entry.
        category (str): The category of the entry.
        value (str): The value of the entry.
        UKPRN (int): The UKPRN associated with the entry.
        he_name (str): The name of the higher education institution associated with the entry.
        hei (HEI): The higher education institution object associated with the entry.
    """
    __tablename__ = 'entry'
    entry_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    academic_year: Mapped[str] = mapped_column(db.Text, nullable=False)
    classification: Mapped[str] = mapped_column(db.Text, nullable=False)
    category_marker: Mapped[str] = mapped_column(db.Text, nullable=False)
    category: Mapped[str] = mapped_column(db.Text, nullable=False)
    value: Mapped[str] = mapped_column(db.Text)
    UKPRN: Mapped[int] = mapped_column(db.Integer)
    he_name: Mapped[str] = mapped_column(db.Text)
    __table_args__ = (
        ForeignKeyConstraint(
            ['UKPRN', 'he_name'],
            ['hei.UKPRN', 'hei.he_name']
        ),
    )
    # add relationship to HEI table
    hei: Mapped['HEI'] = relationship('HEI', back_populates='entries')


class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        user_id (int): The unique identifier for the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
        saved_charts (List['SavedChart']): The list of saved charts associated with the user.
    """

    user_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.Text, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(
        db.Text, unique=True, nullable=False)
    saved_charts: Mapped[List['SavedChart']
                         ] = relationship(back_populates='user')

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def set_password(self, password: str):
        """
        Set the password for the user.

        Parameters:
        - password (str): The password to be set.

        Returns:
        - None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        """
        Check if the provided password matches the hashed password stored in the database.

        Args:
            password (str): The password to be checked.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)


class SavedChart(db.Model):
    """
    Represents a saved chart in the database.

    Attributes:
        chart_id (int): The ID of the saved chart (primary key).
        chart_name (str): The name of the saved chart.
        chart (bytes): The binary representation of the saved chart.
        user_id (int): The ID of the user who saved the chart.
        user (User): The user who saved the chart (relationship).

    """
    chart_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    chart_name: Mapped[str] = mapped_column(db.Text, nullable=True)
    chart: Mapped[bytes] = mapped_column(db.LargeBinary, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user: Mapped['User'] = relationship('User', back_populates='saved_charts')

# TODO: Add lat and lon data to dataset
