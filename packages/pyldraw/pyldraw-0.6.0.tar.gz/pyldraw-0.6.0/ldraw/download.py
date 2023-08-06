#!/usr/bin/env python
"""
Takes care of downloading the complete.zip from LDraw.org
And generating the parts.lst from it
"""
from __future__ import print_function
import zipfile
import os

from mklist.generate import generate_parts_lst

from ldraw.compat import urlretrieve
from ldraw.dirs import get_data_dir
from ldraw.utils import ensure_exists


def download_main(output_dir):
    """ Main function for the downloading/mklist """
    ensure_exists(output_dir)

    url = 'http://www.ldraw.org/library/updates/complete.zip'

    retrieved = os.path.join(output_dir, "complete.zip")

    if not os.path.exists(retrieved):
        print('retrieve the complete.zip from ldraw.org ...')
        urlretrieve(url, filename=retrieved)

    if not os.path.exists(os.path.join(output_dir, 'ldraw')):
        print('unzipping the complete.zip ...')
        zip_ref = zipfile.ZipFile(retrieved, 'r')
        zip_ref.extractall(output_dir)
        zip_ref.close()

    parts_lst_path = os.path.join(output_dir, 'ldraw', '%s.lst')
    for name in ['parts', 'p']:
        if not os.path.exists(parts_lst_path % name):
            print('parts.lst mklist...')
            generate_parts_lst('description',
                               os.path.join(output_dir, 'ldraw', name),
                               parts_lst_path% name)


if __name__ == '__main__':
    download_main(get_data_dir())
