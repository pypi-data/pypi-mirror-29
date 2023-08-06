

import os
import argparse
import getpass
import base64
from configparser import ConfigParser

import boto3
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import pyperclip


def get_key_location(key_path):
    try:
        profile_name = os.environ.get('AWS_PROFILE', None)
        profile_name = 'profile {}'.format(profile_name) if profile_name else 'default'
        config_vars = {'ec2rdp_key': key_path} if key_path else {}

        config_path = os.path.expanduser('~/.aws/config')
        config_parser = ConfigParser()
        config_parser.read(config_path)

        config_key = config_parser.get(profile_name, 'ec2rdp_key', vars=config_vars)
        return config_key
    except Exception:
        raise Exception('Cannot find a key to decrypt password')


def get_ec2_data(instance_id):
    try:
        instance = boto3.resource('ec2').Instance(instance_id)
        dns_name = instance.public_dns_name
        password_data = instance.password_data()['PasswordData']
        return dns_name, password_data.strip()
    except Exception:
        raise Exception('Unable to contact to instance {}'.format(instance_id))


def decrypt_password_data(key_file, key_password, password_data):
    try:
        with open(os.path.expanduser(key_file)) as f:
            key_data = RSA.importKey(f.read(), key_password)

        cipher = PKCS1_v1_5.new(key_data)
        password = cipher.decrypt(base64.b64decode(password_data), None)
        return password
    except Exception:
        raise Exception('Error decrypting instance password.')


def get_output(output, instance_id):
    try:
        if not output:
            output = os.path.join(os.getcwd(), '{}.rdp'.format(instance_id))

        output = os.path.expanduser(output)
        if not os.path.exists(os.path.dirname(output)):
            os.makedirs(os.path.dirname(output))
        return output
    except Exception:
        raise Exception('Error trying to get output directory.')


def write_rdp(output, dns_name):

    content = [
        'auto connect:i:1\n',
        'full address:s:{}\n'.format(dns_name),
        'username:s:Administrator\n',
        'redirectclipboard:i:1\n',
        'prompt for credentials on client:i:1\n'
    ]

    try:
        with open(output, 'w') as f:
            f.writelines(content)
    except Exception:
        raise Exception('Error writing rdp file.')


def password_to_clipboard(password):
    try:
        pyperclip.copy(password)
    except Exception:
        raise Exception('Error copying password to clipboard.')


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--output', help='The path for the rdp file to be created.',
                        action='store', type=str, default=None)
    parser.add_argument('-k', '--key', help='The path to the private key file to decrypt the password.',
                        action='store', type=str, default=None)
    parser.add_argument('-q', '--quick', help='The script will not ask for the passphrase for the key file.',
                        action='store_true', default=False)

    parser.add_argument('--aws-profile', help='The profile name for aws credentials',
                        action='store', type=str, default=None)
    parser.add_argument('--aws-access-key-id', help='The access key id for aws',
                        action='store', type=str, default=None,)
    parser.add_argument('--aws-secret-access-key', help='The secret access key for aws',
                        action='store', type=str, default=None)
    parser.add_argument('--aws-region', help='The region for aws',
                        action='store', type=str, default=None)
    parser.add_argument('instance_id', help='The instance-id to decrypt the password.',
                        action='store', type=str, default=None)

    args = parser.parse_args()

    if args.aws_profile is not None:
        os.environ['AWS_PROFILE'] = args.aws_profile

    if args.aws_region is not None:
        os.environ['AWS_DEFAULT_REGION'] = args.aws_region

    if args.aws_access_key_id is not None and args.aws_secret_access_key is not None:
        os.environ['AWS_ACCESS_KEY_ID'] = args.aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = args.aws_secret_access_key

    try:
        output = get_output(args.output, args.instance_id)
        dns_name, password_data = get_ec2_data(args.instance_id)
        key_path = get_key_location(args.key)

        key_password = getpass.getpass('Password for key file {} (leave blank if none):'.format(key_path)) \
            if not args.quick else ''

        password = decrypt_password_data(key_path, key_password, password_data)
        write_rdp(output, dns_name)
        password_to_clipboard(password)
        print('RDP file written to: {}'.format(output))
        print('Password copied to clipboard')

    except Exception as e:
        print(str(e))
        exit(1)
