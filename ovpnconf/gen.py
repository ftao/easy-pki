#!/usr/bin/env python
'''
ovpnconf-gen - OpenVPN Config Generator

usage:
  ovpnconf-gen (server|client) <name> [(--var=<VAR>)...] [--vars-file=<VARS_FILE>]

options:
  --var=<VAR>                      Key=Value style variables
  --vars-file=<VARS_FILE>          Load options from this file

'''

import docopt
import jinja2
import os
import yaml

here = os.path.dirname(__file__)
client_defaults_file = os.path.join(here, 'defaults/client.yml')
server_defaults_file = os.path.join(here, 'defaults/client.yml')
client_template_file = os.path.join(here, 'templates/client.conf')
smart_route_file = os.path.join(here, 'templates/smart_route.txt')


def parse_cmdline_vars(cmdline_vars):
    return dict(var.split('=', 1) for var in cmdline_vars)

def load_vars(vars_file):
    with open(vars_file, 'r') as fp:
        return yaml.load(fp)


def expand_file_path(context):

    if 'name' not in context or 'pki_root' not in context:
        return 
    name = context['name']
    pki_root = context['pki_root']

    update = {
        'ca_file' : os.path.join(pki_root, 'ca.crt'),
        'key_file' : os.path.join(pki_root, 'private', name + '.key'),
        'cert_file' : os.path.join(pki_root, 'issued', name + '.crt')
    }
    for k,v in update.items():
        if k not in context:
            context[k] = v

def expand_file_contents(context):

    def read_part(fp, start_pattern, end_pattern):
        lines = fp.readlines()
        start_index = 0
        end_index = -1
        for i, line in enumerate(lines):
            if start_pattern in line:
                start_index = i
            if end_pattern in line:
                end_index = i + 1
                break
        return "".join(lines[start_index:end_index])

    def read_cert(fp):
        return read_part(
            fp, 
            '-----BEGIN CERTIFICATE-----',
            '-----END CERTIFICATE-----'
        )

    def read_key(fp):
        return read_part(
            fp, 
            '-----BEGIN PRIVATE KEY-----',
            '-----END PRIVATE KEY-----'
        )

    for ftype in ['ca', 'key', 'cert']:
        if ftype + '_file' in context:
            with open(context[ftype + '_file'], 'r') as fp:
                if ftype == 'key':
                    context[ftype + '_content'] = read_key(fp)
                else:
                    context[ftype + '_content'] = read_cert(fp)

    if context.get('route_mode') == 'smart':
        with open(smart_route_file, 'r') as fp:
            context['smart_route_content'] = fp.read()

def main():
    args = docopt.docopt(__doc__)
    name = args.get('<name>')

    context = {}
    if args.get('client'):
        context.update(load_vars(client_defaults_file))
    elif args.get('server'):
        context.update(load_vars(server_defaults_file))

    if args.get('--vars-file'):
        context.update(load_vars(args.get('--vars-file')))

    context.update(parse_cmdline_vars(args.get('--var')))

    context['name'] = name

    expand_file_path(context)
    expand_file_contents(context)

    env = jinja2.Environment(undefined=jinja2.StrictUndefined)
    template_str = open(client_template_file).read()
    template = env.from_string(template_str)
    print template.render(context)

if __name__ == "__main__":
    main()
