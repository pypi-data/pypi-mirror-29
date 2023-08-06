from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from election.models import ElectionCycle
from government.models import Party


class PartyFilter(admin.SimpleListFilter):
    title = _('party')
    parameter_name = 'party'

    def lookups(self, request, model_admin):
        return [
            (party.ap_code, _(party.__str__()))
            for party in Party.objects.all()
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(party__ap_code=self.value())


class CycleFilter(admin.SimpleListFilter):
    title = _('cycle')
    parameter_name = 'cycle'

    def lookups(self, request, model_admin):
        return [
            (cycle.slug, _(cycle.name))
            for cycle in ElectionCycle.objects.all()
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(race__cycle__name=self.value())


class CandidateAdmin(admin.ModelAdmin):
    search_fields = ['person__full_name']
    list_filter = (PartyFilter, CycleFilter,)
