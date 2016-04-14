#!/usr/bin/env python
# coding: utf-8
''' IMBdownloader : download all Internet Magazine Back Number Archives'''
import re
import os
from urllib2 import urlopen, HTTPError

html = urlopen('http://i.impressrd.jp/bn').read()  # read index page
indexHrefs = re.compile('<a href=\"/bn/pdf/.+\">').findall(html)  # make href list
indexUrls = []
for indexHref in indexHrefs:
    indexUrls.append('http://i.impressrd.jp'+indexHref[9:-2])
# ['http://i.impressrd.jp/bn/pdf/1994/10/001',...'http://i.impressrd.jp/bn/pdf/2006/05/136']
for indexUrl in indexUrls:
    html = urlopen(indexUrl).read()
    dirName = indexUrl[-11:-7]+indexUrl[-6:-4]  # ex)~~impressrd.jp/bn/pdf/1994/10/001->199410
    os.mkdir(dirName)
    pdfHrefs = re.compile('<a href=\"/files/images/bn/pdf/.+\.pdf\">').findall(html)
    # ['<a href="/files/images/bn/pdf/im199410-002-contens.pdf">', ...]
    for pdfHref in pdfHrefs:
        url = 'http://i.impressrd.jp'+pdfHref[9:-2]
        # ex) http://i.impressrd.jp/files/images/bn/pdf/im199410-002-contens.pdf
        pdfName = dirName+'/'+pdfHref[30:-2]
        # ex) 199410/im199410-002-contens.pdf
        print pdfName
        try:
            pdf = urlopen(url).read()
            open(pdfName, 'wb').write(pdf)
        except HTTPError:
            print '  Could not download'
