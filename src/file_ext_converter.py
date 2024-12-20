import argparse
import os
import shutil

import path_resolver


def remove_not_applicables(body_files) -> list:
    not_applicables = ["body.tex", "bodies.tex", "draft.tex"]
    for not_applicable in not_applicables:
        body_files.remove(not_applicable)

    return body_files


def main(**args) -> None:
    # 出力先ディレクトリ内のファイルを削除する
    if path_resolver.retrieve_current_dir() == "src":
        converted_text_dir = "../converted_text"
        dirs = os.listdir("../")
    else:
        converted_text_dir = "./converted_text"
        dirs = os.listdir("./")

    # 出力先が存在する場合は中身を掃除、ない場合はディレクトリを作成する
    if "converted_text" in dirs:
        shutil.rmtree(converted_text_dir)
    else:
        os.makedirs(converted_text_dir)

    # 対象となるディレクトリパスを引数から取得
    target_dir = args["target_dir"]

    # ディレクトリ配下の全ファイルから tex ファイルかつ、ファイル名が日付であるもののみのリストを生成
    body_files = [
        f
        for f in os.listdir(target_dir)
        if os.path.isfile(os.path.join(target_dir, f))
        if ".tex" in f
    ]
    body_files = remove_not_applicables(body_files)

    latest_dir_name = path_resolver.retrieve_latest_dir()
    os.makedirs(f"./converted_text/{latest_dir_name}", exist_ok=True)

    for body_file in body_files:
        converted_body_file = body_file.replace(".tex", ".txt")
        new_body_file = f"{target_dir}/{converted_body_file}"
        shutil.copy(f"{target_dir}/{body_file}", new_body_file)
        shutil.move(
            new_body_file, f"./converted_text/{latest_dir_name}/{converted_body_file}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser("file_ext_converter.py")
    parser.add_argument(
        "--target_dir",
        help="Target directory name",
        type=str,
    )

    args = parser.parse_args()
    main(**vars(args))
