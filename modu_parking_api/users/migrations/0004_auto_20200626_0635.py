# Generated by Django 3.0.7 on 2020-06-26 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_bookmark_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phoneNum',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
