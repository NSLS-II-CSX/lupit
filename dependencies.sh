#!/bin/bash
cd ..
git clone https://github.com/arkilic/dummyBroker
cd dummyBroker
python setup.py install
cd ..
git clone https://github.com/NSLS-II/metadataStpre
cd metadataStore
python setup.py install