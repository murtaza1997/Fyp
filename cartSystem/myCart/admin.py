from django.contrib import admin

# Register your models here.
from .models import Contact,ProCategory,ProdTable
admin.site.register(Contact),
admin.site.register(ProCategory),
admin.site.register(ProdTable)