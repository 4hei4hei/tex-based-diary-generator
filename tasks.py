import invoke


@invoke.task
def validate(c):
    invoke.run("black src tests")
    invoke.run("flake8 src tests")


@invoke.task(validate)
def test(c):
    invoke.run("poetry run pytest -v")
