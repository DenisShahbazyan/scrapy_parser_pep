import datetime as dt
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.count_pep = defaultdict(int)

    def process_item(self, item, spider):
        self.count_pep[item['status']] += 1
        return item

    def close_spider(self, spider):
        dir_path = BASE_DIR / 'results'
        dir_path.mkdir(exist_ok=True)
        now = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = dir_path / f'status_summary_{now}.csv'
        with open(filename, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for key, value in self.count_pep.items():
                f.write(f'{key},{value}\n')
            f.write(f'Total,{sum(self.count_pep.values())}\n')
