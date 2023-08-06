# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('django_mailman3', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mail_domain', models.CharField(unique=True, max_length=255, db_index=True)),
                ('site', models.ForeignKey(related_name='mailman_domains', to='sites.Site', on_delete=models.CASCADE)),
            ],
        ),
    ]
