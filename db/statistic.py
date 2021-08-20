from db.models import User

from tortoise.functions import Avg
from tortoise.query_utils import Q


class Statistic:

    async def report(self) -> dict:
        data = {
            'Users': await User.all().count(),
            'Men': await User.filter(gender=1).count(),
            'Women': await User.filter(gender=0).count(),
            'Average age': await self.average_age(),
            'Average age for men': await self.average_age_for_gender(True),
            'Average age for women': await self.average_age_for_gender(False)
        }
        return data

    async def average_age(self) -> int:
        average = await User.all().annotate(average=Avg('age')).values('average')
        if average:
            return average[0].get('average')
        return 0

    async def average_age_for_gender(self, gender: bool) -> int:
        average = await User.all().annotate(average=Avg('age', _filter=Q(gender=gender))).values('average')
        if average:
            return average[0].get('average')
        return 0
