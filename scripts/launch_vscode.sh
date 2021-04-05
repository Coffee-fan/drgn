#!/bin/bash -e

log() { echo "$@"; }
info() { log "INFO: $@"; }

info "Launching vscode as root"
sudo -E code --user-data-dir=$HOME/.config/Code --extensions-dir=$HOME/.vscode/extensions .

