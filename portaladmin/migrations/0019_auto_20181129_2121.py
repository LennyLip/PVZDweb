# Generated by Django 2.1.1 on 2018-11-29 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portaladmin', '0018_auto_20181129_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='mdstatement',
            name='namespace',
            field=models.CharField(default='created', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='mdstatementhistory',
            name='namespace',
            field=models.CharField(default='created', max_length=30, null=True),
        ),
    ]
