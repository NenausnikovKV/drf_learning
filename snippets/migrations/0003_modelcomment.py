# Generated by Django 4.2.7 on 2024-01-05 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_alter_snippet_highlighted'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=30)),
            ],
        ),
    ]
