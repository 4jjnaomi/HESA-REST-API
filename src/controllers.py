from flask import current_app as app
from src.schemas import HEISchema, EntrySchema
from src import db
from src.models import HEI, Entry
from flask import request, make_response

hei_schema = HEISchema()
heis_schema = HEISchema(many=True)
entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)


@app.route("/")
def index():
    return "Index Page"

@app.route("/hei")
def get_heis():
    all_heis = db.session.execute(db.select(HEI)).scalars()

    result = heis_schema.dump(all_heis)

    return result

@app.route("/entry")
def get_entries():
    all_entries = db.session.execute(db.select(Entry)).scalars()

    result = entries_schema.dump(all_entries)

    return result

# TODO: Add a route to get a single HEI by UKPRN & he_name
# TODO: Add a route to get a single Entry by entry_id
