import sys
import unittest
import uuid

sys.path.append(".")
from src.utils import generate_pdf_from_template


class HtmlToPdfTest(unittest.TestCase):

    def test_all(self):
        param_dict = {
            'teacher_name': 'Test Teacher',
            'effective_date': '2018-07-10',
            'teacher_salary': '6500.00$'
        }

        filename = str(uuid.uuid1())+'.pdf'

        status, output = generate_pdf_from_template('agreement.html',
                                                    param_dict, filename)
        print(status)
        print('output--->'+output)


if __name__ == '__main__':
    unittest.main()
