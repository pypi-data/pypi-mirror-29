#!/bin/bash
echo '*** executing script ***'
sudo apt-get update
sudo apt-get --assume-yes install {}
sudo ln -s /usr/bin/{} /usr/bin/python
echo 'finished executing'
