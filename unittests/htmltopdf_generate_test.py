import sys
import unittest

sys.path.append(".")
from src.utils import generate_pdf_from_template


class HtmlToPdfTest(unittest.TestCase):

    def test_all(self):
        param_dict = {
            'teacher_name': 'Test Teacher',
            'effective_date': '2018-07-10',
            'teacher_salary': '6500.00$'
        }
        status, output = generate_pdf_from_template('agreement.html',
                                                    param_dict, './test.pdf')
        print(status)
        print(output)


if __name__ == '__main__':
    unittest.main()
