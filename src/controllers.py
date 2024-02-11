from flask import current_app as app, request, make_response, abort, jsonify
from sqlalchemy import exc
from marshmallow.exceptions import ValidationError

from src.schemas import HEISchema, EntrySchema
from src import db
from src.models import HEI, Entry


hei_schema = HEISchema()
heis_schema = HEISchema(many=True)
entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)


@app.route("/")
def index():
    return "Index Page"

@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}"

#HEI routes

@app.get("/hei")
def get_heis():
    all_heis = db.session.execute(db.select(HEI)).scalars()

    result = heis_schema.dump(all_heis)

    return result

@app.get("/hei/<UKPRN>")
def get_hei_using_ukprn(UKPRN):
    chosen_hei = db.session.execute(db.select(HEI).filter_by(UKPRN=UKPRN)).scalar_one_or_none()
    return hei_schema.dump(chosen_hei)

@app.get("/hei/<hei_name>")
def get_hei_using_name(hei_name):
    hei = db.session.execute(db.select(HEI).filter(HEI.he_name == hei_name)).scalar_one_or_none()
    print(hei.he_name)

    return hei_schema.dump(hei)

@app.post("/hei")
def add_hei():
    hei_json = request.get_json()
    hei = hei_schema.load(hei_json)
    db.session.add(hei)
    db.session.commit()
    return {"message": f"HEI {hei.he_name} added successfully"}

@app.delete("/hei/<UKPRN>")
def delete_hei_using_ukprn(UKPRN):
    hei = db.session.execute(db.select(HEI).filter(HEI.UKPRN == UKPRN)).scalar_one_or_none()
    db.session.delete(hei)
    db.session.commit()
    return {"message": f"HEI {hei.UKPRN} deleted successfully"}

@app.delete("/hei/<he_name>")
def delete_hei_using_name(HEI_name):
    hei = db.session.execute(db.select(HEI).filter(HEI.he_name == HEI_name)).scalar_one_or_none()
    db.session.delete(hei)
    db.session.commit()
    return {"message": f"HEI {hei.he_name} deleted successfully"}

@app.patch("/hei/<UKPRN>")
def hei_update(UKPRN):
    hei = db.session.execute(db.select(HEI).filter(HEI.UKPRN == UKPRN)).scalar_one_or_none
    hei_json = request.get_json()
    hei_update = hei_schema.load(hei_json, instance=hei, partial=True)
    db.session.add(hei_update)
    db.session.commit()
    updated_hei = db.session.execute(db.select(HEI).filter(HEI.UKPRN == UKPRN)).scalar_one_or_none()
    result = hei_schema.jsonify(updated_hei)
    response = make_response(result, 200)
    return response


#Entry routes
@app.get("/entry")
def get_entries():
    all_entries = db.session.execute(db.select(Entry)).scalars()

    result = entries_schema.dump(all_entries)

    return result

@app.get("/entry/<id>")
def get_entry(id):
    one_entry = db.session.execute(db.select(Entry).filter_by(entry_id=id)).scalar_one_or_none()
    return entry_schema.dump(one_entry)

@app.post("/entry")
def add_entry():
    entry_json = request.get_json()
    entry = entry_schema.load(entry_json)
    db.session.add(entry)
    db.session.commit()
    return {"message": f"Entry {entry.entry_id} added successfully"}

@app.delete("/entry/<id1>")
def delete_entry(id1):
    one_entry = db.session.execute(db.select(Entry).filter_by(entry_id=id1)).scalar_one_or_none()
    db.session.delete(one_entry)
    db.session.commit()
    return {"message": f"Entry {id1} deleted successfully"}

@app.patch("/entry/<entry_id>")
def entry_update(entry_id):
    entry = db.session.execute(db.select(Entry).filter_by(entry_id=entry_id)).scalar_one_or_none()
    entry_json = request.get_json()
    entry_updated = entry_schema.load(entry_json, instance=entry, partial=True)
    db.session.add(entry_updated)
    db.session.commit()
    updated_entry = db.session.execute(db.select(Entry).filter_by(entry_id=entry_id)).scalar_one_or_none()
    result = entry_schema.jsonify(updated_entry)
    response = make_response(result, 200)
    return response
