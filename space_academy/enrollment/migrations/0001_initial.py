# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Имя кандидата', max_length=64)),
                ('age', models.IntegerField(verbose_name='Возраст')),
                ('email', models.EmailField(verbose_name='email', max_length=254)),
                ('is_padawan', models.BooleanField(verbose_name='Яаляется падаваном', default=False)),
                ('answers', models.TextField(verbose_name='Тестовые вопросы и ответы кандидата', default='[]')),
            ],
            options={
                'verbose_name': 'Кандидат',
                'verbose_name_plural': 'Кандидаты',
                'db_table': 'candidates',
            },
        ),
        migrations.CreateModel(
            name='Jedies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Имя джедая', max_length=64)),
            ],
            options={
                'verbose_name': 'Джедай',
                'verbose_name_plural': 'Джедаи',
                'db_table': 'jedies',
            },
        ),
        migrations.CreateModel(
            name='Planets',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Наименование планеты', max_length=64)),
            ],
            options={
                'verbose_name': 'Планета',
                'verbose_name_plural': 'Планеты',
                'db_table': 'planets',
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('question', models.TextField(max_length=128)),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'db_table': 'questions',
            },
        ),
        migrations.CreateModel(
            name='Quests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('order_code', models.CharField(max_length=16)),
                ('questions', models.ManyToManyField(to='enrollment.Questions')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
                'db_table': 'quests',
            },
        ),
        migrations.AddField(
            model_name='jedies',
            name='planet',
            field=models.ForeignKey(to='enrollment.Planets'),
        ),
        migrations.AddField(
            model_name='candidates',
            name='mentor',
            field=models.ForeignKey(verbose_name='Наставник', null=True, to='enrollment.Jedies'),
        ),
        migrations.AddField(
            model_name='candidates',
            name='planet',
            field=models.ForeignKey(verbose_name='Планета', to='enrollment.Planets'),
        ),
    ]
