set -eu
black "$@" --line-length 100 setup.py ctypesgen.py ctypesgencore/ --exclude '.*tab.py'

