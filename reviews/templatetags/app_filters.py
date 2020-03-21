from django import template

register = template.Library()


@register.filter(name='get_all_media_objects')
def get_all_media_objects(dict_list, media_object_type):
    return [feature for feature in dict_list if feature['type'] ==
            media_object_type]
