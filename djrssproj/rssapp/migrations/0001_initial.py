# Generated by Django 4.2.8 on 2023-12-26 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=32, unique=True)),
                ('title', models.TextField()),
                ('publication_date', models.DateTimeField()),
                ('source', models.TextField()),
                ('link', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('source_image', models.TextField(blank=True, null=True)),
                ('image', models.TextField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, default=None, null=True)),
            ],
            options={
                'db_table': 'article_titles_db',
            },
        ),
    ]
