from django.shortcuts import render


def template_debug(request, dir_name, template_name):
    if dir_name == 'index':
        return render(request, 'index.html')
    return render(request, '{}/{}.html'.format(dir_name, template_name))
