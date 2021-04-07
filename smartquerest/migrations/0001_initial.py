# Generated by Django 3.1.7 on 2021-04-05 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cab_name', models.CharField(max_length=255)),
                ('tg_id', models.BigIntegerField(default=-1)),
                ('key', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('tg_id', models.BigIntegerField(default=-1)),
                ('cabinets', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.ManyToManyField(to='smartquerest.Cabinet')),
            ],
        ),
        migrations.AddField(
            model_name='cabinet',
            name='guests',
            field=models.ManyToManyField(to='smartquerest.Guest'),
        ),
    ]