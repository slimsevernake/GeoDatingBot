from loader import dp
from .admin import IsAdmin


if __name__ == "filters":
    dp.filters_factory.bind(IsAdmin)
