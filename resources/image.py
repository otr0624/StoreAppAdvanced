from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import send_file, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import os

from libs import image_helper
from libs.strings import gettext
from schemas.image import ImageSchema

image_schema = ImageSchema()


class ImageUpload(Resource):
    @jwt_required
    def post(self):
        """Used to upload an image file, save image to user's folder"""
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"  # e.g., static/images/user_1
        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            return {"message": gettext("image_uploaded").format(basename)}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400


class Image(Resource):
    @jwt_required
    def get(self, filename: str):
        """Returns requested image if it exists within logged in user's folder"""
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        if not image_helper.is_filename_safe(filename):
            return {'message': gettext("image_illegal_filename").format(filename)}, 400
        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {'message': gettext("image_not_found").format(filename)}, 404

    @jwt_required
    def delete(self, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        if not image_helper.is_filename_safe(filename):
            return {'message': gettext("image_illegal_filename").format(filename)}, 400

        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {'message': gettext("image_deleted").format(filename)}, 200
        except FileNotFoundError:
            return {'message': gettext("image_not_found").format(filename)}, 404
        except:
            traceback.print_exc()
            return {'message': gettext("image_delete_failed")}, 500


class AvatarUpload(Resource):
    @jwt_required
    def put(self):
        """Endpoint used to upload user avatar, named after user ID. Uploding new avatar overwrites existing"""
        data = image_schema.load(request.files)
        filename = f"user_{get_jwt_identity()}"
        folder = "avatars"
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {'message': gettext("avatar_delete_failed")}, 500
        try:
            ext = image_helper.get_extension(data["image"].filename)
            avatar = filename + ext
            avatar_path = image_helper.save_image(
                data["image"], folder=folder, name=avatar
            )
            basename = image_helper.get_basename(avatar_path)
            return {'message': gettext("avatar_uploaded").format(basename)}, 200
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {'message': gettext("image_illegal_extension").format(extension)}