from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

from core.texts import BADWORDS


def validate_clean_text(data):
    words_list = set(data.split())
    for word in words_list:
        if word.lower() in BADWORDS:
            raise ValidationError('Ненормативная лексика')


username_validator = UnicodeUsernameValidator()
