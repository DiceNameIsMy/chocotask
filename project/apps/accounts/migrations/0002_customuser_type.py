# Generated by Django 3.2.8 on 2021-11-21 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='type',
            field=models.IntegerField(choices=[(1, 'Guest'), (2, 'Employee')], default=1),
        ),
    ]
