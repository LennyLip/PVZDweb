# Generated by Django 2.1.1 on 2018-09-16 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Issuer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cacert', models.CharField(help_text='fully qualified domain name', max_length=128, unique=True, verbose_name='Namespace')),
                ('pvprole', models.CharField(help_text='Vor- und Familienname des Zertifikatsinhabers', max_length=64, verbose_name='Name (cn)')),
                ('subjectCN', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Revocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cert', models.CharField(help_text='X.509 cert PEM ohen Whitespace', max_length=128, unique=True, verbose_name='Zertifikat')),
            ],
        ),
        migrations.CreateModel(
            name='STPbetreiber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gvOuID', models.CharField(max_length=32, unique=True, verbose_name='gvOuId')),
                ('cn', models.CharField(help_text='Bezeichnung der Organisationseinheit (ausgeschrieben). (Abt. ITMS/Ref. NIK - \u2028Referat nationale und internationale Koordination)', max_length=64, verbose_name='Bezeichnung (cn)')),
            ],
            options={
                'verbose_name_plural': 'STPbetreiber',
                'verbose_name': 'STPbetreiber',
                'ordering': ['gvOuID'],
            },
        ),
        migrations.CreateModel(
            name='Testobj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fqdn', models.CharField(help_text='fully qualified domain name or domain with * for any hostname, such as "*.sso.xyz.org"', max_length=128, unique=True, verbose_name='Namespace')),
                ('gvOuIdParent', models.ForeignKey(help_text='OrgID des Portalbetreibers', on_delete=django.db.models.deletion.PROTECT, to='fedop.STPbetreiber')),
            ],
            options={
                'verbose_name_plural': 'FQDN Namespaces',
                'verbose_name': 'FQDN Namespace',
                'ordering': ['fqdn'],
            },
        ),
        migrations.CreateModel(
            name='Userprivilege',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cert', models.CharField(help_text='X.509 cert PEM ohen Whitespace', max_length=128, unique=True, verbose_name='Portaladminsitrator-Zertifikat')),
                ('cn', models.CharField(help_text='Vor- und Familienname des Zertifikatsinhabers', max_length=64, verbose_name='Name (cn)')),
                ('gvOuIdParent', models.ForeignKey(help_text='OrgID des Portalbetreibers', on_delete=django.db.models.deletion.PROTECT, to='fedop.STPbetreiber')),
            ],
            options={
                'ordering': ['cn'],
            },
        ),
    ]
