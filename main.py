import time
import requests
import json
import sys
from src.Osintgram import Osintgram
import argparse

def printlogo():
    # ваш код printlogo

def cmdlist():
    # ваш код cmdlist

def signal_handler(sig, frame):
    # ваш код signal_handler

parser = argparse.ArgumentParser(description='Osintgram is a OSINT tool on Instagram.')
parser.add_argument('id', type=str, help='username')
parser.add_argument('password', type=str, help='password')
parser.add_argument('-C','--cookies', help='clear\'s previous cookies', action="store_true")
parser.add_argument('-j', '--json', help='save commands output as JSON file', action='store_true')
parser.add_argument('-f', '--file', help='save output in a file', action='store_true')
parser.add_argument('-c', '--command', help='run in single command mode & execute provided command', action='store')
parser.add_argument('-o', '--output', help='where to store photos', action='store')

args = parser.parse_args()

def login_with_two_factor(session, username, password):
    headers = {
        'User-Agent': 'Instagram 10.26.0 Android'
    }

    data = {
        'username': username,
        'password': password,
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    login_response = session.post('https://i.instagram.com/api/v1/accounts/login/', data=data, headers=headers)

    if login_response.status_code == 200:
        print('Logged in successfully without 2FA')
        return True

    login_response_json = login_response.json()

    if 'two_factor_required' in login_response_json:
        print('Two-factor authentication is required')
        two_factor_identifier = login_response_json['two_factor_info']['two_factor_identifier']

        verification_code = input('Enter the two-factor authentication code: ')

        two_factor_data = {
            'username': username,
            'verification_code': verification_code,
            'two_factor_identifier': two_factor_identifier,
            'trust_this_device': '1',
            'queryParams': {}
        }

        two_factor_response = session.post('https://i.instagram.com/api/v1/accounts/two_factor_login/', data=two_factor_data, headers=headers)

        if two_factor_response.status_code == 200:
            print('Logged in successfully with 2FA')
            return True
        else:
            print('Failed to log in with 2FA')
            return False
    else:
        print(f'Failed to log in. Status code: {login_response.status_code}')
        return False

session = requests.Session()

if login_with_two_factor(session, args.id, args.password):
    api = Osintgram(args.id, args.file, args.json, args.command, args.output, args.cookies)
    # Ваш следущий код

    commands = {
        'list':             cmdlist,
        'help':             cmdlist,
        'quit':             sys.exit,
        'exit':             sys.exit,
        'addrs':            api.get_addrs,
        'cache':            api.clear_cache,
        'captions':         api.get_captions,
        "commentdata":      api.get_comment_data,
        'comments':         api.get_total_comments,
        'followers':        api.get_followers,
        'followings':       api.get_followings,
        'fwersemail':       api.get_fwersemail,
        'fwingsemail':      api.get_fwingsemail,
        'fwersnumber':      api.get_fwersnumber,
        'fwingsnumber':     api.get_fwingsnumber,
        'hashtags':         api.get_hashtags,
        'info':             api.get_user_info,
        'likes':            api.get_total_likes,
        'mediatype':        api.get_media_type,
        'photodes':         api.get_photo_description,
        'photos':           api.get_user_photo,
        'propic':           api.get_user_propic,
        'stories':          api.get_user_stories,
        'tagged':           api.get_people_tagged_by_user,
        'target':           api.change_target,
        'wcommented':       api.get_people_who_commented,
        'wtagged':          api.get_people_who_tagged
    }

    if not args.command:
        printlogo()

    while True:
        if args.command:
            cmd = args.command
            _cmd = commands.get(args.command)
        else:
            signal.signal(signal.SIGINT, signal_handler)
            pc.printout("Run a command: ", pc.YELLOW)
            cmd = input()

            _cmd = commands.get(cmd)

        if _cmd:
            _cmd()
        elif cmd == "FILE=y":
            api.set_write_file(True)
        elif cmd == "FILE=n":
            api.set_write_file(False)
        elif cmd == "JSON=y":
            api.set_json_dump(True)
        elif cmd == "JSON=n":
            api.set_json_dump(False)
        elif cmd == "":
            print("")
        else:
            pc.printout("Unknown command\n", pc.RED)

        if args.command:
            break
else:
    print("Login failed")
