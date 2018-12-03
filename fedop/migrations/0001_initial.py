# Generated by Django 2.1.1 on 2018-12-03 09:25

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
                ('cacert', models.CharField(help_text='Issuer Certificate (TLS CA)', max_length=10000, unique=True, verbose_name='CA Certificate')),
                ('pvprole', models.CharField(choices=[('STP', 'STP'), ('AWP', 'AWP')], default='STP', max_length=3, null=True, verbose_name='Status')),
                ('subjectCN', models.CharField(help_text='Issuer X.509 SubjectCN (TLS CA)', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Namespaceobj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fqdn', models.CharField(help_text='fully qualified domain name or domain with * for any hostname, such as "*.sso.xyz.org"', max_length=30, unique=True, verbose_name='Namespace')),
            ],
            options={
                'verbose_name_plural': 'FQDN Namespaces',
                'verbose_name': 'FQDN Namespace',
                'ordering': ['fqdn'],
            },
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
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'STPbetreiber',
                'verbose_name': 'STPbetreiber',
            },
        ),
        migrations.CreateModel(
            name='Userprivilege',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cert', models.TextField(help_text='X.509 cert PEM ohen Whitespace', max_length=20000, unique=True, verbose_name='Portaladminsitrator-Zertifikat')),
                ('cn', models.CharField(blank=True, help_text='Vor- und Familienname des Zertifikatsinhabers', max_length=64, null=True, verbose_name='Name (cn)')),
                ('gvOuIdParent', models.ForeignKey(help_text='OrgID des Portalbetreibers', on_delete=django.db.models.deletion.PROTECT, to='fedop.STPbetreiber')),
            ],
            options={
                'ordering': ['cn'],
            },
        ),
        migrations.AddField(
            model_name='namespaceobj',
            name='gvOuIdParent',
            field=models.ForeignKey(help_text='OrgID des Portalbetreibers', on_delete=django.db.models.deletion.PROTECT, to='fedop.STPbetreiber'),
        ),
    ]
