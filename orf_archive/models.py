from datetime import date
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models


class Oe1Program(models.Model):
    orf_id = models.IntegerField(unique=True)
    t_day = models.DateField(default=date.today)
    filenames = ArrayField(models.CharField(max_length=200))
    data = JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['orf_id'], name='org_id_i'),
            models.Index(fields=['t_day'], name='t_day_i'),
            models.Index(fields=['filenames'], name='filenames_i'),
        ]

    def __str__(self):
        return 'Ö1_program <{}>'.format(self.data.get('href'))

