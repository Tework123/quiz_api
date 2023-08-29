# Generated by Django 4.2.4 on 2023-08-29 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0003_image_alter_relationship_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='close',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='attachment',
            field=models.ManyToManyField(blank=True, to='messenger.image'),
        ),
    ]
