from django.db import models
from tnadmin.models import GvUserPortalOperator


class Namespaceobj(models.Model):
    class Meta:
        ordering = ['fqdn']
        verbose_name = 'FQDN Namespace'
        verbose_name_plural = 'FQDN Namespaces'

    fqdn = models.CharField(
        unique=True,
        verbose_name='Namespace',
        help_text='fully qualified domain name or domain with * for any hostname, such as "*.sso.xyz.org"',
        max_length=30)
    gvouid_parent = models.ForeignKey(
        GvUserPortalOperator,
        verbose_name='gvOuId',
        on_delete=models.PROTECT,
        help_text='OrgID des Portalbetreibers')

    def save(self, *args, **kwargs):
        self.fqdn = self.fqdn.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.fqdn)

    def org_cn(self):
        return self.gvouid_parent.gvouid.cn