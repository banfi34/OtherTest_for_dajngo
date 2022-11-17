import django_filters
from .models import *


class InfoFilter(django_filters.FilterSet):
    class Meta:
        model = Info
        fields = '__all__'
        exclude = ['publisher', 'info']
