from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(primary_key=True, max_length=200)
    isbn13 = models.CharField(max_length=99, blank=True, null=True)
    pagecount = models.CharField(db_column='pageCount', max_length=99, blank=True, null=True)  # Field name made lowercase.
    maturityrating = models.CharField(db_column='maturityRating', max_length=99, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(max_length=99, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'books'

