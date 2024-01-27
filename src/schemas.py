from src.models import HEI, Entry
from src import db, ma

class HEISchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HEI
        include_fk = True
        load_instance = True
        sqla_session = db.session
        include_relationships = True

class EntrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Entry
        include_fk = True
        load_instance = True
        sqla_session = db.session
        include_relationships = True