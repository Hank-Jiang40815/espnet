# 導入os模塊，用於操作文件和目錄
import os
# 導入whisper模塊，用於語音轉文字
import whisper
# 導入pypinyin模塊，用於漢字轉拼音
from pypinyin import pinyin, Style
# 導入tqdm模塊，用於顯示進度條
from tqdm import tqdm

# 定義wav文件的根目錄
wav_root = '/jiawei/dataset'

# 定義一個函數，用於轉錄wav文件並返回文本和拼音
def transcribe_wav(wav_file_path):
    # 使用Whisper的large-v2模型轉錄wav文件
    whisper_model = whisper.load_model('large-v2')
    result = whisper_model.transcribe(wav_file_path)
    # 獲取轉錄的文本
    text = result['text']
    # 使用pypinyin將文本轉換為拼音（帶聲調）
    pinyin_list = pinyin(text, style=Style.TONE3)
    # 返回文本和拼音
    return text, pinyin_list

# 定義一個函數，用於將文本和拼音結合成指定的格式
def combine_text_pinyin(wav_file, text, pinyin_list):
    # 將文本和拼音結合成指定的格式
    combined = f"{wav_file} "
    for char, pinyin_item in zip(text, pinyin_list):
        combined += f"{char} {''.join(pinyin_item)} "
    # 移除最後的空格
    combined = combined.strip()
    # 返回結合後的字符串
    return combined

# 定義一個函數，用於遍歷wav文件夾下的子目錄，並將轉錄結果寫入content.txt文件
def process_wav_dir(wav_dir, content_file):
    # 遍歷wav文件夾下的子目錄，例如boy3, boy5等
    for wav_sub_dir in os.listdir(wav_dir):
        # 獲取子目錄的完整路徑
        wav_sub_path = os.path.join(wav_dir, wav_sub_dir)
        # 判斷是否是文件夾
        if os.path.isdir(wav_sub_path):
            # 獲取子目錄下的所有wav文件
            wav_files = [f for f in os.listdir(wav_sub_path) if f.endswith('.wav')]
            # 使用tqdm模塊包裝wav文件列表，顯示進度條
            wav_files = tqdm(wav_files, desc=f"Processing {wav_sub_dir}")
            # 遍歷每個wav文件
            for wav_file in wav_files:
                # 獲取wav文件的完整路徑
                wav_file_path = os.path.join(wav_sub_path, wav_file)
                # 轉錄wav文件並獲得文本和拼音
                text, pinyin_list = transcribe_wav(wav_file_path)
                # 將文本和拼音結合成指定的格式
                combined = combine_text_pinyin(wav_file, text, pinyin_list)
                # 將結果寫入content.txt文件，每行一個wav文件的結果
                content_file.write(combined + '\n')

# 遍歷wav文件的子目錄，例如train, test等
for sub_dir in os.listdir(wav_root):
    # 獲取子目錄的完整路徑
    sub_path = os.path.join(wav_root, sub_dir)
    # 判斷是否是文件夾
    if os.path.isdir(sub_path):
        # 定義content.txt文件的路徑，根據不同的子目錄生成不同的文件
        content_path = os.path.join(sub_path, 'content.txt')
        # 打開content.txt文件，準備寫入
        with open(content_path, 'w', encoding='utf-8') as f:
            # 獲取子目錄下的wav文件夾的路徑
            wav_path = os.path.join(sub_path, 'wav')
            # 調用函數，遍歷wav文件夾下的子目錄，並將轉錄結果寫入content.txt文件
            process_wav_dir(wav_path, f)
