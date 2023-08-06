"""
Handle github webhooks
======================

Handles incoming requests from github when webhooks are activated. Allows for performing actions
easily on webhook events.
"""
import importlib.util
import argparse
import sys
import json
from codecs import open  # pylint: disable=W0622
from .bottle import run, post, request, abort

config = {}


@post('/<path:path>')
def handle_repo_events(path):

    print(path)
    if config['url_path'] != path:
        abort(404, "URL path not recognized")

    event = request.headers.get('X-GitHub-Event')  # pylint: disable=E1101

    module_path = config['module_path']
    module_name = '.'.join(module_path.split('/')[-1].split('.')[:-1])
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    function_name_to_call = 'on_event_' + event
    if function_name_to_call in dir(module) and callable(getattr(module, function_name_to_call)):
        return getattr(module, function_name_to_call)(request)


def main(argv=sys.argv):  # pylint: disable=W0102

    parser = argparse.ArgumentParser(description='Easy github webhooks handler')
    parser.add_argument('-c', '--config', required=True,
                        help='JSON config file containing configuration info')
    parser.add_argument(
        '-m', '--module', required=True,
        help='Python module (.py file) contain functions to execute against github events')

    args = parser.parse_args()

    print(args.config)
    print(args.module)

    c = json.load(open(args.config, encoding='utf-8'))
    config['host'] = c['host']
    config['port'] = c['port']
    config['url_path'] = c['url_path']
    config['module_path'] = args.module

    run(host=config['host'], port=config['port'], debug=True)


if '__main__' == __name__:
    main(argv=sys.argv)
