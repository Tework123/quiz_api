# Generated by Django 4.2.4 on 2023-08-19 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0013_alter_user_email'),
        ('quiz', '0003_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='consumer',
        ),
        migrations.AddField(
            model_name='quiz',
            name='group',
            field=models.ManyToManyField(to='auth.group'),
        ),
    ]