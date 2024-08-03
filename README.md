# tex-based-diary-generator

開始日から指定した日数分だけの日記用テンプレートを Tex ファイル群を基に PDF 形式で出力する

# Requirements

Mac 環境かつ、ツール群は以下の Version にて動作することを確認

asdf 管理

- Python ^3.12.4

- Poetry ^1.8.3

asdf 外 (Homebrew) の管理

- mactex-no-gui ^2023.0314

# How to use

リポジトリのルートディレクトリで invoke コマンドを実行する (必要に応じてコマンドの前段に `poetry run` を付与する)

e.g. 2023 年 1 月 1 日から 31 日間分の日記用ファイルを作成する

```bash
inv generate --args 2023-01-01 --args 31
```

作成された各ディレクトリ配下では tex ファイルに変更を加えた後に以下コマンドを実行することで pdf が出力される

```bash
latexmk draft
```

一度コマンドを実行すると、停止するまでインタラクティブモードになる

インタラクティブモードの間に tex ファイルに変更を加えてファイルを保存すると自動的に pdf を再出力できる

リポジトリのルートディレクトリで invoke コマンドを実行する形式でも生成が可能

```bash
inv pdf
```

invoke コマンドの場合、自動で最新のディレクトリを取得するため指定は不要

# Note

日記のテンプレートは template/ 配下に配置している

既存のテンプレートは必要に応じて修正する
