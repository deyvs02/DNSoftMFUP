#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import hashlib
import os
import sys
from mediafire import MediaFireApi
from mediafire.client import MediaFireClient

def main(argv):
    vnumber = "0.3"
    print('mfcmd.py v' + vnumber, file=sys.stderr)

    account = ''
    passphrase = ''
    filepath = ''
    filepathbase = ''
    localhash = ''
    uldir = 'DNSoftUpload'  # Definindo o subdiretório padrão

    try:
        opts, args = getopt.getopt(argv, "e:p:u:h:f:", ["email=", "password=", "upload-folder=", "hash=", "file="])
    except getopt.GetoptError:
        print('Error!', file=sys.stderr)
        return

    for opt, arg in opts:
        if opt in ("-e", "--email"):
            account = arg
        elif opt in ("-p", "--password"):
            passphrase = arg
        elif opt in ("-u", "--upload-folder"):
            uldir = arg
        elif opt in ("-h", "--hash"):
            localhash = arg
        elif opt in ("-f", "--file"):
            filepath = arg

    if not account or not passphrase or not filepath:
        print('Error: Missing credentials or file path', file=sys.stderr)
        return

    if not os.path.isfile(filepath):
        print('Error: File does not exist', file=sys.stderr)
        return

    filepathbase = os.path.basename(filepath)
    print('Filepath:', filepath, file=sys.stderr)
    print('Filename:', filepathbase, file=sys.stderr)

    if not localhash:
        print('No SHA-256 specified: calculating...', file=sys.stderr)
        localhash = calculate_sha256(filepath)
    print('Checksum:', localhash, file=sys.stderr)

    api = MediaFireApi()

    try:
        session = api.user_get_session_token(
            email=account,
            password=passphrase,
            app_id='42511'
        )
        print('MediaFire API: connected', file=sys.stderr)
        api.session = session
    except Exception as e:
        print(f'Error: login failed - {e}', file=sys.stderr)
        return

    try:
        userinfo = api.user_get_info()
        print("Account holder:", userinfo['user_info']['display_name'], file=sys.stderr)
        maxstore = userinfo['user_info']['storage_limit']
        usedstore = userinfo['user_info']['used_storage_size']
        freestore = int(maxstore) - int(usedstore)
        print("Maximum storage:", maxstore, file=sys.stderr)
        print("Used storage:", usedstore, file=sys.stderr)
        print("Free storage:", freestore, file=sys.stderr)
        localsize = os.path.getsize(filepath)
        if freestore <= localsize:
            print("Error: available space will not suffice!", file=sys.stderr)
            return
        else:
            print("Available filespace will suffice", file=sys.stderr)
    except Exception as e:
        print(f'Error getting or parsing user info: {e}', file=sys.stderr)
        return

    client = MediaFireClient()

    try:
        client.login(email=account, password=passphrase, app_id='42511')
        print('MediaFire Client: logged in', file=sys.stderr)
    except Exception as e:
        print(f'Error: client login failed - {e}', file=sys.stderr)
        return

    try:
        client.get_resource_by_path("/" + uldir + "/")
        print('Detected upload folder ./' + uldir, file=sys.stderr)
    except:
        print('Upload folder ./' + uldir + ' does not exist, creating it.', file=sys.stderr)
        try:
            client.create_folder("mf:/" + uldir)
        except Exception as e:
            print(f'Could not create upload folder: {e}', file=sys.stderr)
            uldir = ''

    try:
        # Tratamento do nome de arquivo para garantir compatibilidade
        safe_filename = filepathbase.replace(" ", "_")  # Substitui espaços por underscores
        print(f'Uploading file "{safe_filename}" to mf:/{uldir}/', file=sys.stderr)
        client.upload_file(filepath, "mf:/" + uldir + "/" + safe_filename)
        print('File uploaded successfully!', file=sys.stderr)
    except Exception as e:
        print(f'Error: upload function failed - {e}', file=sys.stderr)
        return

    try:
        fileinfo = client.get_resource_by_path("/" + (uldir + "/" if uldir else "") + safe_filename)
        dlurl = fileinfo['links']['normal_download']
        dlurl = dlurl.replace('http://www.', 'https://')
        save_to_file(dlurl, "link.txt")
        print('Download link:', dlurl)
    except Exception as e:
        print(f'Error: retrieving file info after upload - {e}', file=sys.stderr)
        return

    print("Done.", file=sys.stderr)

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def save_to_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content + '\n')

if __name__ == "__main__":
    main(sys.argv[1:])
