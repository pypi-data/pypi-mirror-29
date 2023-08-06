from django.contrib import admin

from .models import CensusEstimate, CensusLabel, CensusTable, CensusVariable


class CensusVariableInline(admin.TabularInline):
    model = CensusVariable
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(CensusVariableInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )
        if db_field.name == 'label':
            if hasattr(request, '_obj_'):
                field.queryset = field.queryset.filter(
                    table=request._obj_
                )
            else:
                field.queryset = field.queryset.none()
        return field


class CensusLabelInline(admin.TabularInline):
    model = CensusLabel
    extra = 0


@admin.register(CensusTable)
class CensusTableAdmin(admin.ModelAdmin):
    inlines = [
        CensusLabelInline,
        CensusVariableInline
    ]
    list_display = ('year', 'series', 'code', 'title')
    list_filter = ('year', 'series')
    search_fields = ('code',)

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(CensusTableAdmin, self).get_form(request, obj, **kwargs)


@admin.register(CensusVariable)
class CensusVariableAdmin(admin.ModelAdmin):
    list_display = ('table', 'code')


@admin.register(CensusLabel)
class CensusLabelAdmin(admin.ModelAdmin):
    inlines = [
        CensusVariableInline
    ]
    search_fields = ('table',)
    list_filter = ('table__year', 'table__series')
    list_display = ('label', 'table')


@admin.register(CensusEstimate)
class CensusEstimateAdmin(admin.ModelAdmin):
    list_filter = ('variable__table__code',)
    list_display = (
        'variable_code',
        'table_code',
        'division_name',
        'estimate',
    )

    def variable_code(self, obj):
        return obj.variable.code

    def table_code(self, obj):
        return obj.variable.table.code

    def division_name(self, obj):
        return '{0}, {1}'.format(
            obj.division.name,
            obj.division.parent.name
        )
