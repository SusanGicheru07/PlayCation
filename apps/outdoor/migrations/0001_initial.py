import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OutdoorLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
                'verbose_name': 'Outdoor Location',
                'verbose_name_plural': 'Outdoor Locations',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='OutdoorActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('activity', models.CharField(choices=[('hike', 'Hike Trail'), ('park', 'Park'), ('sport', 'Sports Ground'), ('bird_watching', 'Bird Watching'), ('camping', 'Camping'), ('fishing', 'Fishing'), ('market', 'Outdooor Market'), ('picnic', 'Picnic Area'), ('photography', 'Photography'), ('other', 'Other')], default='other', max_length=50)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('notes', models.TextField(blank=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='outdoor.outdoorlocation')),
            ],
            options={

                'verbose_name': 'Outdoor Activity',
                'verbose_name_plural': 'Outdoor Activities',
                'ordering': ['name', 'activity'],
                'unique_together': {('name', 'activity')},
            },
        ),
    ]
