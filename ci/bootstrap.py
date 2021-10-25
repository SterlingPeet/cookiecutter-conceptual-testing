#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from pathlib import Path
from os import unlink
import sys


this_path = Path(__file__).resolve()
repo_path = Path(*this_path.parts[:-2])


parser = argparse.ArgumentParser(
    description='Bootstrap script for generating CI matrix testing configuration.')
parser.add_argument('--no-env', action='store_true',
                    help='Execute in local context rather than venv')


def main():
    import jinja2
    import matrix
    import yaml

    jinja = jinja2.Environment(
        loader=jinja2.FileSystemLoader(repo_path.joinpath('ci', 'templates')),
        trim_blocks=True,
        lstrip_blocks=True)
    # keep_trailing_newlines=True)

    # Remove old env configurations
    tox_envs = {}
    for old_env in repo_path.joinpath('ci', 'envs').iterdir():
        unlink(old_env)

    # Make new cookiecutterrc for each env
    for (alias, conf) in matrix.from_file(repo_path.joinpath('ci', 'setup.cfg')).items():
        tox_envs[alias] = conf
        conf['slug'] = 'TestProject'
        # path_to_dep = conf['deployment_path']
        # if path_to_dep == '' or path_to_dep == '.':
        #     conf['deployment_path_to_project_root'] = '..'
        # else:
        #     conf['deployment_path_to_project_root'] = '/'.join(['..' for k in path_to_dep.split('/')])
        # print(conf['deployment_path_to_project_root'])
        with open(repo_path.joinpath('ci', 'envs', alias + '.cookiecutterrc'), 'w') as fh:
            fh.write(yaml.safe_dump(
                dict(default_context={k: v for k, v in conf.items() if v}),
                default_flow_style=False
            ))

    # Constitute templates from bootstrapped configuration
    for templ in repo_path.joinpath('ci', 'templates').iterdir():
        with open(repo_path.joinpath(templ.name), 'w') as fh:
            fh.write(jinja.get_template(templ.name).render(
                tox_environments=tox_envs))
        print('Generated {}'.format(templ.name))
    print('Done.')


if __name__ == "__main__":
    args = sys.argv[1:]
    args = parser.parse_args(args=args)
    if args.no_env:
        main()
    else:
        exit(1)
