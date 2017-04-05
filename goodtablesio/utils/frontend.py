from flask import render_template
from flask_login import current_user

from goodtablesio import settings


# Module API

def render_component(component, props={}):
    """Render frontend component within html layout.

    Args:
        component (str): component name
        props (dict): component props

    Returns:
        str: rendered component

    """
    filename = 'index.min.html'
    if settings.DEBUG:
        filename = 'index.html'

    # Common props
    if not props or (props and 'userName' not in props):
        props['userName'] = getattr(current_user, 'display_name', None)

    return render_template(filename, component=component, props=props.copy())
