# Generated by Django 3.0.2 on 2020-01-24 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcomment',
            old_name='username',
            new_name='name',
        ),
    ]
