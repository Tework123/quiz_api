# Generated by Django 4.2.4 on 2023-08-21 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_resultanswer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultanswer',
            name='result',
        ),
    ]