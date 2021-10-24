

from os import path
import pandas as pd
import tabula
import PyPDF2
import os
import boto3
from io import BytesIO
from django.conf import settings

def pdf_from_s3(bucket_name,file_name):
    s3 = boto3.resource('s3',
         aws_access_key_id=settings.AWS_ACCESS_ID,
         aws_secret_access_key= settings.AWS_ACCESS_KEY)
    """bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter():
        print (obj.key)"""
    obj = s3.Object(bucket_name=bucket_name, key=file_name)
    fs = obj.get()['Body'].read()
    pdf = PyPDF2.PdfFileReader(BytesIO(fs))
    #file_pdf = pdf.getFormTextFields()
    return pdf

def separate_url_file(path):
    arr = path.split("/")
    arr_2 = arr[2].split(".")
    bucket = arr_2[0]
    file_name = arr[-1]
    return (bucket,file_name)

def obtain_count(path_name, type):
    data = {}
    list_bbva_pdf = ['Datos/Reportes GF BBVA/1T21.pdf','Datos/Reportes GF BBVA/2T20.pdf',
            'Datos/Reportes GF BBVA/2T21.pdf','Datos/Reportes GF BBVA/3T20.pdf',
            'Datos/Reportes GF BBVA/4T20.pdf']
    for count, lista in enumerate(list_bbva_pdf):
        print(lista,count)
        extract_balance_activo_BBVA(lista,count)
    return data

def extract_data(id_bank,type,url_file):
    if id_bank == 1:
        #BBVA
        return extract_data_BBVA(type,url_file)
    if id_bank == 2:
        #Banorte
        return extract_data_BANORTE(type,url_file)
    if id_bank == 3:
        #Santander
        return extract_data_SANTANDER(type,url_file)

def extract_data_BBVA(type,url_file):
    count = obtain_count(url_file)
    if type == 1:
        #Balance Activo
        return extract_balance_activo_BBVA(url_file,count)
    if type == 2:
        #Balance Activo
        return extract_balance_activo_BBVA(url_file,count)
    if type == 3:
        #Balance Activo
        return extract_balance_activo_BBVA(url_file,count)
    if type == 4:
        #Balance Activo
        return extract_balance_activo_BBVA(url_file,count)
    if type == 5:
        #Balance Activo
        return extract_balance_activo_BBVA(url_file,count)
    if type == 6:
        #Balance Activo
        return extract_balance_activo_BBVA(url_file,count)

def extract_data_BANORTE(type,url_file):
    count = obtain_count(url_file)
    if type == 1:
        #Balance Activo
        return extract_balance_activo_BANORTE(url_file,count)

def extract_data_SANTANDER(type,url_file):
    count = obtain_count(url_file)
    if type == 1:
        #Balance Activo
        return extract_balance_activo_SANTANDER(url_file,count)

def extract_balance_activo_BANORTE(path,count):
    print("BANORTE")

def extract_balance_activo_SANTANDER(path,count):
    print("SANTANDER")

def extract_balance_activo_BBVA(path,count):
    (bucket_name,item_name) = separate_url_file(path)
    pdfReader = pdf_from_s3(bucket_name,item_name)
    pageObj = pdfReader.getPage(2)
    Texto_indice = pageObj.extractText()
    BBVA_dict = {}
    value_add = [1,4.4,-2,2.8,-0.3]

    #Acciones para Balance General Activo
    Activo_pag = (Texto_indice[Texto_indice.find('Activo',Texto_indice.find('Estados Financieros'))+167:Texto_indice.find('Activo',Texto_indice.find('Estados Financieros')) +173])
    Activo_pag = Activo_pag.replace(' ', '')
    Activo_pag = Activo_pag.replace('P', '')
    Activo_pag = int(Activo_pag.replace('.', ''))
    area_activo_1 = [i*2.83 for i in [45 ,10+ value_add[count], 251, 100+value_add[count]] ]
    area_activo_2 = [i*2.83 for i in [45 ,99+value_add[count], 251, 118+value_add[count]] ]
    area_activo_3 = [i*2.83 for i in [45 ,117+value_add[count], 251, 137+value_add[count]] ]
    area_activo_4 = [i*2.83 for i in [45 ,135+value_add[count], 251, 154.8+value_add[count]] ]
    area_activo_5 = [i*2.83 for i in [45 ,153.5+value_add[count], 251, 172.8+value_add[count]] ]
    area_activo_6 = [i*2.83 for i in [45 ,171.6+value_add[count], 251, 198+value_add[count]] ]
    df_column1 = tabula.read_pdf(path,
                                stream= True,
                                area = area_activo_1, 
                                multiple_tables = False,
                                output_format="dataframe")[0].dropna(axis='columns')
    print(df_column1)
    df_column1 = tabula.read_pdf(path, 
                                pages = str(Activo_pag),
                                stream= True,area = area_activo_1,
                                multiple_tables = False,
                                output_format="dataframe")[0].dropna(axis='columns')
    df_column2 = tabula.read_pdf(path, pages = str(Activo_pag),stream= True,area = area_activo_2, multiple_tables = False,output_format="dataframe")[0].dropna(axis='columns')
    df_column3 = tabula.read_pdf(path, pages = str(Activo_pag),stream= True,area = area_activo_3, multiple_tables = False,output_format="dataframe")[0].dropna(axis='columns')
    df_column4 = tabula.read_pdf(path, pages = str(Activo_pag),stream= True,area = area_activo_4, multiple_tables = False,output_format="dataframe")[0].dropna(axis='columns')
    df_column5 = tabula.read_pdf(path, pages = str(Activo_pag),stream= True,area = area_activo_5, multiple_tables = False,output_format="dataframe")[0].dropna(axis='columns')
    df_column6 = tabula.read_pdf(path, pages = str(Activo_pag),stream= True,area = area_activo_6, multiple_tables = False,output_format="dataframe")[0].dropna(axis='columns')
    df_columns_names = [df_column1.columns.values,df_column2.columns.values,df_column3.columns.values,df_column4.columns.values,df_column5.columns.values,df_column6.columns.values]

    df_column1.rename(columns={df_columns_names[0][0]: df_columns_names[0][0]+ ' '+str(df_column1[str(df_columns_names[0][0])][0])},inplace=True)
    df_column2.rename(columns={df_columns_names[1][0]: df_columns_names[1][0]+ ' '+str(df_column2[str(df_columns_names[1][0])][0])},inplace=True)
    df_column3.rename(columns={df_columns_names[2][0]: df_columns_names[2][0]+ ' '+str(df_column3[str(df_columns_names[2][0])][0])},inplace=True)
    df_column4.rename(columns={df_columns_names[3][0]: df_columns_names[3][0]+ ' '+str(df_column4[str(df_columns_names[3][0])][0])},inplace=True)
    df_column5.rename(columns={df_columns_names[4][0]: df_columns_names[4][0]+ ' '+str(df_column5[str(df_columns_names[4][0])][0])},inplace=True)
    df_column6.rename(columns={df_columns_names[5][0]: df_columns_names[5][0]+ ' '+str(df_column6[str(df_columns_names[5][0])][0])},inplace=True)

    df_general = df_column1.join(df_column2.join(df_column3.join(df_column4.join(df_column5.join(df_column6)))))
    print (df_general)
    return (df_general)

def run():
    from detail.models import Category
    categories = Category.objects.all()
    for cat in categories:
        print(cat.name)

if __name__ == '__main__':
    import django
    #  you have to set the correct path to you settings module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")
    django.setup()
    run()
