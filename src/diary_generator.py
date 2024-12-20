import argparse
import datetime
import re
import shutil
import textfile
from logging import getLogger

import path_resolver

logger = getLogger(__name__)
allowed_pettern_start_day = r"[0-9]{4}-[0-9]{2}-[0-9]{2}"


def validate_args(args) -> tuple:
    """
    引数の検証を行う
    """
    exception_messeage = ""
    try:
        start_day = args["start_date"]
        day_range = args["day_range"]
        if start_day is None or day_range is None:
            raise ValueError(
                "Args are empty (required two args, i.e., --start_date and --day_range)"
            )

        fmt_flag = re.fullmatch(allowed_pettern_start_day, start_day)

        if fmt_flag is None:
            raise ValueError(
                "Date format is invalid (You must give a date, such as yyyy-mm-dd)"
            )
        if day_range <= 0:
            raise ValueError(
                "Number of days format is invalid (You must give a nonnegative integer)"
            )
        return start_day, day_range

    except ValueError as e:
        exception_messeage = e

    except Exception as e:
        exception_messeage = e

    logger.error("\nAn error occurred in current execution: " + str(exception_messeage))
    return str(exception_messeage)


def generate_files(start_day, day_range) -> None:
    """
    開始日と日数を基にディレクトリとファイルを生成する
    """

    # 日付操作用の datetime クラスオブジェクト
    datetime_start_day = datetime.datetime.strptime(start_day, "%Y-%m-%d")
    datetime_end_day = datetime_start_day + datetime.timedelta(days=day_range - 1)

    # ディレクトリ名用の str オブジェクト
    str_start_day = "".join(str(datetime_start_day).split()[0].split("-"))
    str_end_day = "".join(str(datetime_end_day).split()[0].split("-"))

    current_dir = path_resolver.retrieve_current_dir()
    if current_dir == "src":
        dir_name = f"../diary/{str_start_day}-{str_end_day}"
    else:
        dir_name = f"./diary/{str_start_day}-{str_end_day}"
    print(rf"{str_start_day}-{str_end_day}/ is generated!!")

    try:
        if current_dir == "src":
            shutil.copytree("../templates/", f"./{dir_name}/")
        else:
            shutil.copytree("./templates/", f"../{dir_name}/")
    except OSError as e:
        logger.info(e)
        pass

    for day in range(day_range):
        datetime_day = datetime_start_day + datetime.timedelta(days=day)
        file_name = "".join(str(datetime_day).split()[0].split("-"))

        shutil.copyfile(f"{dir_name}/body.tex", f"./{dir_name}/{file_name}.tex")

        textfile.replace(
            f"./{dir_name}/{file_name}.tex",
            r"\section*{yyyymmdd}",
            rf"\section*{{{file_name}}}",
        )
        f = open(f"./{dir_name}/bodies.tex", "a")
        f.write(rf"\include{{ {file_name}.tex}}" + "\n")


def main(**args) -> None:
    logger.info("Start generate dirary files")

    try:
        start_day, day_range = validate_args(args)
        generate_files(start_day, day_range)
        logger.info("Generate dirary files is finished!!")
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("diary_generator.py")
    parser.add_argument("--start_date", help="Start date of file generation", type=str)
    parser.add_argument(
        "--day_range", help="Number of days for file generation", type=int
    )
    args = parser.parse_args()
    main(**vars(args))
