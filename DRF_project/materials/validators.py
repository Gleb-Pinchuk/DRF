import re
from django.core.exceptions import ValidationError


def validate_video_url(value):
    """
    Разрешает только ссылки на Rutube
    """
    if not value:
        return

    allowed_domains = ['rutube.com', 'rutube.ru']

    pattern = r'^https?://(?:www\.)?([^/]+)'
    match = re.search(pattern, value)

    if not match:
        raise ValidationError('Некорректный URL')

    domain = match.group(1).lower()

    if not any(allowed in domain for allowed in allowed_domains):
        raise ValidationError('Разрешены только ссылки на Rutube')
