from django.contrib import admin

from .models import Partner, Project, QuoteRequest, Service, SiteSettings, Stat

admin.site.site_header = "Hira Engineering Consultancy admin"
admin.site.site_title = "Hira admin"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only one settings row should ever exist.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "year", "featured")
    list_filter = ("featured", "year")
    search_fields = ("name", "location")


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("number", "label", "order")
    list_editable = ("order",)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    readonly_fields = ("created_at",)
    search_fields = ("name", "email")

    def has_add_permission(self, request):
        return False
