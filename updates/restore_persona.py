"""Restore the encrypted personality update with the existing Phoenix recovery key."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key-file', required=True)
    parser.add_argument('--dsh-home', required=True, help='Restored dsh-home folder or live .dsh folder')
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent
    manifest = json.loads((folder / 'doujiang-persona-20261114.json').read_text(encoding='utf-8'))
    blob = (folder / manifest['file']).read_bytes()
    if hashlib.sha256(blob).hexdigest() != manifest['sha256']:
        raise ValueError('Encrypted file hash mismatch')
    key = base64.urlsafe_b64decode(Path(args.key_file).read_text(encoding='utf-8-sig').strip())
    plain = AESGCM(key).decrypt(blob[:12], blob[12:], manifest['aad'].encode())
    if hashlib.sha256(plain).hexdigest() != manifest['plaintext_sha256']:
        raise ValueError('Personality hash mismatch')
    target = Path(args.dsh_home) / 'plugins-data' / 'aurabot' / 'personas' / 'dafeiyu.md'
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        backup = target.with_name(target.name + '.before-20261114-update.bak')
        with backup.open('xb') as stream:
            stream.write(target.read_bytes())
    target.write_bytes(plain)
    print('Restored personality:', target)


if __name__ == '__main__':
    main()
