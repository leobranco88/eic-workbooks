#!/bin/bash
# Uso: ./deploy.sh ~/eic-site   (pasta do projeto eic-worksheets, a que tem o firebase.json)
set -e
SITE="${1:-$HOME/eic-site}"
[ -f "$SITE/firebase.json" ] || { echo "firebase.json não encontrado em $SITE"; exit 1; }
cd "$(dirname "$0")"
PUB=$(python3 -c "import json;h=json.load(open('$SITE/firebase.json'))['hosting'];print(h['public'] if isinstance(h,dict) else h[0]['public'])")
mkdir -p "$SITE/$PUB/grammar/causative-permission-verbs" "$SITE/$PUB/neural-markers"
cp -v grammar/causative-permission-verbs/* "$SITE/$PUB/grammar/causative-permission-verbs/"
cp -rv neural-markers/mix-it neural-markers/defend-it "$SITE/$PUB/neural-markers/"
mkdir -p "$SITE/$PUB/neural-english"; cp -v neural-english/index.html "$SITE/$PUB/neural-english/"
cd "$SITE" && firebase deploy --only hosting
