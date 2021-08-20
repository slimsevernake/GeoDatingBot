from tortoise import Model, fields


class User(Model):
    user_id = fields.IntField()
    username = fields.CharField(max_length=100)
    description = fields.TextField()
    gender = fields.BooleanField()  # True - main. False - woman
    interested_gender = fields.BooleanField()
    age = fields.IntField()
    age_suffix = fields.CharField(max_length=5, null=True)
    longitude = fields.FloatField()
    latitude = fields.FloatField()
    search_distance = fields.IntField()
    photo = fields.CharField(max_length=255)

    @property
    def user_age(self) -> str:
        return f'{self.age} {self.age_suffix}'

    @staticmethod
    async def get_gender_display(gender_bool: bool) -> str:
        return 'Мужчина' if gender_bool else 'Женщина'

    @staticmethod
    async def get_age_suffix(age: int) -> str:
        suffix = ("год" if 11 <= age <= 19 or age % 10 == 1 else
                  "года" if 2 <= age % 10 <= 4 else
                  "лет")
        return suffix


class UserProfile(Model):
    user: fields.OneToOneRelation[User] = fields.OneToOneField('models.User', on_delete=fields.CASCADE,
                                                               related_name='profile')
    likes = fields.IntField(default=0)
    dislikes = fields.IntField(default=0)
    matched = fields.IntField(default=0)
