from django.contrib import admin

from .models import Body, Jurisdiction, Office, Party


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('body__label', 'jurisdiction__name',)
    search_fields = ['name']


admin.site.register(Body)
admin.site.register(Jurisdiction)
admin.site.register(Office, OfficeAdmin)
admin.site.register(Party)
