# Generated by Django 2.1.4 on 2019-01-02 09:53
import logging
import os
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tnadmin', '0002_custom_migr_add_constraints'),
    ]

    if 'SQLLITE' in os.environ.keys():
        logging.info('Skipping postgres-specific schema modification ')
    else:
        operations = [
            migrations.RunSQL(
                "INSERT  INTO tnadmin_gvfederation (gvfederationname, gvmetadataurl, gvScope) "
                "VALUES ('Verwaltungsportalverbund (Test)', 'http://mdfeed.test.portalverbund.gv.at/metadata.xml', 'initial');"
            ),
            migrations.RunSQL(
                "INSERT  INTO tnadmin_gvOrganisation (cn, gvouid, gvOuCn, gvouvkz, gvScope, ldap_dn, o) "
                "VALUES ('Verwaltungsportalverbund (Depositar innerhalb der TNV)', 'AT:PVP:0', 'nicht ändern', 'AG-IZ', 'intern', 'dummy', 'AG-IZ')"
                "ON CONFLICT DO NOTHING;"
            ),
        ]
