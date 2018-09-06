# Generated by Django 2.0.6 on 2018-07-29 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('market_simulator', '0007_auto_20180729_0923'),
    ]

    operations = [
        migrations.CreateModel(
            name='LongPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_price', models.FloatField(default=0)),
                ('profit_or_loss', models.FloatField(default=0)),
                ('curr_quantity', models.IntegerField(default=0)),
                ('is_open', models.NullBooleanField(default=None)),
                ('symbol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='market_simulator.Symbol')),
            ],
        ),
    ]
