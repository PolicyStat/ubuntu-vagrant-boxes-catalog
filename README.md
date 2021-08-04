# ubuntu-vagrant-boxes-catalog

## What this does

For a given ubuntu release URL, fetch the metadata for each version in that release then output a vagrant box catalog in JSON format.

## How to use

You should be able to use any release defined under https://cloud-images.ubuntu.com/releases/

Examples:

    python ubuntu_cagrant_box_catalog.py https://cloud-images.ubuntu.com/releases/focal/ > focal.json
    python ubuntu_cagrant_box_catalog.py https://cloud-images.ubuntu.com/releases/bionic/ > bionic.json
    python ubuntu_cagrant_box_catalog.py https://cloud-images.ubuntu.com/releases/xenial/ > xenial.json

Upload the JSON files somewhere (e.g. S3), and then you can setup vagrant to use it:

    vagrant init ubuntu-focal <url>/focal.json

 ## Why does this exist

The catalog that is hosted at https://app.vagrantup.com/ubuntu/ is either broken or
has undesirable behavior (as of 2021-08-04). This has been reported to Hashicorp but it is unknown whether it will be fixed.

Specifically, any query for an old box version is always redirected to the latest box. This means it's not possible to use any of the older boxes.

Example:

    > curl https://app.vagrantup.com/ubuntu/boxes/bionic64/versions/20210609.0.0/providers/virtualbox.box -s -L -I -o /dev/null -w '%{url_effective}'
    https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64-vagrant.box

Despite requesting the specific version `20210609.0.0`, the request is redirected to the current version. This happens for all releases, all versions.
