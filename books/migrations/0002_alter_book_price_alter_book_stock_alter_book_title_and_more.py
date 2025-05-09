# Generated by Django 4.2 on 2025-05-09 04:12

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='book',
            name='stock',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='stockevent',
            name='scheduled_for',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 12, 4, 12, 13, 675572, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterUniqueTogether(
            name='stockevent',
            unique_together={('book', 'scheduled_for')},
        ),
    ]
