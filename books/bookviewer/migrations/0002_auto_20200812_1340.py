# Generated by Django 3.1 on 2020-08-12 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookviewer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goodreads_Id',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='userid',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='bookviewer.goodreads_id'),
            preserve_default=False,
        ),
    ]
