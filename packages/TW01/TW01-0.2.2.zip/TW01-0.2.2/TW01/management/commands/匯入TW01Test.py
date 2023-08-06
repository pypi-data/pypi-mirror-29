from os import walk
from os.path import join
from subprocess import PIPE
import subprocess


from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from 臺灣言語工具.音標系統.閩南語.通用拼音音標 import 通用拼音音標
from TW01.management.commands._匯入指令 import 匯入指令


class Command(匯入指令):

    公家內容 = {
        '來源': 'TW01Test',
        '種類': '字詞',
        '年代': '2001',
    }

    def _全部資料(self, 語料目錄):
        for 所在, _資料夾陣列, 檔案陣列 in sorted(walk(語料目錄)):
            for 檔案 in sorted(檔案陣列)[:10]:
                路徑 = join(所在, 檔案)
                if 檔案 == 'TW01MIC_TEST_validated.tcp':
                    proc = subprocess.Popen(
                        ['iconv', '-f', 'big5', '-t', 'utf8', 路徑], stdout=PIPE
                    )
                    outs, _errs = proc.communicate()
#                     print(路徑)
                    for 一逝 in outs.decode().split('\n'):
                        if 一逝.strip():
                            編號, 通用1, _通用2 = 一逝.split()
                            音檔路徑 = join(所在, 編號 + '.wav')
#                             資料[編號] = (漢字, 通用)
                            用的音標 = 通用1.replace('_', ' ')
                            try:
                                正規化物件 = (
                                    拆文分析器
                                    .對齊組物件(用的音標, 用的音標)
                                    .轉音(通用拼音音標)
                                )
                                yield (編號.split('_')[2], 音檔路徑, 正規化物件)
                            except 解析錯誤:
                                self.stderr.write(str((用的音標, 用的音標)))
                                pass
