# Generated by Django 3.1 on 2020-08-07 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('title', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('isbn13', models.CharField(blank=True, max_length=99, null=True)),
                ('pagecount', models.CharField(blank=True, db_column='pageCount', max_length=99, null=True)),
                ('maturityrating', models.CharField(blank=True, db_column='maturityRating', max_length=99, null=True)),
                ('category', models.CharField(blank=True, max_length=99, null=True)),
            ],
        ),
    ]
