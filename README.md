# お題カード生成ツール

企画案のマークダウンファイルからお題を抽出し、A4グリッドレイアウトのPDFを生成するCLIツールです。

## 使用方法

```bash
# 仮想環境の準備
python3 -m venv venv
source venv/bin/activate
pip install fpdf2

# 基本的な使用方法
python card_generator.py 企画案.md

# カスタム設定での使用方法
python card_generator.py 企画案.md -g 5 -c 2 -r 2 -o custom_cards.pdf
```

## オプション

- `-g, --groups`: グループ数（デフォルト: 9）
- `-c, --cols`: 列数（デフォルト: 3）
- `-r, --rows`: 行数（デフォルト: 3）
- `-o, --output`: 出力ファイル名（デフォルト: odai_cards.pdf）

## 必要なファイル

- `ipaexg.ttf`: 日本語フォントファイル（自動で配置済み）
- `企画案.md`: お題リストが含まれたマークダウンファイル

## 出力

指定されたグリッドレイアウトでA4サイズのPDFファイルが生成されます。各カードの中央にお題が表示され、罫線で区切られています。