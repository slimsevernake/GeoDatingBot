from tortoise import Model, fields


class User(Model):
    user_id = fields.IntField()
    username = fields.CharField(max_length=100)
    description = fields.TextField()
    gender = fields.BooleanField()  # True - main. False - woman
    interested_gender = fields.BooleanField()
    age = fields.IntField()
    longitude = fields.FloatField()
    latitude = fields.FloatField()
    search_distance = fields.IntField()


class UserProfile(Model):
    user: fields.OneToOneRelation[User] = fields.OneToOneField('models.User', on_delete=fields.CASCADE,
                                                               related_name='profile')
    likes = fields.IntField(default=0)
    dislikes = fields.IntField(default=0)
    matched = fields.IntField(default=0)
