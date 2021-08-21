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
    photo = fields.CharField(max_length=255)

    likes = fields.IntField(default=0)
    dislikes = fields.IntField(default=0)
    matched = fields.IntField(default=0)

    @staticmethod
    async def get_gender_display(gender_bool: bool) -> str:
        return 'Man' if gender_bool else 'Woman'
