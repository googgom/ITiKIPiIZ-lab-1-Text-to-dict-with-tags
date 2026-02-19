#!/bin/bash
rm -f ./dict.opcorpora.xml.zip
wget https://opencorpora.org/files/export/dict/dict.opcorpora.xml.zip
unzip dict.opcorpora.xml.zip
rm -f ./dict.opcorpora.xml.zip
echo 'Download & Extract complete'