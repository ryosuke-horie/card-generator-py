#!/usr/bin/env python3
"""
お題カード生成ツール
企画案のマークダウンファイルからお題を抽出し、A4グリッドレイアウトでPDFを生成
"""

import argparse
import re
import sys
from pathlib import Path
from fpdf import FPDF

# デフォルト設定
DEFAULT_GROUPS = 9
DEFAULT_COLS = 3
DEFAULT_ROWS = 3
DEFAULT_OUTPUT = "odai_cards.pdf"

def extract_topics_from_markdown(markdown_file):
    """
    マークダウンファイルからお題リストを抽出
    """
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ODAI_LIST配列から値を抽出
        pattern = r'ODAI_LIST\s*=\s*\[(.*?)\]'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # 文字列リストを抽出
            list_content = match.group(1)
            topics = re.findall(r'"([^"]+)"', list_content)
            return topics
        else:
            print("エラー: マークダウンファイルからODAI_LISTが見つかりません")
            return []
            
    except FileNotFoundError:
        print(f"エラー: ファイル '{markdown_file}' が見つかりません")
        return []
    except Exception as e:
        print(f"エラー: ファイル読み込み中にエラーが発生しました: {e}")
        return []

def process_topic_text(topic):
    """
    お題テキストの前処理（改行タグ対応）
    """
    # <br>、<BR>、\nを改行に変換
    topic = topic.replace('<br>', '\n')
    topic = topic.replace('<BR>', '\n')
    topic = topic.replace('\\n', '\n')
    return topic

def generate_pdf(topics, num_groups, cols, rows, output_file):
    """
    PDF生成（1ページに同じお題を配置）
    """
    if not topics:
        print("エラー: お題が見つかりません")
        return False
    
    cards_per_page = cols * rows
    total_cards = len(topics) * num_groups
    
    # PDF初期化
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    
    # 日本語フォント設定
    try:
        pdf.add_font('ipaexg', '', 'ipaexg.ttf')
    except Exception as e:
        print(f"エラー: フォントファイル 'ipaexg.ttf' が見つからない、または読み込めません: {e}")
        return False
    
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # ページ設定
    margin = 10
    page_width = 210 - (margin * 2)
    page_height = 297 - (margin * 2)
    card_width = page_width / cols
    card_height = page_height / rows
    
    print(f"お題数: {len(topics)}")
    print(f"グループ数: {num_groups}")
    print(f"総カード数: {total_cards}")
    print(f"レイアウト: {cols}x{rows}")
    
    page_counter = 0
    
    # お題ごとにページを作成
    for topic_index, topic in enumerate(topics):
        processed_topic = process_topic_text(topic)
        cards_remaining = num_groups
        
        print(f"お題 {topic_index + 1}: '{topic}' の処理中...")
        
        while cards_remaining > 0:
            # 新しいページを作成
            pdf.add_page()
            page_counter += 1
            print(f"  {page_counter}ページ目を作成中...")
            
            # このページに配置するカード数
            cards_this_page = min(cards_remaining, cards_per_page)
            
            for card_index in range(cards_this_page):
                # カード位置計算
                col = card_index % cols
                row = card_index // cols
                
                x = margin + (col * card_width)
                y = margin + (row * card_height)
                
                # フォント設定
                pdf.set_font('ipaexg', '', 12)
                
                # 切り取り線描画（薄い点線）
                pdf.set_line_width(0.1)
                pdf.set_draw_color(180, 180, 180)  # 薄いグレー
                
                # 縦の切り取り線（カード右側）
                if col < cols - 1:  # 最後の列以外
                    line_x = x + card_width
                    # 手動で点線を描画（2mmごとに1mm線を描画）
                    for dot_y in range(int(y), int(y + card_height), 4):
                        if dot_y + 2 <= y + card_height:
                            pdf.line(line_x, dot_y, line_x, dot_y + 2)
                
                # 横の切り取り線（カード下側）
                if row < rows - 1:  # 最後の行以外
                    line_y = y + card_height
                    # 手動で点線を描画（2mmごとに1mm線を描画）
                    for dot_x in range(int(x), int(x + card_width), 4):
                        if dot_x + 2 <= x + card_width:
                            pdf.line(dot_x, line_y, dot_x + 2, line_y)
                
                # 線の色をリセット
                pdf.set_draw_color(0, 0, 0)
                
                # テキスト配置（中央揃え）
                text_height = 6
                pdf.set_xy(x, y + (card_height - text_height) / 2)
                pdf.multi_cell(card_width, text_height, processed_topic, align='C')
            
            cards_remaining -= cards_this_page
    
    # PDF出力
    try:
        pdf.output(output_file)
        print("-" * 40)
        print(f"完了: '{output_file}' を生成しました")
        print(f"総ページ数: {page_counter}")
        return True
    except Exception as e:
        print(f"エラー: PDF生成中にエラーが発生しました: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='マークダウンファイルからお題カードPDFを生成'
    )
    parser.add_argument(
        'markdown_file',
        help='企画案のマークダウンファイルパス'
    )
    parser.add_argument(
        '-g', '--groups',
        type=int,
        default=DEFAULT_GROUPS,
        help=f'グループ数 (デフォルト: {DEFAULT_GROUPS})'
    )
    parser.add_argument(
        '-c', '--cols',
        type=int,
        default=DEFAULT_COLS,
        help=f'列数 (デフォルト: {DEFAULT_COLS})'
    )
    parser.add_argument(
        '-r', '--rows',
        type=int,
        default=DEFAULT_ROWS,
        help=f'行数 (デフォルト: {DEFAULT_ROWS})'
    )
    parser.add_argument(
        '-o', '--output',
        default=DEFAULT_OUTPUT,
        help=f'出力ファイル名 (デフォルト: {DEFAULT_OUTPUT})'
    )
    
    args = parser.parse_args()
    
    # 入力ファイル存在確認
    if not Path(args.markdown_file).exists():
        print(f"エラー: ファイル '{args.markdown_file}' が見つかりません")
        sys.exit(1)
    
    # パラメータ検証
    if args.groups <= 0 or args.cols <= 0 or args.rows <= 0:
        print("エラー: グループ数、列数、行数は1以上を指定してください")
        sys.exit(1)
    
    # お題抽出
    topics = extract_topics_from_markdown(args.markdown_file)
    if not topics:
        sys.exit(1)
    
    # PDF生成
    success = generate_pdf(topics, args.groups, args.cols, args.rows, args.output)
    
    if success:
        print("処理完了")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()