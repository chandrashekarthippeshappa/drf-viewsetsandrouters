# Generated by Django 2.1.5 on 2019-02-13 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20190213_2237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='group_id',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='photo_id',
        ),
        migrations.AlterField(
            model_name='photo',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Group'),
        ),
    ]
