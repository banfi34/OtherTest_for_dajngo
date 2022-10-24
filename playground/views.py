from django.db.models.functions import Lower
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Info
from .info import InfoForm


def delete_info(request, info_id):
    info = Info.objects.get(pk=info_id)
    if request.user.is_staff or request.user.id == info.publisher_id:
        info.delete()
        return redirect('info')
    else:
        messages.add_message(request, messages.INFO,
                             'You are not authorized!!')
        return redirect('info')


def base_html(request):
    return render(request, 'home.html')


# Create your views here.
def info_html(request):
    info_list = Info.objects.all().order_by('id')
    return render(request, 'info/info.html',
                  {'info_list': info_list,
                   })


def add_info(request):
    if request.user.is_anonymous:
        messages.add_message(request, messages.INFO,
                             'You must be logged in')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        submitted = False
        if request.method == "POST":
            form = InfoForm(request.POST)
            if form.is_valid():
                info = form.save(commit=False)
                info.publisher_id = request.user.id
                info.save()

                return HttpResponseRedirect('/add_info?submitted=True')
        else:
            form = InfoForm
            if 'submitted' in request.GET:
                submitted = True

        return render(request, 'info/add_info.html', {'info': form, 'submitted': submitted})
