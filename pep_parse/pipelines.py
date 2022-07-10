import csv
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
            writer = csv.writer(f, dialect='unix')
            writer.writerows([
                ['Статус', 'Количество'],
                *self.count_pep.items(),
                ['Total', sum(self.count_pep.values())],
            ])
