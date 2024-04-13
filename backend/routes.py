from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/picture", methods=["GET"])
def get_pictures():
    # Return the data list as JSON
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################
    # Define the route for the GET method on the /picture/<id> endpoint
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    # Search for the picture with the given ID
    for picture in data:
        if picture["id"] == id:
            # Return the picture as JSON
            return jsonify(picture), 200

    # If picture with the given ID is not found, return 404 Not Found
    abort(404)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # Extract picture data from request body
    picture_data = request.json

    # Check if picture with the same id already exists
    for picture in data:
        if picture["id"] == picture_data["id"]:
            # Return the existing picture data
            return jsonify(picture), 302

    # Append the new picture data to the data list
    data.append(picture_data)

    # Return the new picture data with status code 201 Created
    return jsonify(picture_data), 201

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Extract updated picture data from request body
    updated_picture_data = request.json

    # Find the picture with the given id
    for picture in data:
        if picture["id"] == id:
            # Update picture data
            picture.update(updated_picture_data)
            return jsonify(picture), 200

    # If picture with the given ID is not found, return 404 Not Found
    abort(404)

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find the index of the picture with the given id
    for index, picture in enumerate(data):
        if picture["id"] == id:
            # Delete the picture from the data list
            del data[index]
            # Return 204 No Content
            return "", 204

    # If picture with the given ID is not found, return 404 Not Found
    abort(404)