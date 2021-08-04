import json
import pathlib
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def main(args):
    for url in args:
        cataloger = UbuntuVagrantBoxCataloger(url)
        catalog = cataloger.build_catalog()
        print(json.dumps(catalog, indent=4))


class UbuntuVagrantBoxCataloger(object):
    def __init__(self, url):
        self.url = url

    def _get_sha256sum_and_box_name(self, sha256sums_url):
        sha256sums_reponse = requests.get(sha256sums_url)
        content = sha256sums_reponse.content.decode('utf-8')
        lines = content.split('\n')
        for line in lines:
            sha256sum, name = line.split()
            if name.endswith('vagrant.box'):
                break
        name = name.strip('*')  # why is there a * in the name?
        return sha256sum, name

    def build_catalog(self):
        path = pathlib.Path(self.url)
        catalog_name = path.parts[-1]
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('a')
        releases = []
        for link in links:
            href = link['href']
            if not href.startswith('release-'):
                continue
            _, version = href.strip('/').split('-')
            release_url = urljoin(self.url, href)
            sha256sums_url = urljoin(release_url, 'SHA256SUMS')
            sha256sum, name = self._get_sha256sum_and_box_name(sha256sums_url)
            box_url = urljoin(release_url, name)
            releases.append([version, sha256sum, box_url])

        metadata = dict(
            name = f'ubuntu-{catalog_name}',
            description = f'Box images direct from {self.url}',
            versions = [
                dict(
                    version=version,
                    providers=[dict(
                        name='virtualbox',
                        url=url,
                        checksum_type='sha256',
                        checksum=digest,
                    )],
                )
                for version, digest, url in releases
            ]
        )
        return metadata


if __name__ == '__main__':
    main(sys.argv[1:])
