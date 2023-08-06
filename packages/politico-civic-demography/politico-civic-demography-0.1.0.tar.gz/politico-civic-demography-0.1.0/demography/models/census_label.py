from django.db import models


class CensusLabel(models.Model):
    """
    Custom labels for census variables that allow us to
    aggregate variables.
    """
    AGGREGATION_CHOICES = (
        ('s', 'Sum'),
        ('a', 'Average'),
        ('m', 'Median'),
    )
    label = models.CharField(max_length=100)
    aggregation = models.CharField(
        max_length=1,
        choices=AGGREGATION_CHOICES,
        default='s'
    )
    table = models.ForeignKey(
        'CensusTable',
        on_delete=models.CASCADE,
        related_name='labels'
    )

    def __str__(self):
        return self.label
