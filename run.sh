#!bin/zsh

START_DATE=$1 # yyyy-mm-dd
DAY_RANGE=$2 # Nonnegative number

set -eu

poetry run inv test
cd ./src && poetry run python diary_generator.py --start_date ${START_DATE} --day_range ${DAY_RANGE}
