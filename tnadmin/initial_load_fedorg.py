import datetime
import json
import pathlib
import os
import sys

import django

if __name__ != '__main__':
    sys.exit(1)

projhome = pathlib.Path('sys.argv[0]').parent.parent.parent
sys.path.append(projhome)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
django.setup()

#from ldapgvat.models import GvUserPortal as LdapUserPortal
import ldapgvat.models
from tnadmin.models.constants import *
from tnadmin.models.get_defaults import *
from tnadmin.models.gvfederationorg import *
from tnadmin.models.gvorg import *
import tnadmin.models.gvorg

class InitialLoadFedOrg:
    def main(self):
        self.exit_code = 0
        self.load_PVV_org()
        self.load_STP_DL_org()
        self.load_PV_ZUGRIFF_org()
        sys.exit(self.exit_code)

    def load_PVV_org(self):
        fedorg_pvv = pathlib.Path(sys.argv[0]).parent / 'tests' / 'data' / 'fedorg_pvv.json'
        print(f'loading FederationOrg/PVV from {fedorg_pvv}')
        with fedorg_pvv.open() as fd:
            org_pvv = json.load(fd)
            for vkz in org_pvv:
                gvorg = self.get_gvorg_by_vkz(vkz)
                if gvorg:
                    fedorg = GvFederationOrg(gvouid=gvorg)
                    fedorg.gvContractStatus = LEGAL_BASIS_PVV
                    fedorg.gvSource = str(datetime.datetime.now()) + ' initial_load_fedorg'
                    try:
                        fedorg.save()
                    except Exception as e:
                        if not str(e).startswith('duplicate key'):
                            raise
            pass

    def load_STP_DL_org(self):
        fedorg_stp_dl = pathlib.Path(sys.argv[0]).parent / 'tests' / 'data' / 'fedorg_stp_dl.json'
        print(f'loading FederationOrg/STP-DL from {fedorg_stp_dl}')
        with fedorg_stp_dl.open() as fd:
            org_stp_dl = json.load(fd)
            for (ouid, cn) in org_stp_dl.items():
                gvorg = self.get_gvorg_by_ouid(ouid, cn)
                if gvorg:
                    fedorg = GvFederationOrg(gvouid=gvorg)
                    fedorg.gvContractStatus = LEGAL_BASIS_PROCESSOR_IDP
                    fedorg.gvSource = str(datetime.datetime.now()) + ' initial_load_fedorg'
                    try:
                        fedorg.save()
                    except Exception as e:
                        if not str(e).startswith('duplicate key'):
                            raise

    def load_PV_ZUGRIFF_org(self):
        for userportal in ldapgvat.models.GvUserPortal.objects.all():
            if 'gvuserportal' in [oc.lower() for oc in userportal.object_classes] and \
                userportal.gvParticipants:
                print(f'{len(userportal.gvParticipants)} participant(s) declared in "{userportal.cn}"')
                for ouid in userportal.gvParticipants:
                    gvorg = self.get_gvorg_by_ouid(ouid, '')
                    if gvorg:
                        fedorg_new = GvFederationOrg(gvouid=gvorg)
                        fedorg_new.gvouid_aufsicht_id = get_default_org()
                        fedorg_new.gvouid_dl_id = get_default_org()
                        fedorg_new.gvContractStatus = LEGAL_BASIS_ENTITLED_ORG
                        if not self.is_already_on_db_or_pvv(fedorg_new):
                            fedorg_new.gvSource = str(datetime.datetime.now()) + ' initial_load_fedorg'
                            fedorg_new.save()
                    else:
                        print(f'participant {ouid} registered in {userportal.dn} not found in gvOrganisation', file=sys.stderr)

    def is_already_on_db_or_pvv(self, new: GvFederationOrg):
        try:
            GvFederationOrg.objects.get(gvouid_id=new.gvouid_id,
                                        gvouid_aufsicht_id=new.gvouid_aufsicht_id,
                                        gvouid_dl_id = new.gvouid_dl_id,
                                        gvContractStatus = new.gvContractStatus)
            return True
        except Exception:
            pass
        try:
            GvFederationOrg.objects.get(gvouid_id=new.gvouid_id,
                                        gvouid_aufsicht_id=new.gvouid_aufsicht_id,
                                        gvouid_dl_id=new.gvouid_dl_id,
                                        gvContractStatus=LEGAL_BASIS_PVV)
            return True
        except Exception:
            return False

    def get_gvorg_by_ouid(self, ouid: str, cn: str) -> GvOrganisation:
        try:
            gvorg = GvOrganisation.objects.get(gvouid=ouid)
            return gvorg
        except tnadmin.models.gvorg.GvOrganisation.DoesNotExist:
            print(f"gvOrganisation '{cn}' not found via gvOuId='{ouid}'", file=sys.stderr)
            #self.exit_code = 1  # do not stop loading on inconsistent data
            return None


    def get_gvorg_by_vkz(self, vkz: str) -> GvOrganisation:
        try:
            gvorg = GvOrganisation.objects.get(gvouvkz=vkz)
            return gvorg
        except tnadmin.models.gvorg.GvOrganisation.DoesNotExist:
            print(f"gvOrganisation not found via gvOuVKZ='{vkz}'", file=sys.stderr)
            self.exit_code = 1
        return None


InitialLoadFedOrg().main()
