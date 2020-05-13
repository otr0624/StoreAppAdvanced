from ma import ma
from marshmallow import pre_dump, Schema, fields
from models.user import UserModel


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)


    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "confirmation")

    @pre_dump
    def _pre_dump(self, user: UserModel):
        user.confirmation = [user.most_recent_confirmation]
        return user
