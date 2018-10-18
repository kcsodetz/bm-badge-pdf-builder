"""
Python script to generate the Executive team badges for Boilermake VI

Author: Ken Sodetz
Since: 10/17/2018
"""
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Import font from .ttf file
pdfmetrics.registerFont(TTFont('Lato-Regular', 'Resources/Lato/Lato-Regular.ttf'))

# Constant Values
bottom_offset = 2 * inch
AC_width = 4.25 * inch
AC_height = 3 * inch
jpg_path = "Resources/AccessCardsJpg/AC_Exec.jpg"
pdf_path = "execs.pdf"
csv_path = "execs.csv"

# Define our canvas
c = canvas.Canvas(pdf_path, pagesize=letter)


# Left row of cards
def draw_left(i, name):
    c.drawImage(jpg_path, 0, bottom_offset + i * AC_height, width=AC_width,
                height=AC_height, mask=None)
    c.setFont("Lato-Regular", 16)
    c.drawCentredString(x=2.9 * inch, y=bottom_offset + 2 * inch + i * AC_height, text=name)
    c.setFont("Lato-Regular", 10)
    c.drawCentredString(x=2.9 * inch, y=bottom_offset + 1.75 * inch + i * AC_height,
                        text="Purdue University")


# Right row of cards
def draw_right(i, name):
    c.drawImage(jpg_path, AC_width, bottom_offset + i * AC_height, width=AC_width,
                height=AC_height, mask=None)
    c.setFont("Lato-Regular", 16)
    c.drawCentredString(x=2.9 * inch + AC_width, y=bottom_offset + 2 * inch + i * AC_height,
                        text=name)
    c.setFont("Lato-Regular", 10)
    c.drawCentredString(x=0 + 2.9 * inch + AC_width, y=bottom_offset + 1.75 * inch + i * AC_height,
                        text="Purdue University")


# Open CSV file.
print(f'Reading from {csv_path}...')
with open(csv_path, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    row_num = 0
    # For each row in the csv file.
    for row in csv_reader:
        # If line is even, draw left. Else draw right.
        if line_count % 2 == 0:
            draw_left(row_num, row[0])
        else:
            draw_right(row_num, row[0])
            row_num += 1

        # If on the third row, go to a new page and reset the row.
        if row_num == 3:
            c.showPage()
            row_num = 0

        line_count += 1

print(f'Processed {line_count} Badges to {pdf_path}')

c.save()
