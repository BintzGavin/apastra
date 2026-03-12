def render_template(template, variables):
    """
    Renders a prompt template by replacing {{variable_name}} with the value
    from the variables dict. Handles string, list, and dict templates.
    """
    if not variables:
        return template

    if isinstance(template, str):
        result = template
        for k, v in variables.items():
            result = result.replace(f"{{{{{k}}}}}", str(v))
        return result

    if isinstance(template, list):
        return [render_template(item, variables) for item in template]

    if isinstance(template, dict):
        return {k: render_template(v, variables) for k, v in template.items()}

    return template