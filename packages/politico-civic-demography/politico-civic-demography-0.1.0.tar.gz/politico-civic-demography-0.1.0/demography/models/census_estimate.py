from django.db import models
from geography.models import Division


class CensusEstimate(models.Model):
    """
    Individual census series estimates.
    """
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name='census_estimates'
    )
    variable = models.ForeignKey(
        'CensusVariable',
        on_delete=models.CASCADE,
        related_name='estimates'
    )
    estimate = models.FloatField()

    @property
    def full_code(self):
        return '{}_{}'.format(
            self.variable.table.code,
            self.variable.code
        )

    def __str__(self):
        return '{} {}_{}'.format(
            self.division.code,
            self.variable.table.code,
            self.variable.code
        )
