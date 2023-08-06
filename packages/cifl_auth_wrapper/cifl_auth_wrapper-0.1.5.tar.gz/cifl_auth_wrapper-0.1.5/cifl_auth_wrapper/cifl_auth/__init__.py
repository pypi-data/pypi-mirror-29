#!/usr/bin/python
from google_auth_oauthlib import flow
from apiclient import discovery

import pickle
import json
import os
import logging
import sys
import argparse

home_dir = os.getcwd()

# auth_dir = os.path.join(os.path.dirname(os.path.realpath(os.path.realpath(home_dir))), 'run-google-auth')
auth_dir = os.path.join(os.path.expanduser('~'), 'run-google-auth')


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schema(entity):
    from singer import utils
    return utils.load_json(get_abs_path(home_dir + "/config/schemas/{}.json".format(entity)))


def load_params(entity):
    from singer import utils
    return utils.load_json(get_abs_path(home_dir + "/config/params/{}.json".format(entity)))


def load_targets(entity):
    from singer import utils
    return utils.load_json(get_abs_path(home_dir + "/config/targets/{}.json".format(entity)))


def error_logger():
    logger = logging.getLogger('custom-logger')
    handler = logging.FileHandler(os.getcwd() + '/logs/errors.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.CRITICAL)
    return logger


def exit_error(e):
    print('An Error Occurred')
    print (e)
    sys.exit()

auth_config_path = os.path.join(home_dir, 'config', 'auth_config.json')

try:
    auth_config = json.load(open(auth_config_path))
except Exception as e:
    auth_config = {"config": {
                            "scopes": [
                                "https://www.googleapis.com/auth/analytics.readonly",
                                "https://www.googleapis.com/auth/webmasters.readonly",
                                "https://www.googleapis.com/auth/spreadsheets",
                                "https://www.googleapis.com/auth/adsense",
                                "https://www.googleapis.com/auth/bigquery",
                                "https://www.googleapis.com/auth/cloud-platform"
                            ],
                            "client_secret_file_name": "client_secrets.json",
                            "application_name": "CIFL Google Authentication Module",
                            "launch_browser": "True"
                        }
                    }

SCOPES = auth_config['config']['scopes']
CLIENT_SECRET_FILE = os.path.join(home_dir, auth_config['config']['client_secret_file_name'])
APPLICATION_NAME = auth_config['config']['application_name']
LAUNCH_LOCAL_BROWSER = auth_config['config']['launch_browser']


def get_auth():
    # parser = argparse.ArgumentParser(
    #     formatter_class=argparse.RawDescriptionHelpFormatter,
    #     parents=[tools.argparser])
    #
    # flags = parser.parse_args([])

    credential_dir = os.path.join(auth_dir, '.credentials')

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "google_api_auth_tokens.pickle")

    try:
        credentials = pickle.load(open(credential_path, "rb"))
    except Exception as e:
        pickle.dump(None, open(credential_path, "wb"))
        credentials = pickle.load(open(credential_path, "rb"))

    if not credentials or not credentials.valid:
        appflow = flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        appflow.user_agent = APPLICATION_NAME

        if LAUNCH_LOCAL_BROWSER == 'True':
            appflow.run_local_server()
        else:
            appflow.run_console()

        credentials = appflow.credentials

        pickle.dump(credentials, open(credential_path, "wb"))

        print('Storing credentials to ' + credential_path)
        print("Oauth Flow Complete, credentials successfully generated")
        return None
    return credentials


def get_auth_access_token():
    is_valid_auth = get_auth()
    if is_valid_auth is not None:
        return is_valid_auth.token
    else:
        return None


def get_service(API_NAME, API_VERSION):

    try:
        credentials = get_auth()
    except Exception as e:
        logger = cifl_auth.error_logger()
        logger.error(e)
        exit_error("Please run the auth flow")

    if credentials != None:
        # Build the service object.
        return discovery.build(API_NAME, API_VERSION, credentials=credentials)
    else:
        return None
