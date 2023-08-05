import os

from django import template

import ajax_forms

register = template.Library()

VALIDATION_SCRIPT = None

def include_validation():
    global VALIDATION_SCRIPT # pylint: disable=global-statement
    if VALIDATION_SCRIPT is None:
        VALIDATION_SCRIPT = open(os.path.join(os.path.dirname(ajax_forms.__file__), 'media', 'ajax_forms', 'js', 'jquery-ajax-validation.js')).read()
    return '<script type="text/javascript">%s</script>' % VALIDATION_SCRIPT
register.simple_tag(include_validation)
