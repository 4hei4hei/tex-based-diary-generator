import invoke
import os


def retrieve_latest_dir():
    dirs = os.listdir("./diary")
    latest_dir = sorted(dirs)[-1]
    return latest_dir


def retrieve_current_dir():
    current_path = os.getcwd()
    current_dir = current_path.split("/")[-1]
    return current_dir


@invoke.task
def validate(c):
    invoke.run("black tasks.py ./src ./tests")
    invoke.run("flake8 tasks.py ./src ./tests --max-line-length 125")


@invoke.task(validate)
def test(c):
    invoke.run("python -m pytest -v")


@invoke.task(test, iterable=["args"])
def generate(c, args):
    current_dir = retrieve_current_dir()
    if current_dir == "src":
        invoke.run(
            f"python diary_generator.py --start_date {args[0]} --day_range {args[1]}"
        )
    else:
        invoke.run(
            f"cd src && python diary_generator.py --start_date {args[0]} --day_range {args[1]}"
        )


@invoke.task(test)
def pdf(c):
    latest_dir = retrieve_latest_dir()
    invoke.run(f"cd ./diary/{latest_dir} && latexmk draft && open draft.pdf")


@invoke.task
def convert(c):
    latest_dir = retrieve_latest_dir()
    if retrieve_current_dir() == "src":
        invoke.run(f"python ./file_ext_converter.py --target_dir ../diary/{latest_dir}")
    else:
        invoke.run(
            f"python ./src/file_ext_converter.py --target_dir ./diary/{latest_dir}"
        )
