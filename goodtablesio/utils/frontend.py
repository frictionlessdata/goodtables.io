from flask import render_template
from flask_login import current_user

from goodtablesio import settings


# Module API

def render_component(component, props=None):
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

    if not props:
        props = {}

    # Common props
    if props == {} or (props and 'userName' not in props):
        user_name = getattr(current_user, 'display_name')
        if not user_name:
            user_name = getattr(current_user, 'name')
        props['userName'] = user_name
    return render_template(
        filename, component=component, props=props.copy(),
        google_analytics_code=settings.GOOGLE_ANALYTICS_CODE)
