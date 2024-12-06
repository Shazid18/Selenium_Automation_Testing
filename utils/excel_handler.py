import pandas as pd
from datetime import datetime

class ExcelHandler:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = []

    def add_result(self, page_url, testcase, status, comments):
        self.results.append({
            'page_url': page_url,
            'testcase': testcase,
            'status': status,
            'comments': comments
        })

    def save_results(self, filename=None):
        if filename is None:
            filename = f'test_results_{self.timestamp}.xlsx'
        
        df = pd.DataFrame(self.results)
        df.to_excel(filename, index=False)
        return filename