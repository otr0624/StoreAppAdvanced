from ma import ma
from marshmallow import pre_dump, fields
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)


    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "confirmation")
        load_instance = True

    @pre_dump
    def _pre_dump(self, user: UserModel):
        user.confirmation = [user.most_recent_confirmation]
        return user
