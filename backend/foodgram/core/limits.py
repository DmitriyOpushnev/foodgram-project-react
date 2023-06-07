from enum import IntEnum


class Limits(IntEnum):
    """Числовые постоянные проекта."""

    USER_MODEL_EMAIL_FIELDS_LENGHT = 254
    USER_MODEL_OTHER_FIELDS_LENGHT = 150
    INGRIDIENT_RECIPE_FIELDS_TAG_LENGHT = 200
    HEX_COLOR_FIELD_LENGHT = 7
    MIN_COOKING_TIME = 1
    MAX_COOKING_TIME = 600
    MIN_INGREDIENTS_AMOUNT = 1
