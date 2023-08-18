#!bin/zsh

START_DATE=$1 # yyyy-mm-dd
DAY_RANGE=$2 # Nonnegative number

set -eu

poetry run black ./tests 
poetry run black ./src
poetry run pytest -v
cd ./src && poetry run python diary_generator.py --start_date ${START_DATE} --day_range ${DAY_RANGE}
