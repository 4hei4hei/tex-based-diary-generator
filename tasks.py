import invoke
import src.path_resolver as path_resolver


@invoke.task
def validate(c) -> None:
    invoke.run("black tasks.py ./src ./tests")
    invoke.run("flake8 tasks.py ./src ./tests --max-line-length 125")


@invoke.task(validate)
def test(c) -> None:
    invoke.run("python -m pytest -v")


@invoke.task(test, iterable=["args"])
def generate(c, args) -> None:
    current_dir = path_resolver.retrieve_current_dir()
    try:
        if current_dir == "src":
            invoke.run(
                f"python diary_generator.py --start_date {args[0]} --day_range {args[1]}"
            )
        else:
            invoke.run(
                f"cd ./src && \
                python diary_generator.py --start_date {args[0]} --day_range {args[1]}"
            )
    except IndexError:
        print("\nNot executed!! Pass correct args to 'inv generate'")
    except Exception as e:
        print(e)


@invoke.task(test)
def pdf(c) -> None:
    latest_dir = path_resolver.retrieve_latest_dir()
    invoke.run(
        f"cd ./diary/{latest_dir} &&\
        latexmk draft &&\
        open draft.pdf"
    )


@invoke.task
def convert(c) -> None:
    latest_dir = path_resolver.retrieve_latest_dir()
    if path_resolver.retrieve_current_dir() == "src":
        invoke.run(f"python ./file_ext_converter.py --target_dir ../diary/{latest_dir}")
        invoke.run(
            f"cp ../diary/{latest_dir}/draft.pdf ../converted_text/{latest_dir}/draft.pdf"
        )
        invoke.run(f"cp ../diary/figures/*.png ../converted_text/{latest_dir}")
    else:
        invoke.run(
            f"python ./src/file_ext_converter.py --target_dir ./diary/{latest_dir}"
        )
        invoke.run(
            f"cp ./diary/{latest_dir}/draft.pdf ./converted_text/{latest_dir}/draft.pdf"
        )
        invoke.run(f"cp ./diary/figures/*.png ./converted_text/{latest_dir}")


@invoke.task(pdf, convert)
def outputs(c) -> None:
    print("\nAll contents have been generated!!")
