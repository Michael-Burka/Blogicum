# Generated by Django 3.2.16 on 2023-06-10 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_comment_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created_at',)},
        ),
    ]