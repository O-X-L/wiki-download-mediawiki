# MediaWiki Download Script

This is a very simple script to download the whole contents of MediaWiki instance via its [API]().

This script should not be used to download huge Wiki's as it will not scale well!

----

## Features

* Downloading the content of all pages in their source-format

We did not yet have the need to also download the images. Feel free to open a PR!

----

## Usage

Dependencies:
```bash
pip install requests
```

Arguments:
```bash
python3 main.py --help
> usage: MediaWiki Download Script (© OXL IT Services, License: MIT)
>        [-h] -u URL [-o OUT_DIR] [-r REPLACE]
> 
> options:
>   -h, --help            show this help message and exit
>   -u URL, --url URL     Base-URL of the MediaWiki instance
>   -o OUT_DIR, --out-dir OUT_DIR
>   -r REPLACE, --replace REPLACE
>                         Replace/Update existing pages
```

----

## Result

**Overview: dump/overview.json**

```bash
# namespace-id => page-id => page-title
cat dump/overview.json 
> {
>   "0": {
>     "1": "Page Title"
>   },
>   "15": {}
> }
```

**Files: dump/<namespace-id>/<page-id>.mw**

```bash
tree dump/
> dump/
> ├── 0
> │   ├── 1.mw
```

**Content**

```bash
head dump/0/1.mw 
> # Main Page
> Welcome to the ''nftables'' HOWTO documentation page. Here you will find documentation on how to build, install, configure and use nftables.
> 
> If you have any suggestion to improve it, please send your comments to Netfilter users mailing list <netfilter@vger.kernel.org>.
> 
> 
> = [[News]] =
> 
> 
> = Introduction =
```
