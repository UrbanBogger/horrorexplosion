import re
from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter(name='get_all_media_objects')
def get_all_media_objects(dict_list, media_object_type):
    return [feature for feature in dict_list if feature['type'] ==
            media_object_type]


@register.filter(name='highlight_search')
def hightlight_search(text, search_term):
    pattern = re.compile(r'(\s\(\d{4}\))', re.MULTILINE)
    search_term_as_list = [str(search_term)]

    if not (isinstance(text, str)):
        text = str(text)

    split_text = None
    if re.search(pattern, text):
        split_text = re.split(pattern, text)
        text = split_text[0]

    highlighted = re.sub(
        '(?i)(' + '|'.join(map(re.escape, search_term_as_list)) + ')',
        r'<strong style="color:red;">\1</strong>', text)

    if split_text:
        return mark_safe(highlighted + split_text[1])
    else:
        return mark_safe(highlighted)
