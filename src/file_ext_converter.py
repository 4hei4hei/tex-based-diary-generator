import argparse
import glob
import os
import shutil


def main(**args) -> None:
    # 出力先ディレクトリ内のファイルを削除する
    for target_file in glob.glob("./converted_text/*.txt"):
        os.remove(target_file)

    # 対象となるディレクトリパスを引数から取得
    target_dir = args["target_dir"]
    print(target_dir)

    # ディレクトリ配下の全ファイルから tex ファイルかつ、ファイル名が日付であるもののみのリストを生成
    body_files = [
        f
        for f in os.listdir(target_dir)
        if os.path.isfile(os.path.join(target_dir, f))
        if ".tex" in f
    ]
    not_applicables = ["body.tex", "bodies.tex", "draft.tex", "summary.tex"]
    for not_applicable in not_applicables:
        body_files.remove(not_applicable)

    for body_file in body_files:
        converted_body_file = body_file.replace(".tex", ".txt")
        new_body_file = f"{target_dir}/{converted_body_file}"
        shutil.copy(f"{target_dir}/{body_file}", new_body_file)
        shutil.move(new_body_file, f"./converted_text/{converted_body_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("file_ext_converter.py")
    parser.add_argument(
        "--target_dir",
        help="Target directory name",
        type=str,
    )

    args = parser.parse_args()
    main(**vars(args))
