# Generated by Django 4.2.6 on 2023-11-09 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sducraft', '0004_rename_server_imagesetforhistorynode_historynode'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagesetforhistorynode',
            name='name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
