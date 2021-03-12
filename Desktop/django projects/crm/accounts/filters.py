import django_filters
from .models import *
from django_filters import CharFilter

class filterorder(django_filters.FilterSet):
    search=CharFilter(field_name="status",lookup_expr="icontains")
    class Meta:
        model=Order
        fields="__all__"
