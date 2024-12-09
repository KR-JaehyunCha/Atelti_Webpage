# Generated by Django 5.1.3 on 2024-12-09 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=50)),
                ('number', models.PositiveIntegerField()),
                ('nationality', models.CharField(max_length=50)),
                ('birth_date', models.DateField()),
                ('image_url', models.URLField()),
            ],
        ),
    ]
