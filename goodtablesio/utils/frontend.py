from flask import render_template
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
    return render_template(filename, component=component, props=props.copy())
