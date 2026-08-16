#!/bin/sh
set -eu

extension_dir="${XDG_DATA_HOME:-"$HOME/.local/share"}/nautilus-python/extensions"

mkdir -p "$extension_dir"
cp "$(dirname "$0")/copy_path.py" "$extension_dir/copy_path.py"
nautilus --quit 2>/dev/null || true

printf 'Installed Copy Path. Reopen Files to load the extension.\n'
