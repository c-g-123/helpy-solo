from django.shortcuts import render


def render_error_message(request, template, error_message, context=None):
    if context:
        context['error_message'] = error_message
        return render(request, template, context)

    return render(request, template, {'error_message': error_message})
