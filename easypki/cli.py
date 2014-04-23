#!/usr/bin/env python
'''
easypki - Easy PKI Management Tool
usage:
  easypki init-ca [<cname>] [options]
  easypki gen-key (server|client) <cname> [options]
  easypki gen-dh  [options]

options:
  --pki-dir=<PKI-DIR>          PKI Directory

'''

import docopt
import os
from easypki.pki import get_pki

def main():
    args = docopt.docopt(__doc__)
    default_pki_dir = os.path.join(os.getcwd(), 'pki')
    pki_dir = args.get("--pki-dir") or default_pki_dir
    pki = get_pki(pki_dir)
    cname = args.get('<cname>')
    if args.get("init-ca"):
        pki.init_pki()
        pki.build_ca(cname)
    elif args.get("gen-key"):
        cname = args.get('<cname>')
        type_ = "server" if args.get('server') else "client"
        pki.gen_key(type_, cname)
    elif args.get("gen-dh"):
        pki.gen_dh()


if __name__ == "__main__":
    main()
