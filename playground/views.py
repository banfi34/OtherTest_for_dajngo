from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Info
from .info import InfoForm


def base_html(request):
    return render(request, 'home.html')


# Create your views here.
def info_html(request):
    info_list = Info.objects.all()
    return render(request, 'info.html',
                  {'info_list': info_list,
                   })


def add_info(request):
    submitted = False
    if request.method == "POST":
        form = InfoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_info?submitted=True')
    else:
        form = InfoForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'add_info.html', {'info': form, 'submitted': submitted})
