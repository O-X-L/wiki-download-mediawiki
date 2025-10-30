#!/usr/bin/env python3

# https://www.mediawiki.org/wiki/API:Lists
# https://www.mediawiki.org/wiki/API:Allpages

from time import sleep
from pathlib import Path
from argparse import ArgumentParser
from json import dumps as json_dumps

from requests import get as http_get

MAX_RETRIES = 2
MAX_PAGES = 10_000  # this script was not designed for huge wiki's
WAIT_TIME = 0.5  # we do not want to DOS the service
headers = {'User-Agent': 'MediaWiki Downloader'}


def _api(params: dict) -> dict:
    sleep(WAIT_TIME)
    print(' =>', params)
    params['format'] = 'json'
    retry = 0
    while retry < MAX_RETRIES:
        try:
            return http_get(
                url=API_URL,
                headers=headers,
                params=params,
                timeout=5,
            ).json()

        except ConnectionError:
            retry += 1

    raise ConnectionError()


def _dl_page(ns_id: str, page_id: int, page_title: str):
    page_id = str(page_id)

    ns_dir = Path(out_dir / ns_id)
    ns_dir.mkdir(exist_ok=True)
    file = ns_dir / f'{page_id}.mw'
    if file.is_file() and not args.replace:
        print(f' => {ns_id}:{page_id} Skipping Update')
        return

    res = _api({
        'action': 'query',
        'prop': 'revisions',
        'rvprop': 'content',
        'rvslots': 'main',
        'pageids': page_id,
        'rvlimit': '1',
    })['query']['pages'][page_id]

    latest_revision = res['revisions'][0]
    content = latest_revision['slots']['main']['*']

    with open(file, 'w', encoding='utf-8') as f:
        f.write(f'# {page_title}' + '\n\n')
        f.write(content)


def main():
    test = http_get(API_URL)
    if test.content.find(b'MediaWiki API') == -1:
        raise ValueError('URL does not seem to be a MediaWiki API')

    namespaces = _api({
        'action': 'query',
        'meta': 'siteinfo',
        'siprop': 'namespaces',
    })['query']['namespaces']

    print("NAMESPACES:", list(namespaces))

    print('\n### QUERYING PAGES ###')
    count = 0
    ns_pages = {}
    for ns_id in namespaces:
        apcontinue = None
        pages = {}

        while True:
            params = {
                'action': 'query',
                'list': 'allpages',
                'apnamespace': ns_id,
                'aplimit': 500,
            }
            if apcontinue:
                params['apcontinue'] = apcontinue

            res = _api(params)

            if 'query' in res:
                for page in res['query']['allpages']:
                    count += 1
                    pages[page['pageid']] = page['title']

            else:
                print('Error fetching pages:', res)
                break

            if 'continue' in res and 'apcontinue' in res['continue']:
                apcontinue = res['continue']['apcontinue']

            else:
                break

        ns_pages[ns_id] = pages
        if count > MAX_PAGES:
            raise  OverflowError('ERROR: THIS SCRIPT WAS NOT DESIGNED TO HANDLE HUGE WIKIs!')

    with open(out_dir / 'overview.json', 'w', encoding='utf-8') as f:
        f.write(json_dumps(ns_pages, indent=2))

    print('\n### DOWNLOADING PAGES ###')
    for ns_id, pages in ns_pages.items():
        for page_id, page_title in pages.items():
            _dl_page(ns_id=ns_id, page_id=page_id, page_title=page_title)


if __name__ == '__main__':
    out_dir_default = Path(__file__).parent / 'dump'
    parser = ArgumentParser(prog='MediaWiki Download Script (© OXL IT Services, License: MIT)')
    parser.add_argument('-u', '--url', help='Base-URL of the MediaWiki instance', required=True)
    parser.add_argument('-o', '--out-dir', default=out_dir_default)
    parser.add_argument('-r', '--replace', help='Replace/Update existing pages', default=False)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(exist_ok=True)

    API_URL = f"{args.url}/api.php"

    main()
