#!/bin/bash
# Uso: ./deploy.sh ~/eic-site   (pasta do projeto eic-worksheets, a que tem o firebase.json)
set -e
SITE="${1:-$HOME/eic-site}"
[ -f "$SITE/firebase.json" ] || { echo "firebase.json não encontrado em $SITE"; exit 1; }
cd "$(dirname "$0")"
PUB=$(python3 -c "import json;print(json.load(open('$SITE/firebase.json'))['hosting']['public'] if isinstance(json.load(open('$SITE/firebase.json'))['hosting'],dict) else json.load(open('$SITE/firebase.json'))['hosting'][0]['public'])")
mkdir -p "$SITE/$PUB/grammar/causative-permission-verbs"
cp -v grammar/causative-permission-verbs/* "$SITE/$PUB/grammar/causative-permission-verbs/"
cd "$SITE" && firebase deploy --only hosting
