#!/bin/bash
# Uso: ./deploy.sh ~/eic-site   (pasta do projeto eic-worksheets, a que tem o firebase.json)
# A pasta destes arquivos tem o mesmo nome que terá no site: grammar/<nome-da-pasta>/
set -e
SITE="${1:-$HOME/eic-site}"
[ -f "$SITE/firebase.json" ] || { echo "firebase.json não encontrado em $SITE"; exit 1; }
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME="$(basename "$HERE")"
PUB=$(python3 -c "import json;h=json.load(open('$SITE/firebase.json'))['hosting'];print(h['public'] if isinstance(h,dict) else h[0]['public'])")
mkdir -p "$SITE/$PUB/grammar/$NAME"
for f in "$HERE"/*; do [ "$(basename "$f")" = deploy.sh ] || cp -v "$f" "$SITE/$PUB/grammar/$NAME/"; done
cd "$SITE" && firebase deploy --only hosting
