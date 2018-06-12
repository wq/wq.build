set -e
if [ "$LINT" ]; then
    flake8 *.py
else
    python setup.py test
fi
