# お題カード生成ツール

## 概要

企画案のマークダウンファイルからお題を抽出し、A4サイズの用紙にグリッドレイアウトで配置されたお題カードのPDFを生成するコマンドラインツールです。

### 主な機能

- **マークダウン解析**: 企画案.mdファイルからODAI_LIST配列を自動抽出
- **柔軟なレイアウト**: カスタマイズ可能な列数×行数のグリッド配置
- **日本語対応**: IPAフォントを使用した正しい日本語表示
- **切り取りやすさ**: 薄いグレーの切り取り線で簡単にカード分離
- **自動改ページ**: 1ページに収まらない場合の自動ページ送り

### 使用場面

- 社内イベント（納会、歓送迎会等）の伝言ゲーム準備
- ワークショップやアイスブレイクのお題カード作成
- チームビルディング活動のゲーム素材準備

## 必要な環境

- **Python**: 3.7以上
- **OS**: Windows, macOS, Linux（Python実行環境があること）
- **必要な空き容量**: 約10MB（フォントファイル含む）

## インストールと初期設定

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd card-generator-py
```

### 2. 仮想環境の作成と有効化

```bash
# 仮想環境作成
python3 -m venv venv

# 仮想環境有効化（macOS/Linux）
source venv/bin/activate

# 仮想環境有効化（Windows）
venv\\Scripts\\activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 日本語フォントの配置

ツールはIPAフォント（ipaexg.ttf）を使用します。初回実行時に自動でダウンロードされますが、手動で配置する場合：

```bash
# IPAフォントのダウンロード（自動実行されるため通常不要）
curl -L -o ipafont.zip https://moji.or.jp/wp-content/ipafont/IPAexfont/ipaexg00401.zip
unzip ipafont.zip
cp ipaexg00401/ipaexg.ttf .
```

## 使用方法

**重要**: 仮想環境を有効化してから実行してください。

### 基本的な使用法

```bash
# 1. 仮想環境を有効化
source venv/bin/activate

# 2. デフォルト設定でPDF生成（3×3グリッド、9グループ）
python card_generator.py 企画案.md
```

### カスタム設定での使用法

```bash
# 仮想環境有効化後に以下を実行

# グループ数を指定
python card_generator.py 企画案.md -g 5

# レイアウトを指定（2×2グリッド）
python card_generator.py 企画案.md -c 2 -r 2

# 出力ファイル名を指定
python card_generator.py 企画案.md -o custom_cards.pdf

# 全オプション組み合わせ
python card_generator.py 企画案.md -g 5 -c 2 -r 2 -o event_cards.pdf
```

### なぜマークダウンファイルが必要？

このツールは**お題を外部ファイルから読み込む**設計になっています：

1. **柔軟性**: コードを変更せずにお題だけを変更可能
2. **再利用性**: イベント別に企画案ファイルを作成・管理
3. **保守性**: お題の管理とプログラムロジックを分離

例：
- `忘年会_企画案.md` → 忘年会用のお題カード
- `新人研修_企画案.md` → 研修用のお題カード  
- `チームビルディング_企画案.md` → チームビルディング用

### コマンドライン引数

| 引数 | 省略形 | 説明 | デフォルト値 |
|------|--------|------|-------------|
| `markdown_file` | - | 企画案のマークダウンファイルパス | **必須** |
| `--groups` | `-g` | グループ数 | 9 |
| `--cols` | `-c` | 列数（横方向のカード数） | 3 |
| `--rows` | `-r` | 行数（縦方向のカード数） | 3 |
| `--output` | `-o` | 出力PDFファイル名 | `odai_cards.pdf` |

### ヘルプ表示

```bash
python card_generator.py --help
```

## 企画案ファイルの形式

マークダウンファイル内に以下の形式でお題リストを記述してください：

```python
ODAI_LIST = [
    "全力で壁ドンするサンタクロース",
    "締切に追われている夏目漱石", 
    "自撮りが盛れて喜んでいる織田信長",
    "ヨガの難しいポーズに挑戦するドラえもん",
    "初めてのZoom会議で固まっている坂本龍馬",
]
```

## 出力結果

### PDFの仕様

- **用紙サイズ**: A4（210mm × 297mm）
- **向き**: 縦向き
- **マージン**: 10mm
- **フォント**: IPAフォント 12pt
- **切り取り線**: 薄いグレー（RGB: 180,180,180）の細線

### カード計算

- **総カード数** = お題数 × グループ数
- **1ページあたりのカード数** = 列数 × 行数
- **総ページ数** = ⌈総カード数 ÷ 1ページあたりのカード数⌉

#### 計算例

```
お題数: 5個
グループ数: 9組
レイアウト: 3×3（9枚/ページ）

総カード数 = 5 × 9 = 45枚
総ページ数 = ⌈45 ÷ 9⌉ = 5ページ
```

## 注意点とトラブルシューティング

### ⚠️ 重要な注意点

1. **フォントファイル**
   - `ipaexg.ttf`が見つからない場合、エラーで停止します
   - 初回実行時は自動ダウンロードのため時間がかかる場合があります

2. **マークダウンファイル**
   - `ODAI_LIST`配列が正しく記述されていることを確認してください
   - 配列内の文字列は必ずダブルクォートで囲んでください

3. **出力ファイル**
   - 同名のPDFファイルが存在する場合、上書きされます
   - 生成されたPDFファイルは`.gitignore`により除外されています

### よくあるエラーと対処法

#### エラー: "ファイル '企画案.md' が見つかりません"
```bash
# 解決方法: ファイルパスを確認
ls -la *.md
python card_generator.py ./企画案.md
```

#### エラー: "ODAI_LISTが見つかりません"
```bash
# 解決方法: マークダウンファイル内の記述を確認
grep -n "ODAI_LIST" 企画案.md
```

#### エラー: "フォントファイルが見つからない"
```bash
# 解決方法: フォントファイルの再取得
rm -f ipaexg.ttf
curl -L -o ipafont.zip https://moji.or.jp/wp-content/ipafont/IPAexfont/ipaexg00401.zip
unzip ipafont.zip && cp ipaexg00401/ipaexg.ttf .
```

### パフォーマンスについて

- **処理時間**: 45枚（5ページ）で約1-2秒
- **メモリ使用量**: 約10-20MB
- **ファイルサイズ**: 1ページあたり約50-100KB

## カスタマイズ例

### 小さいカード（多数配置）
```bash
# 4×4グリッドで16枚/ページ
python card_generator.py 企画案.md -c 4 -r 4
```

### 大きいカード（少数配置）
```bash
# 2×2グリッドで4枚/ページ
python card_generator.py 企画案.md -c 2 -r 2
```

### イベント別ファイル
```bash
# 忘年会用
python card_generator.py 企画案.md -g 10 -o 忘年会_お題カード.pdf

# 新人研修用
python card_generator.py 企画案.md -g 5 -c 2 -r 3 -o 新人研修_アイスブレイク.pdf
```

## ライセンス

このツールはMITライセンスの下で公開されています。

### 使用フォントについて

- **IPAフォント**: IPA Font License Agreement v1.0
- フォントファイルは[IPA(情報処理推進機構)](https://moji.or.jp/ipafont/)より提供

## 開発・貢献

### 開発環境の構築
```bash
git clone <repository-url>
cd card-generator-py
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 品質チェック
```bash
# コード検証
python -m py_compile card_generator.py

# 動作テスト
python card_generator.py 企画案.md -o test.pdf
```

## 更新履歴

- **v1.1.0**: 切り取り線を薄いグレーの実線に変更
- **v1.0.0**: 初回リリース - 基本的なPDF生成機能