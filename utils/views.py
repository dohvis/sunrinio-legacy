from django.shortcuts import render


def template_debug(request, dir_name, template_name):
    return render(request, '{}/{}.html'.format(dir_name, template_name))
