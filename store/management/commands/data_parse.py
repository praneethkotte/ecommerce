import os
from pathlib import Path
from django.db import models
from django.core.management.base import BaseCommand, CommandError
from openpyxl import load_workbook
from store.models import Product

class Command(BaseCommand):
    help = 'Load data from csv'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        print('table dropped')
        
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        book_path = os.path.join(base_dir, 'store/us_data/US Superstore data.xlsx')
        book = load_workbook(book_path)
        sheet = book['US Superstore data']
        print(sheet.title)
        max_row_num = sheet.max_row
        max_col_num = sheet.max_column
        print(max_row_num)
        print(max_col_num)

        # placeholder variables for city object
        country = "data_country"
        product = "data_product"
        category = "data_category"
        sub_category = "data_sub_category"
        product_name = "data_product_name"
        sales = "data_sales"


        for i in range(2, max_row_num): # for each row, minus the first (headers) and last (total count)

            for j in range(1, max_col_num+1): # for each column in each row 
                cell_obj=sheet.cell(row=i, column=j)
                if cell_obj.column_letter=='I':
                    country = cell_obj.value
                if cell_obj.column_letter=='N':
                    sector = cell_obj.value
                if cell_obj.column_letter=='O':
                    gas = cell_obj.value
                if cell_obj.column_letter=='P':
                    dec_2010 = cell_obj.value
                if cell_obj.column_letter=='Q':
                    dec_2000 = cell_obj.value
                if cell_obj.column_letter=='R':
                    dec_1990 = cell_obj.value
                

            data = Product.objects.create(country=country, product= product, category=category, sub_category=sub_category, product_name=product_name, sales=sales)

            data.save()
        
            if (i % 100 == 0):
                print(f'{i} records parsed')
    print("successfully parsed")