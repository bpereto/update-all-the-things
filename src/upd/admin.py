from django.contrib import admin
from upd.models import Product, Version

# pylint: disable=missing-class-docstring


class VersionAdmin(admin.ModelAdmin):
    readonly_fields = ('indexed',)


class VersionInline(admin.TabularInline):
    model = Version
    fields = ('version', 'date_published')

class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = (VersionInline,)

admin.site.register(Product, ProductAdmin)
admin.site.register(Version, VersionAdmin)
