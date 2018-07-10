import json
import os
import sys

import unittest
from datetime import datetime, timedelta

from fpdf import FPDF, HTMLMixin


class MyPdf(FPDF, HTMLMixin):
    pass


class HtmlToPdfTest(unittest.TestCase):

    def test_all(self):
        print(os.getcwd())
        with open('./pdf_templates/agreement.html', 'r') as f:
            lines = f.readlines()
        html = ''.join(lines)
        pdf = MyPdf()
        pdf.add_page()
        pdf.add_font('simkai', '', './font/simkai.ttf', uni=True)
        pdf.write_html(html)
        pdf.output('./agreement.pdf', 'F')


if __name__ == '__main__':
    unittest.main()