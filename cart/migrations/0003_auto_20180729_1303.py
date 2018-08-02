# Generated by Django 2.0.7 on 2018-07-29 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0005_meal_description'),
        ('cart', '0002_auto_20180728_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meal.Meal')),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='meal',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='quantity',
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(to='cart.CartItems'),
        ),
    ]