from tortoise import Model, fields

from geopy import distance


class User(Model):
    user_id = fields.IntField()
    full_name = fields.CharField(max_length=100)
    username = fields.CharField(max_length=255)
    description = fields.TextField()
    gender = fields.BooleanField()  # True - main. False - woman
    interested_gender = fields.BooleanField()
    age = fields.IntField()
    longitude = fields.FloatField()
    latitude = fields.FloatField()
    search_distance = fields.IntField()
    photo = fields.CharField(max_length=255)

    likes = fields.IntField(default=0)
    likers = fields.ManyToManyField('models.User', related_name='liked')

    dislikes = fields.IntField(default=0)
    dislikers = fields.ManyToManyField('models.User', related_name='disliked')

    matched = fields.IntField(default=0)

    async def find_matched_users(self) -> list[int]:
        """
        Conversion unit - meters
        If distance between two users is less than 'this' user search_distance - add iterated user`s id to list
        If user disliked profile before - exclude them from queryset
        """
        users = []
        my_coord = (self.longitude, self.latitude)
        for user in await User.filter(dislikers__not=self.pk, pk__not=self.pk):
            user_coord = (user.longitude, user.latitude)
            coord_distance = distance.distance(my_coord, user_coord).meters
            if coord_distance <= self.search_distance:
                users.append(user.user_id)
        return users

    @staticmethod
    async def get_gender_display(gender_bool: bool) -> str:
        return 'Man' if gender_bool else 'Woman'
