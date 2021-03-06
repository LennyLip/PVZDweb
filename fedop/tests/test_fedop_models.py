import os
import pathlib
import pytest
assert os.environ["DJANGO_SETTINGS_MODULE"] in ("pvzdweb.settings_pytest_dev", "pvzdweb.settings_pytest"), \
    "require in-memory-db for loading fixtures"

from django.core import management
from pvzdweb.settings import *
INSTALLED_APPS=list(set(INSTALLED_APPS + ['fedop']))

from fedop.models.issuer import *
from fedop.models.revocation import *
from fedop.models.namespace import *
from fedop.models.userprivilege import *
from tnadmin.models.gvfederationorg import *

#pytestmark = pytest.mark.django_db  # not working for whatever reason.
                                     # workaround from https://github.com/pytest-dev/pytest-django/issues/396
from pytest_django.plugin import _blocking_manager
from django.db.backends.base.base import BaseDatabaseWrapper
_blocking_manager.unblock()
_blocking_manager._blocking_wrapper = BaseDatabaseWrapper.ensure_connection


@pytest.fixture(scope="module")
def load_tnadmin1():
    management.call_command('migrate')
    tnadmin_data = pathlib.Path('tnadmin/fixtures/tnadmin1.json')
    assert tnadmin_data.is_file(), f'could not find file {tnadmin_data}'
    management.call_command('loaddata', tnadmin_data)

@pytest.fixture(scope="module")
def load_fedop1(load_tnadmin1):
    management.call_command('migrate')
    fedop_data = pathlib.Path('fedop/fixtures/fedop1.json')
    assert fedop_data.is_file(), f'could not find file {fedop_data}'
    management.call_command('loaddata', fedop_data)

def test_issuer(load_fedop1):
    i = Issuer.objects.filter(subject_cn='PortalRoot-CA')
    assert i.cacert == "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"
    assert i.pvprole
    assert i.subject_cn

def test_revocation():
    r = Revocation.objects.all()[0]  # only one item in testdata
    assert r.subject_cn == 'gondor.magwien.gv.at/emailAddress=cctprod-l@adv.magwien.gv.at'
    assert r.pubkey == 'dummy'
    assert r.cert

def test_namespace():
    i = Namespaceobj(fqdn='*.bmj.gv.at')
    assert i.gvouid_parent.gvouid == 'AT:B:1'


def test_userprivilege():
    cert = 'MIIEjzCCA3egAwIBAgIDGP0iMA0GCSqGSIb3DQEBBQUAMIGXMQswCQYDVQQGEwJBVDFIMEYGA1UECgw/QS1UcnVzdCBHZXMuIGYuIFNpY2hlcmhlaXRzc3lzdGVtZSBpbSBlbGVrdHIuIERhdGVudmVya2VociBHbWJIMR4wHAYDVQQLDBVhLXNpZ24tUHJlbWl1bS1TaWctMDIxHjAcBgNVBAMMFWEtc2lnbi1QcmVtaXVtLVNpZy0wMjAeFw0xNTA3MTAxMDI0MTNaFw0yMDA3MTAwODI0MTNaMF4xCzAJBgNVBAYTAkFUMRYwFAYDVQQDDA1SYWluZXIgSMO2cmJlMQ8wDQYDVQQEDAZIw7ZyYmUxDzANBgNVBCoMBlJhaW5lcjEVMBMGA1UEBRMMODkxMzQ4MDYxMzEwMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEitOBhEXzDGJ1V9idI3RvmHl4g5FYTqB0sp+KcvbwEFg1briOreGj2zXNOOhEzM+mDljuCv5D7QkHlHCk1Evc3KOCAeUwggHhMBEGA1UdDgQKBAhB3LUFPwWu4jAOBgNVHQ8BAf8EBAMCBsAwEwYDVR0jBAwwCoAITd/h/0vZyd8wCQYDVR0TBAIwADB7BggrBgEFBQcBAQRvMG0wQgYIKwYBBQUHMAKGNmh0dHA6Ly93d3cuYS10cnVzdC5hdC9jZXJ0cy9hLXNpZ24tUHJlbWl1bS1TaWctMDJhLmNydDAnBggrBgEFBQcwAYYbaHR0cDovL29jc3AuYS10cnVzdC5hdC9vY3NwMFkGA1UdIARSMFAwRAYGKigAEQELMDowOAYIKwYBBQUHAgEWLGh0dHA6Ly93d3cuYS10cnVzdC5hdC9kb2NzL2NwL2Etc2lnbi1QcmVtaXVtMAgGBgQAizABATAnBggrBgEFBQcBAwEB/wQYMBYwCAYGBACORgEBMAoGCCsGAQUFBwsBMIGaBgNVHR8EgZIwgY8wgYyggYmggYaGgYNsZGFwOi8vbGRhcC5hLXRydXN0LmF0L291PWEtc2lnbi1QcmVtaXVtLVNpZy0wMixvPUEtVHJ1c3QsYz1BVD9jZXJ0aWZpY2F0ZXJldm9jYXRpb25saXN0P2Jhc2U/b2JqZWN0Y2xhc3M9ZWlkQ2VydGlmaWNhdGlvbkF1dGhvcml0eTANBgkqhkiG9w0BAQUFAAOCAQEA08DFHxU01lhHnx/5s/n+Ue/LUQFNLaTxQYbmKuQ2zdiJBI33TQptMCQQITGZvJJBeTBgGguVu5547+BdnxonyULw+GkfBqR0ZBcS7ejEx9ujRnTZdUYNAXkTMnk25YAAX4DDgm3CHV850LVUt++ofaYgzv+HNSPGvu3gD3qGp6tJ1nlns0SVCIMBE+LHFh+9lBjCHCmPWosfEcCv2vSmL/PkQGtXKhegUPnnAJFzDqK4xrRm3uj53TXZwdWzYUWYeUggnvzck5sUQCtGlFLkaiAvS4dtnS9DuRuq82kqzHoTTSb6hWcVCoVBx4OswoOXeF6xhaCm7oYL6Q9fPi1zCQ=='
    u = Userprivilege(cert=cert)
    assert u.cn == "Rainer H\u00f6rbe"
    assert i.gvouid_parent.gvouid == 'AT:VKZ:XFN-318886a'