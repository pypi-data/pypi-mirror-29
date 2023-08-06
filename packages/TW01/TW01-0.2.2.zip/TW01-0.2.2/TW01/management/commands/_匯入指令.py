from django.core.management.base import BaseCommand


from 臺灣言語服務.models import 訓練過渡格式


class 匯入指令(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '語料目錄',
            type=str,
        )
        parser.add_argument(
            '--匯入幾筆',
            type=int,
            default=100000,
            help='試驗用，免一擺全匯'
        )

    def handle(self, *args, **參數):
        self.stdout.write('資料數量：{}'.format(訓練過渡格式.資料數量()))

        全部資料 = []
        匯入數量 = 0
        for 語者, 音檔路徑, 正規化物件 in self._全部資料(參數['語料目錄']):
            全部資料.append(
                訓練過渡格式(
                    影音所在=音檔路徑, 影音語者=語者,
                    文本=正規化物件.看分詞(),
                    **self.公家內容
                )
            )

            匯入數量 += 1
            if 匯入數量 % 100 == 0:
                self.stdout.write('匯入 {} 筆'.format(匯入數量))
            if 匯入數量 == 參數['匯入幾筆']:
                break

        self.stdout.write('檢查格式了匯入')
        訓練過渡格式.加一堆資料(全部資料)

        self.stdout.write('資料數量：{}'.format(訓練過渡格式.資料數量()))
