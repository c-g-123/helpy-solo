from django.shortcuts import render


def render_error_message(request, template, error_message):
    return render(request, template, {'error_message': error_message})
