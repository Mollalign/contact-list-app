from flask import request, jsonify, send_from_directory
from config import app, db
from models import Contact
import os

# Serve React Frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Tell Flask where the static React files are
app.static_folder = '../frontend/dist'
app.template_folder = "../frontend/dist"    

# POST: Create contact
@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "all fields are Required!"}),
            400
        )
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201


# GET: Contact
@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})


# PATCH: Update contact
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not Found!"}), 404
    
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "User Updated!"}), 200


# DELETE: Delete contact
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not Found!"}), 404
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User Deleted!"}), 200
    

# start app here
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

