import re
from rest_framework.serializers import ValidationError


class DescriptionsValidator:
    """
    Validator for descriptions.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if not tmp_value:
            return
        pattern = r"https?://(?!www\.youtube\.com)|http://(?!www\.youtube\.com)"
        if re.search(pattern, tmp_value):
            raise ValidationError(
                "Описание не должно содержать ссылок кроме https://www.youtube.com/"
            )
