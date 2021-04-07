# Generated by Django 3.1.7 on 2021-04-06 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartquerest', '0002_auto_20210406_0825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cabinet',
            name='guests',
        ),
        migrations.AddField(
            model_name='cabinet',
            name='query',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='guest',
            name='cabinet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartquerest.cabinet'),
        ),
        migrations.AlterField(
            model_name='cabinet',
            name='tg_id',
            field=models.BigIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='cabinets',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]