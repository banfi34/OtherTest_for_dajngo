from django.db.models import Avg
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import Info, Pages, InfoReview
from .forms import InfoForm, ReviewAdd
from django.core.paginator import Paginator
from .filter import InfoFilter, ReviewFilter


def delete_info(request, info_id):
    info = Info.objects.get(pk=info_id)
    if request.user.is_staff or request.user.id == info.publisher_id:
        info.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.add_message(request, messages.INFO,
                             'You are not authorized!!')
        return redirect(request.META.get('HTTP_REFERER'))


def delete_review(request, review_id, info_id):
    info = Info.objects.get(pk=info_id)
    review = InfoReview.objects.get(pk=review_id)
    if request.user.is_staff or request.user.id == review.user_id:
        review.delete()
        avg_reviews = InfoReview.objects.filter(info=info).aggregate(avg_rating=Avg('review_rating'))
        info.sumRev = avg_reviews['avg_rating']
        info.save()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.add_message(request, messages.INFO,
                             'You are not authorized!!')
        return redirect(request.META.get('HTTP_REFERER'))


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        pages_list = Pages.objects.filter(page_name__contains=searched)
        if not request.user.is_staff:
            pages_list = pages_list.filter(auth_users__id=request.user.id)

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
    if request.user.is_staff and Pages.objects.all().filter(id=request.user.id):
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
    pages = Pages.objects.get(page_name="info")
    info = Info.objects.all()
    p = Paginator(info.order_by('-sumRev'), 6)
    page = request.GET.get('page')
    infos = p.get_page(page)

    reviews = InfoReview.objects.all()
    getTrue = True
    myFilter = InfoFilter(request.GET, queryset=info)
    newFilter = ReviewFilter(request.GET, queryset=reviews)

    if not myFilter.qs.exists():
        getTrue = False

    if request.GET.get('name') or request.GET.get('publisher_name') or request.GET.get('review_rating'):
        if request.GET.get('review_rating'):
            pg = Paginator(myFilter.qs.filter(sumRev__startswith=request.GET.get('review_rating'))
                           .all().order_by('-sumRev'), 6)
            page = request.GET.get('page')
            infos = pg.get_page(page)
            if not myFilter.qs.filter(sumRev__startswith=request.GET.get('review_rating')).all():
                getTrue = False
        else:
            pg = Paginator(myFilter.qs.all().order_by('-sumRev'), 6)
            page = request.GET.get('page')
            infos = pg.get_page(page)

        if not getTrue:
            messages.add_message(request, messages.INFO,
                                 'Could not find what you searched for')
            return redirect(request.META.get('HTTP_REFERER'))

    if request.user.is_staff:
        return render(request, 'info/info.html',
                      {'infos': infos,
                       'reviews': reviews,
                       'newFilter': newFilter,
                       'myFilter': myFilter,
                       'getTrue': getTrue,
                       })

    elif request.user.is_authenticated and pages.auth_users.filter(id=request.user.id):
        return render(request, 'info/info.html',
                      {'infos': infos,
                       'reviews': reviews,
                       'newFilter': newFilter,
                       'myFilter': myFilter,
                       'getTrue': getTrue,
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
                if not form.data['publisher_name']:
                    info = form.save(commit=False)
                    info.publisher_name = 'Anonymous'

            info = form.save(commit=False)
            info.publisher_id = request.user.id
            info.save()

            return HttpResponseRedirect('/add_info?submitted=True')
        else:
            form = InfoForm
            if 'submitted' in request.GET:
                submitted = True

        return render(request, 'info/add_info.html', {'info': form, 'submitted': submitted})


def save_review(request, pid):
    info = Info.objects.get(pk=pid)
    user = request.user
    review = InfoReview.objects.create(
        user=user,
        info=info,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
    )
    data = {
        'user': user.username,
        'review_text': request.POST['review_text'],
        'review_rating': request.POST['review_rating']
    }

    # Fetch avg rating for reviews
    avg_reviews = InfoReview.objects.filter(info=info).aggregate(avg_rating=Avg('review_rating'))
    info.sumRev = avg_reviews['avg_rating']
    info.save()
    # End

    return redirect(request.META.get('HTTP_REFERER'), {'data': data})


def info_review(request, id):
    info = Info.objects.get(id=id)
    reviewForm = ReviewAdd()

    # Check
    canAdd = True
    reviewCheck = InfoReview.objects.filter(user=request.user, info=info).count()
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd = False
    # End

    # Fetch reviews
    reviews = InfoReview.objects.filter(info=info)
    # End

    # Fetch avg rating for reviews
    avg_reviews = InfoReview.objects.filter(info=info).aggregate(avg_rating=Avg('review_rating'))
    # End

    rev = InfoReview.objects.all().values_list('info_id', flat=True).filter(info_id=info).count()
    return render(request, 'review/review_info.html',
                  {'info': info,
                   'reviewForm': reviewForm,
                   'canAdd': canAdd, 'reviews': reviews,
                   'avg_reviews': avg_reviews,
                   'rev': rev,
                   })
