from tortoise import Model, fields
from tortoise.queryset import QuerySet

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

    rates: fields.ForeignKeyRelation['Rate']
    as_target: fields.ForeignKeyRelation['Rate']

    async def _get_queryset_of_related_users(self) -> QuerySet:
        """
        Get users that are not disliked by current user.
        """
        queryset = User.filter(pk__not=self.pk)
        rate_queryset = await Rate.filter(rate_owner=self, type=False)
        if rate_queryset:
            queryset = queryset.filter(as_target__not_in=rate_queryset)
        return queryset

    async def _calculate_distance(self, my_coord: tuple[float, float], user: 'User') -> float:
        """
        Distance between two coordinates: longitude and latitude. In meters
        """
        user_coord = (user.longitude, user.latitude)
        coord_distance = distance.distance(my_coord, user_coord).meters
        return coord_distance

    async def find_matched_users(self) -> list[int]:
        """
        Conversion unit - meters
        If distance between two users is less than 'this' user search_distance - add iterated user`s id to list
        If user disliked profile before - exclude them from queryset
        """
        users = []
        my_coord = (self.longitude, self.latitude)
        queryset = await self._get_queryset_of_related_users()
        for user in await queryset:
            coord_distance = await self._calculate_distance(my_coord, user)
            if coord_distance <= float(self.search_distance):
                users.append(user.user_id)
        return users

    async def get_liked_users(self) -> list:
        queryset = (await self._get_queryset_of_related_users()).filter(as_target__type=True)
        users = []
        for user in await queryset:
            users.append(user.user_id)
        return users

    async def find_nearest(self) -> int:
        """
        Find nearest person from db. IMPORTANT - this person is not disliked by current user
        """
        nearest_distance = 6371000  # Earth radius
        my_coord = (self.longitude, self.latitude)
        queryset = await self._get_queryset_of_related_users()
        for user in await queryset:
            coord_distance = await self._calculate_distance(my_coord, user)
            if coord_distance < nearest_distance:
                nearest_distance = coord_distance
            else:
                continue
        return nearest_distance

    @staticmethod
    async def get_gender_display(gender_bool: bool) -> str:
        return 'Man' if gender_bool else 'Woman'


class Rate(Model):
    rate_owner = fields.ForeignKeyField('models.User', related_name='rates', on_delete=fields.CASCADE)
    target = fields.ForeignKeyField('models.User', related_name='as_target', on_delete=fields.CASCADE)
    type = fields.BooleanField()  # True is like. False is dislike
