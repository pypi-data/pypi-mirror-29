"""Django models to handle Thema codes and descriptions."""

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _


class ThemaCategory(models.Model):
    """Model that represents the Thema categories.

    The field `header` contains the heading in English.
    """

    code = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('ThemaCategory', null=True)
    header = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(default="")

    class Meta:
        """Meta options for the thema category admin."""

        ordering = ('updated_at', )

    def __str__(self):
        """String representation for each instance of the model."""
        return self.code

    @property
    def local_header(self):
        """Return the header translated to the activated language."""
        return _(self.header)

    @property
    def local_notes(self):
        """Return the notes translated to the activated language."""
        return _(self.notes)
