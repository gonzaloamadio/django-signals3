from django.http import HttpResponse
import csv

class ExportCsvMixin:
    """
        Mixing to use in Django admin.
        Example:
            @admin.register(Hero)
            class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
                actions = ["export_as_csv"]
                ...

        In dropdown actions will be added this export to csv action
    """
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected to CSV"
