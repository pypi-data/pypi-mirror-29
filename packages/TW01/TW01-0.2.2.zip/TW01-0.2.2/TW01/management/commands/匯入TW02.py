from os import walk
from subprocess import PIPE
import subprocess


from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from 臺灣言語工具.音標系統.閩南語.通用拼音音標 import 通用拼音音標
from os.path import join, basename
from TW01.management.commands._匯入指令 import 匯入指令


class Command(匯入指令):

    公家內容 = {
        '來源': 'TW02',
        '種類': '字詞',
        '年代': '2002',
    }

    def _全部資料(self, 語料目錄):
        for 所在, 資料夾陣列, _檔案陣列 in sorted(walk(語料目錄)):
            for 資料夾 in 資料夾陣列:
                if 資料夾 == 'usable':
                    yield from self._揣usable內底的檔案(join(所在, 資料夾))

    def _揣usable內底的檔案(self, 資料夾目錄):
        for 所在, _資料夾陣列, 檔案陣列 in sorted(walk(資料夾目錄)):
            for 檔案 in 檔案陣列:
                路徑 = join(所在, 檔案)
                if 路徑.endswith('.tcp'):
                    proc = subprocess.Popen(
                        ['iconv', '-f', 'big5', '-t', 'utf8', 路徑], stdout=PIPE
                    )
                    outs, _errs = proc.communicate()
                    for 一逝 in outs.decode().split('\n'):
                        if 一逝.strip():
                            編號, 漢羅, 通用 = 一逝.split()
                            音檔路徑 = join(所在, 編號 + '.wav')
#                             資料[編號] = (漢字, 通用)
                            try:
                                正規化物件 = (
                                    拆文分析器
                                    .對齊組物件(漢羅, 通用.replace('_', ' '))
                                    .轉音(通用拼音音標)
                                )
                                yield (basename(所在), 音檔路徑, 正規化物件)
                            except 解析錯誤:
                                self.stderr.write(str((漢羅, 通用)))
                                pass
