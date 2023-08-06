from django.db import models


class CensusVariable(models.Model):
    """
    Individual variables on census series to pull, e.g.,  "001E" on ACS table
    19001, the total for household income.
    """
    code = models.CharField(
        max_length=4,
        help_text="3 digit code for variable and 'E', e.g., 001E."
    )
    table = models.ForeignKey(
        'CensusTable',
        related_name='variables',
        on_delete=models.CASCADE
    )
    label = models.ForeignKey(
        'CensusLabel',
        related_name='variables',
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    def __str__(self):
        return '{}_{}'.format(
            self.table.code,
            self.code
        )
