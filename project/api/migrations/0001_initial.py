# Generated by Django 4.1.2 on 2022-10-15 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Database',
            fields=[
                ('idDatabase', models.AutoField(primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=15)),
                ('port', models.IntegerField()),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('idTable', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('database', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.database')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('idRecord', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('database', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.database')),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('idColumn', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('information_type', models.CharField(max_length=50)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.table')),
            ],
        ),
    ]
