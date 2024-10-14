from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apis_core.apis_entities.models import AbstractEntity
from apis_core.core.models import LegacyDateMixin
from apis_core.utils.helpers import create_object_from_uri
from apis_core.generic.abc import GenericModel
from apis_core.apis_entities.abc import E53_Place
from apis_core.history.models import VersionMixin
from apis_core.utils.fields import NewlineSeparatedListField


class LegacyStuffMixin(models.Model):
    sources = GenericRelation("Source")

    class Meta:
        abstract = True

    @classmethod
    def get_or_create_uri(cls, uri):
        print(f"using custom get_or_create_uri with {uri}")
        return create_object_from_uri(uri, cls) or cls.objects.get(pk=uri)

    @property
    def uri(self):
        contenttype = ContentType.objects.get_for_model(self)
        uri = reverse("apis_core:generic:detail", args=[contenttype, self.pk])
        return uri


class Source(GenericModel, models.Model):
    orig_filename = models.CharField(max_length=255, blank=True)
    indexed = models.BooleanField(default=False)
    pubinfo = models.CharField(max_length=400, blank=True)
    author = models.CharField(max_length=255, blank=True)
    orig_id = models.PositiveIntegerField(blank=True, null=True)
    pdf_filename = models.CharField(blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        if retstr := self.orig_filename:
            if self.author:
                retstr += f" stored by {self.author}"
            return retstr
        return f"(ID: {self.id})".format(self.id)


class Title(GenericModel, models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Title")
        verbose_name_plural = _("Titles")


class ProfessionCategory(GenericModel, models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Profession Category")
        verbose_name_plural = _("Profession Categories")


class Profession(GenericModel, models.Model):
    class Meta:
        ordering = ("name",)
        verbose_name = _("Profession")
        verbose_name_plural = _("Professions")

    name = models.CharField(max_length=255, blank=True)
    oldids = models.TextField(null=True)
    oldnames = models.TextField(null=True)

    def __str__(self):
        return self.name or f"No name ({self.id})"


class Event(LegacyStuffMixin, VersionMixin, LegacyDateMixin, AbstractEntity):
    kind = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name="Name", blank=True)
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")


class Institution(VersionMixin, LegacyStuffMixin, LegacyDateMixin, AbstractEntity):
    kind = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name="Name", blank=True)
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))
    textsnippet_protokoll = models.TextField(blank=True, verbose_name="Textsnippet Protokoll")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Institution")
        verbose_name_plural = _("Institutions")


class Person(VersionMixin, LegacyStuffMixin, LegacyDateMixin, AbstractEntity):
    GENDER_CHOICES = (
        ("female", "female"),
        ("male", "male"),
        ("third gender", "third gender"),
    )
    surname = models.CharField(max_length=255, verbose_name="Name", blank=True)
    forename = models.CharField(max_length=255, help_text="The persons´s forename. In case of more then one name...", blank=True, null=True)
    profession = models.ManyToManyField(Profession, blank=True)
    professioncategory = models.ForeignKey(ProfessionCategory, on_delete=models.CASCADE, null=True, blank=True)
    title = models.ManyToManyField(Title, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, blank=True, null=True)
    external_resources = models.CharField(verbose_name="Externe Verweise", blank=True, null=True)
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))
    alternative_names = NewlineSeparatedListField(blank=True, verbose_name=_("Alternative Names"))

    #texts
    # "ÖBL Haupttext"
    textsnippet_protokoll = models.TextField(blank=True, verbose_name="Textsnippet Protokoll")

    def __str__(self):
        return f"{self.forename} {self.surname}"


    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")


class Place(E53_Place, VersionMixin, LegacyStuffMixin, LegacyDateMixin, AbstractEntity):
    kind = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))
    textsnippet_protokoll = models.TextField(blank=True, verbose_name="Textsnippet Protokoll")

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _("Place")
        verbose_name_plural = _("Places")


class Work(LegacyStuffMixin, VersionMixin, LegacyDateMixin, AbstractEntity):
    kind = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name="Name", blank=True)
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))
    nbr_tei_xml_data = models.TextField(blank=True, verbose_name="NBR TEI XML data")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Work")
        verbose_name_plural = _("Works")


class Denomination(AbstractEntity):
    name = models.CharField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Denomination")
        verbose_name_plural = _("Denominations")
