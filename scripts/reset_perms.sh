#!/bin/bash -e

echo "Resetting permissions such that I do not mess things up"
sudo chown -R pierre:users $HOME/.config/Code $HOME/.vscode/extensions

