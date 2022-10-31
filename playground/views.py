from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Info, Pages
from .forms import InfoForm
from django.core.paginator import Paginator


def delete_info(request, info_id):
    info = Info.objects.get(pk=info_id)
    if request.user.is_staff or request.user.id == info.publisher_id:
        info.delete()
        return redirect('info')
    else:
        messages.add_message(request, messages.INFO,
                             'You are not authorized!!')
        return redirect('info')


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        pages_list = Pages.objects.filter(page_name__contains=searched)
        info = Info.objects.filter(publisher_name__contains=searched).order_by('-id') \
               or Info.objects.filter(name__contains=searched).order_by('-id')
        return render(request, 'search/search.html',
                      {'searched': searched,
                       'pages': pages_list,
                       'info': info})

    else:
        return render(request, 'search/search.html',
                      {})


def about_html(request):
    page = Pages.objects.get(page_name="about")
    if request.user.is_authenticated and page.auth_users.filter(id=request.user.id) or request.user.is_staff:
        return render(request, 'about/about.html')

    else:
        messages.add_message(request, messages.INFO,
                             'You dont have access to this site')
        return redirect('home')


def contact_html(request):
    page = Pages.objects.get(page_name="contact")
    if request.user.is_authenticated and page.auth_users.filter(id=request.user.id) or request.user.is_staff:
        return render(request, 'contact/contact.html')

    else:
        messages.add_message(request, messages.INFO,
                             'You dont have access to this site')
        return redirect('home')


def base_html(request):
    if request.user.is_staff:
        pages_list = Pages.objects.all().order_by('id')
        return render(request, 'homes/home.html',
                      {'pages_list': pages_list,
                       })

    elif request.user.is_authenticated and Pages.objects.filter(auth_users__id=request.user.id):
        pages_list = Pages.objects.all().filter(auth_users__id=request.user.id).order_by('id')
        return render(request, 'homes/home.html',
                      {'pages_list': pages_list,
                       })

    else:
        return render(request, 'homes/welcome.html')


def home_info_html(request):
    page = Pages.objects.get(page_name="info")
    if request.user.is_staff:
        pages_list = Pages.objects.all().order_by('id')
        return render(request, 'homes/info/home_info.html',
                      {'pages_list': pages_list,
                       })

    elif request.user.is_authenticated and page.auth_users.filter(id=request.user.id):
        pages_list = Pages.objects.all().filter(auth_users__id=request.user.id).order_by('id')
        return render(request, 'homes/info/home_info.html',
                      {'pages_list': pages_list,
                       })

    else:
        messages.add_message(request, messages.INFO,
                             'You dont have access to this site')
        return redirect('home')


def home_contact_html(request):
    page = Pages.objects.get(page_name="contact")
    if request.user.is_staff:
        pages_list = Pages.objects.all().order_by('id')
        return render(request, 'homes/contact/home_contact.html',
                      {'pages_list': pages_list,
                       })

    elif request.user.is_authenticated and page.auth_users.filter(id=request.user.id):
        pages_list = Pages.objects.all().filter(auth_users__id=request.user.id).order_by('id')
        return render(request, 'homes/contact/home_contact.html',
                      {'pages_list': pages_list,
                       })

    else:
        messages.add_message(request, messages.INFO,
                             'You dont have access to this site')
        return redirect('home')


def home_about_html(request):
    page = Pages.objects.get(page_name="about")
    if request.user.is_staff:
        pages_list = Pages.objects.all().order_by('id')
        return render(request, 'homes/about/home_about.html',
                      {'pages_list': pages_list,
                       })

    elif request.user.is_authenticated and page.auth_users.filter(id=request.user.id):
        pages_list = Pages.objects.all().filter(auth_users__id=request.user.id).order_by('id')
        return render(request, 'homes/about/home_about.html',
                      {'pages_list': pages_list,
                       })

    else:
        messages.add_message(request, messages.INFO,
                             'You dont have access to this site')
        return redirect('home')


# Create your views here.
def info_html(request):
    page = Pages.objects.get(page_name="info")
    if request.user.is_staff:

        p = Paginator(Info.objects.all().order_by('-id'), 6)
        page = request.GET.get('page')
        infos = p.get_page(page)

        return render(request, 'info/info.html',
                      {'infos': infos
                       })

    elif request.user.is_authenticated and page.auth_users.filter(id=request.user.id):
        p = Paginator(Info.objects.all().order_by('-id'), 6)
        page = request.GET.get('page')
        infos = p.get_page(page)
        return render(request, 'info/info.html',
                      {'infos': infos
                       })

    else:
        messages.add_message(request, messages.INFO,
                             'You dont have access to this site')
        return redirect('home')


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
