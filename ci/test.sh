#!/bin/bash -eux
shopt -s xpg_echo

if [[ -z "$1" ]]; then
    echo Usage:
    echo    $0 env-name
    exit 1
fi

# A safer way to invoke 'sed', compensates for the difference between BSD and GNU sed.
# https://stackoverflow.com/a/38595160/1950432
safe_sed () {
    sed --version > /dev/null 2>&1 && sed -i -- "$@" || sed -i "" "$@"
}

echo "\033[1;36m================================\033[0m"
echo "\033[1;36m================================ Testing: $1\033[0m"
echo "\033[1;36m================================\033[0m"

set -x
pwd
cat ci/envs/$1.cookiecutterrc
rm -rf TestProject

# if [ -d "fprime" ]
# then
#     # update F Prime?
#     echo 'F Prime already cloned.'
# else
#     git clone https://github.com/nasa/fprime.git
# fi

cookiecutter --no-input --config-file=ci/envs/$1.cookiecutterrc .

python3 ci/check_rendered_config.py $1 # -e ci/envs -o .

# fprime-util generate
# fprime-util build
