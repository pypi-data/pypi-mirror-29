"""
Handle github webhooks
======================

Handles incoming requests from github when webhooks are activated. Allows for performing actions
easily on webhook events.
"""

import subprocess
import logging
import os.path

REPO_FOLDER = '/root/tf-frontend'
WEBROOT = '/var/www/html'


def get_configured_logger(name, filename):
    l = logging.getLogger(name)

    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(formatter)

    l.addHandler(console_handler)
    l.addHandler(file_handler)

    l.setLevel(logging.DEBUG)

    return l

log = get_configured_logger(
    __name__,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'github_webhook.log'))


def pull_code(repo_path):
    log.info("Pulling latest code...")
    try:
        subprocess.run("cd /root/tf-frontend; git pull origin master", shell=True, check=True)
    except subprocess.CalledProcessError as exp:
        log.error("Error pulling updates, aborting :-(")
        log.error(exp)
        return False
    else:
        log.info("Done!")

    return True


def deploy_to_web(repo_path, web_path):
    log.info("Copying to web root: %s", web_path)
    try:
        subprocess.run("cd {}/dist/; cp -r * {}/".format(repo_path, web_path), shell=True, check=True)
    except subprocess.CalledProcessError as exp:
        log.error("Error copying to web root, aborting :-(")
        log.error(exp)
        return False
    else:
        log.info("Done!")

    return True


def on_event_ping(request):
    log.info("Got ping event")


def on_event_push(request):

    branch = request.json.get('ref').split('/')[-1]

    if 'master' == branch:
        log.info("changes pushed to master branch")

        pusher = request.json.get('pusher')
        log.info("Pushed by %s (%s)", pusher['name'], pusher['email'])

        hc = request.json.get('head_commit')
        log.info("Head commit: %s", hc['id'])
        log.info("  By: %s (%s)", hc['committer']['name'], hc['committer']['email'])
        log.info("  on: %s", hc['timestamp'])
        log.info("  %s", hc['message'])

        pull_code(REPO_FOLDER)
        deploy_to_web(REPO_FOLDER, WEBROOT)
