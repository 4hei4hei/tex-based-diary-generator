import invoke
import os


@invoke.task
def validate(c):
    invoke.run("black ./src ./tests")
    invoke.run("flake8 ./src ./tests --max-line-length 100")


@invoke.task(validate)
def test(c):
    invoke.run("poetry run pytest -v")


@invoke.task(test)
def convert(c):
    dirs = os.listdir("./diary")
    target_dir = sorted(dirs)[-1]
    invoke.run(
        f"poetry run python ./src/file_ext_converter.py --target_dir ./diary/{target_dir}"
    )
