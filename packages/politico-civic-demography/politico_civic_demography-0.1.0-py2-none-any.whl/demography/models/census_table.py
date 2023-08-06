from django.db import models


class CensusTable(models.Model):
    """
    A census series.
    """
    SERIES_CHOICES = (
        ('acs1', 'American Community Survey 1-year data profiles'),
        ('acs5', 'American Community Survey 5-year'),
        ('sf1', 'Decennial census, SF1'),
        ('sf3', 'Decennial census, SF3'),
    )
    series = models.CharField(max_length=4, choices=SERIES_CHOICES)
    year = models.CharField(max_length=4)
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        if self.title:
            return '{} {} ({})'.format(self.year, self.code, self.title)
        return '{} {}'.format(self.year, self.code)
