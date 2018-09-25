import django_filters

from .models import Staff

class StaffFilter(django_filters.FilterSet):
    class Meta:
        model = Staff
        fields = ['department']