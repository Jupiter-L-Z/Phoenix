import argparse,base64,hashlib,json,zipfile
from pathlib import Path
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def main():
    ap=argparse.ArgumentParser(description="Download, verify and restore Phoenix backup")
    ap.add_argument('--key-file',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--tag',default='backup-20261108-2309')
    args=ap.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    cache=out/'downloads';cache.mkdir(exist_ok=True)
    base='https://github.com/Jupiter-L-Z/Phoenix/releases/download/'+args.tag+'/'
    def download(name):
        path=cache/name
        if not path.exists():
            temp=path.with_suffix('.partial')
            with requests.get(base+name,stream=True,timeout=(30,300)) as r:
                r.raise_for_status()
                with temp.open('wb') as f:
                    for b in r.iter_content(1024*1024):f.write(b)
            temp.rename(path)
        return path
    manifest=json.loads(download('manifest.json').read_text(encoding='utf-8'))
    aes=AESGCM(base64.urlsafe_b64decode(Path(args.key_file).read_text().strip()))
    archive=out/'snapshot.zip'
    with archive.open('wb') as f:
        for part in manifest['parts']:
            blob=download(part['name']).read_bytes()
            if len(blob)!=part['bytes'] or hashlib.sha256(blob).hexdigest()!=part['sha256']:
                raise RuntimeError('Invalid download: '+part['name'])
            f.write(aes.decrypt(blob[:12],blob[12:],part['name'].encode()))
            print('Verified and decrypted',part['name'],flush=True)
    with archive.open('rb') as f:
        if hashlib.file_digest(f,'sha256').hexdigest()!=manifest['archive_sha256']:raise RuntimeError('Invalid archive hash')
    with zipfile.ZipFile(archive) as z:
        bad=z.testzip()
        if bad:raise RuntimeError('Invalid ZIP entry: '+bad)
        dest=out/'restored';dest.mkdir(exist_ok=True)
        for info in z.infolist():
            target=(dest/info.filename).resolve()
            if not target.is_relative_to(dest.resolve()):raise RuntimeError('Unsafe archive path')
        z.extractall(dest)
    print('Restored to',dest)
    print('Read backup-report.json and README before copying into your user profile.')
if __name__=='__main__':main()
