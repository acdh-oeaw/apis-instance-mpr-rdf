import django_tables2 as tables
from apis_core.apis_entities.tables import AbstractEntityTable
from django_tables2.utils import A
from .models import Person



class PersonTable(AbstractEntityTable):
    class Meta:
        model = Person
        fields = ["surname", "forename", "start_date", "end_date"]
        exclude = ["desc"]


    surname = tables.Column(linkify=lambda record: record.get_edit_url(), empty_values=[],)
    forename = tables.Column(linkify=lambda record: record.get_edit_url(), empty_values=[],)

    def render_surname(self, record):
        return record.surname or "No name"

    def render_start_date(self, record):
        if record.start_date:
            return record.start_date.year
        return "-"

    def render_end_date(self, record):
        if record.end_date:
            return record.end_date.year
        return "-"
