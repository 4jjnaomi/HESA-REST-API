"""
This module contains the schema classes for serializing and deserializing HEI and Entry objects.

The HEISchema class is used to serialize and deserialize 
HEI objects. It automatically generates fields 
based on the model's attributes.

The EntrySchema class is used to convert Entry objects to 
JSON format and vice versa. It inherits from the SQLAlchemyAutoSchema 
class provided by the Marshmallow library.

Both classes define metadata options for the schema, such as whether
 to include foreign key fields, whether to load instances when 
 deserializing, the SQLAlchemy session to use, and whether to include relationships in the schema.
"""

from src.models import HEI, Entry
from src import db, ma


class HEISchema(ma.SQLAlchemyAutoSchema):
    """
    Serializer schema for the HEI model.

    This schema is used to serialize and deserialize HEI objects.
    It automatically generates fields based on the model's attributes.

    Attributes:
        Meta: A nested class that defines the schema's metadata.

    """
    class Meta:
        """
        Meta class for defining options for the HEI schema.

        Attributes:
            model (class): The model class associated with the schema.
            include_fk (bool): Whether to include foreign key fields in the schema.
            load_instance (bool): Whether to load an existing instance when deserializing data.
            sqla_session (object): The SQLAlchemy session to use for database operations.
            include_relationships (bool): Whether to include relationships in the schema.
        """
        model = HEI
        include_fk = True
        load_instance = True
        sqla_session = db.session
        include_relationships = False


class EntrySchema(ma.SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing Entry objects.

    This class defines the structure and behavior of the EntrySchema, which is used to convert Entry objects
    to JSON format and vice versa. It inherits from the SQLAlchemyAutoSchema class provided by the Marshmallow
    library.

    Attributes:
        Meta: A nested class that defines metadata options for the schema.

    """

    class Meta:
        """
        Meta class for defining options for the Entry schema.

        Attributes:
            model: The model class to be used for the schema.
            include_fk: Whether to include foreign key fields in the schema.
            load_instance: Whether to load the instance when deserializing.
            sqla_session: The SQLAlchemy session to be used for the schema.
            include_relationships: Whether to include relationships in the schema.
        """
        model = Entry
        include_fk = True
        load_instance = True
        sqla_session = db.session
        include_relationships = False
