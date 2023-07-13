import django_filters
from .models import MostanadatDakheli, MostanadatKhareji
from django import forms

class MostanadatDakheliFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', label="عنوان")
    dakheliSanadCode = django_filters.NumberFilter(field_name='dakheliSanadCode', label="کد سند")
    typeMadrakCode = django_filters.CharFilter(field_name='typeMadrakCode', label="نوع مدرک")
    systemMortabetCode = django_filters.NumberFilter(field_name='systemMortabetCode', label="سیستم مرتبط")
    vahedMortabetCode = django_filters.CharFilter(field_name="vahedMortabetCode", label="واحد مرتبط ")
    
    class Meta:
        model = MostanadatDakheli
        fields = ['title', 'dakheliSanadCode', 'typeMadrakCode', 'systemMortabetCode', "vahedMortabetCode"]
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
            super(MostanadatDakheliFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
            self.filters['title'].field.widget.attrs.update({'class': 'form-control'})
            self.filters['dakheliSanadCode'].field.widget.attrs.update({'class': 'form-control'})
            self.filters['typeMadrakCode'].field.widget.attrs.update({'class': 'form-control'})
            self.filters['systemMortabetCode'].field.widget.attrs.update({'class': 'form-control'})
            self.filters['vahedMortabetCode'].field.widget.attrs.update({'class': 'form-control'})
    


class MostanadatKharejiFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', label="عنوان")
    processCode = django_filters.CharFilter(field_name='processCode', label="فرآیند مرتبط")
    refrenceName = django_filters.CharFilter(field_name='refrenceName', label="نام مرجع")
    created_at = django_filters.DateFilter(field_name='created_at', label="تاریخ انتشار")

    class Meta:
        model = MostanadatKhareji
        fields = ['title', 'processCode', 'refrenceName', 'created_at']

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super(MostanadatKharejiFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        self.filters['title'].field.widget.attrs.update({'class': 'form-control'})
        self.filters['processCode'].field.widget.attrs.update({'class': 'form-control'})
        self.filters['refrenceName'].field.widget.attrs.update({'class': 'form-control'})
        self.filters['created_at'].field.widget.attrs.update({'class': 'form-control'})
            