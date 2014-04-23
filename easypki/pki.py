'''
PKI 
'''
import os
import subprocess

class EasyRSAPKI(object):
    '''
    An Easy-RSA Based PKI Backend
    '''
    def __init__(self, pki_dir, easyrsa_dir):
        self.pki_dir = pki_dir
        self.env = {
            'EASYRSA' : easyrsa_dir,
            'EASYRSA_PKI' : self.pki_dir,
            'EASYRSA_DN' : 'cn_only',
            'EASYRSA_BATCH' : "1",
        }
        self.EASYRSA_BIN = os.path.join(self.env['EASYRSA'], 'easyrsa')
        self._check()

    def _check(self):
        if not os.path.exists(self.EASYRSA_BIN):
            raise Exception("%s does not exists" %self.EASYRSA_BIN)

    def init_pki(self):
        subprocess.call([self.EASYRSA_BIN, "init-pki"], env=self.env)

    def build_ca(self, cname=None):
        env = self.env.copy()
        if cname is not None:
            env.update({'EASYRSA_REQ_CN' : cname})
        subprocess.call([self.EASYRSA_BIN, "build-ca", 'nopass'], env=env)

    def gen_key(self, type_, cname):
        env = self.env.copy()
        if cname is not None:
            env.update({'EASYRSA_REQ_CN' : cname})
        #make it  safe for filename 
        filename = cname
        subprocess.call([self.EASYRSA_BIN, "gen-req", filename, 'nopass'], env=env)
        subprocess.call([self.EASYRSA_BIN, "sign-req", type_, filename], env=env)

    def gen_dh(self):
        env = self.env.copy()
        subprocess.call([self.EASYRSA_BIN, "gen-dh"], env=env)

def get_pki(pki_dir, easyrsa_dir=None):
    if easyrsa_dir is None:
        easyrsa_dir = os.environ.get("EASYRSA", None)
    if easyrsa_dir is None:
        raise Exception("can not locate EASYRSA tool, consider set environment variable EASYRSA")
    return EasyRSAPKI(pki_dir, easyrsa_dir)
