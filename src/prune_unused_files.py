import argparse
import difflib
import os
from logging import getLogger

logger = getLogger(__name__)


def prune_unused_files(body_files, target_dir) -> None:
    """
    target_dir で指定したディレクト配下の tex ファイルをテンプレートのファイルと比較するループを回す
    結果次第でその tex ファイルを削除する
    """
    # 比較対象の template 用ファイルのパスを宣言
    template_body_path = f"{target_dir}/body.tex"

    # 一覧化されたリストの要素を一つずつ見させるループ
    for body_file in body_files:
        # template 用のファイルと同様に対象ファイル (body) のパスを取得
        body_file_path = f"{target_dir}/{body_file}"

        # テンプレートファイルと対象ファイルをそれぞれファイルオブジェクトとして開く
        template_body = open(template_body_path)
        body = open(body_file_path)

        # 1 行目は日付を記載する箇所のため、読み飛ばしてリスト化する
        list_template_body = template_body.readlines()[1:]
        list_body = body.readlines()[1:]

        # リスト化した各ファイルの diff オブジェクトを取得
        diff = difflib.Differ()
        diff_output = diff.compare(list_template_body, list_body)

        # diff オブジェクトを引数に、差分があるか判定する関数を呼び出し、結果を取得する
        prune_flag = compare_files(diff_output)

        # 取得した結果を基に、True の場合は当該ファイルを削除する
        if prune_flag is True:
            os.remove(body_file_path)
            print(f"{body_file_path} is pruned.")

        # 対象のファイルを閉じ、次の要素の比較へ移る
        template_body.close()
        body.close()


def compare_files(diff_output) -> bool:
    """
    最初の行以外で差分があれば True を返し、そうでなければ False を返す
    """
    prune_flag = True
    for data in diff_output:
        if data[0:1] in ["+", "-"]:
            prune_flag = False
    return prune_flag


def main(**args) -> None:
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

    # 生成したリストを引数として関数を呼び出す
    prune_unused_files(body_files, target_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("prune_unused_files.py")
    parser.add_argument(
        "--target_dir",
        help="Target directory name",
        type=str,
    )

    args = parser.parse_args()
    main(**vars(args))
