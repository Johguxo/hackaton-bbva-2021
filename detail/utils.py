

from os import path
import pandas as pd
from detail.models import Detail, DetailFeature, DetailSubfeature, Season
from institution.models import Institution
from resource.models import File, UserInstitutionFile
import tabula
import PyPDF2
import os
import boto3
from io import BytesIO
from django.conf import settings
import math

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
    #print(path)
    arr = path.split("/")
    arr_2 = arr[2].split(".")
    bucket = arr_2[0]
    file_name = arr[-1]
    return (bucket,file_name)

def obtain_count(name):
    name.replace('.pdf','')
    if '2T20':
        return 0
    elif '2T21':
        return 1

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

def extract_data_BBVA(type_report,url_file):
    print("Archivo: ", url_file)
    if type_report.id == 3:
        #Balance Activo
        return extract_balance_BBVA(url_file,'Activo')
    if type_report.id == 2:
        #Balance Activo
        return extract_balance_BBVA(url_file,'Pasivo')

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

def extract_balance_BBVA(path,count,modo):
    print("bbvaaaaa:", modo)
    (bucket_name,item_name) = separate_url_file(path)
    pdfReader = pdf_from_s3(bucket_name,item_name)
    pageObj = pdfReader.getPage(2)
    Texto_indice = pageObj.extractText()
    BBVA_dict = {}

    #count = obtain_count(item_name)
    #print(count)
    if modo == 'Activo':
        value_add = [4.6,-2]
        #Acciones para Balance General Activo
    
        Activo_pag = (Texto_indice[Texto_indice.find('Activo',Texto_indice.find('Estados Financieros'))+167:Texto_indice.find('Activo',Texto_indice.find('Estados Financieros')) +173])
        Activo_pag = Activo_pag.replace(' ', '')
        Activo_pag = Activo_pag.replace('P', '')
        Activo_pag = int(Activo_pag.replace('.', ''))
        #print(Activo_pag)

        area_activo_1 = [i*2.83 for i in [45 ,15+ value_add[count], 251, 100+value_add[count]] ]
        area_activo_2 = [i*2.83 for i in [45 ,99+value_add[count], 251, 118+value_add[count]] ]
        area_activo_3 = [i*2.83 for i in [45 ,117+value_add[count], 251, 137+value_add[count]] ]
        area_activo_4 = [i*2.83 for i in [45 ,135+value_add[count], 251, 154.8+value_add[count]] ]
        area_activo_5 = [i*2.83 for i in [45 ,152+value_add[count], 251, 173.3+value_add[count]] ]
        area_activo_6 = [i*2.83 for i in [45 ,171+value_add[count], 251, 198+value_add[count]] ]
        df_column1 = tabula.read_pdf(path, pages = str(Activo_pag),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0].dropna(axis='columns')
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
        #print(df_general)
        return df_general

    
    
    #Acciones para Balance General Pasivo
    elif modo == "Pasivo":
        #value_add = [0,0,-6,0,-2]
        value_add = [0,-6]

        Activo_pag = (Texto_indice[Texto_indice.find('Pasivo y Capital',Texto_indice.find('Estados Financieros'))+159:Texto_indice.find('Pasivo y Capital',Texto_indice.find('Estados Financieros')) +165])
        Activo_pag = Activo_pag.replace(' ', '')
        Activo_pag = Activo_pag.replace('C', '')
        Activo_pag = int(Activo_pag.replace('.', ''))
        print(Activo_pag)

        area_activo_1 = [i*2.83 for i in [35 ,15+ value_add[count], 253, 113+value_add[count]] ]
        area_activo_2 = [i*2.83 for i in [35 ,108+value_add[count], 253, 200+value_add[count]] ]

        df_column1 = tabula.read_pdf(path, pages = str(Activo_pag),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0].dropna(axis='columns')
        df_column2 = tabula.read_pdf(path, pages = str(Activo_pag),stream= True,area = area_activo_2, multiple_tables = False,output_format="dataframe")[0].dropna(axis='columns')
        df_column2['Dic'] = df_column2['Dic'] #.str.replace(r"[a-zA-Z]",'')

        df_columns_names = ['Grupo Financiero BBVA Bancomer, S.A. de C.V.', 'Jun', 'Sep', 'Dic', 'Mar', 'Jun.1']

        df_column1.rename(columns={df_columns_names[0]: df_columns_names[0]+ ' '+str(df_column1[str(df_columns_names[0])][0])},inplace=True)
        df_column2.rename(columns={df_columns_names[1]: df_columns_names[1]+ ' '+str(df_column2[str(df_columns_names[1])][0])},inplace=True)
        df_column2.rename(columns={df_columns_names[2]: df_columns_names[2]+ ' '+str(df_column2[str(df_columns_names[2])][0])},inplace=True)
        df_column2.rename(columns={df_columns_names[3]: df_columns_names[3]+ ' '+str(df_column2[str(df_columns_names[3])][0])},inplace=True)
        df_column2.rename(columns={df_columns_names[4]: df_columns_names[4]+ ' '+str(df_column2[str(df_columns_names[4])][0])},inplace=True)
        df_column2.rename(columns={df_columns_names[5]: df_columns_names[5]+ ' '+str(df_column2[str(df_columns_names[5])][0])},inplace=True)


        df_general = df_column1.join(df_column2)
        #print(df_general)
        return df_general


    elif modo == "Cuentas_Orden":
        #Acciones para Cuentas de orden

        Activo_pag = (Texto_indice[Texto_indice.find('Cuentas de Orden',Texto_indice.find('Estados Financieros'))+152:Texto_indice.find('Cuentas de Orden',Texto_indice.find('Estados Financieros')) +164])
        Activo_pag = Activo_pag.replace('\n', '')
        Activo_pag = Activo_pag.replace(' ', '')
        Activo_pag = Activo_pag.replace('E', '')
        Activo_pag = Activo_pag.replace('s', '')
        Activo_pag = int(Activo_pag.replace('.', ''))
        print(Activo_pag)
        
        area_activo_1 = [i*2.83 for i in [45 ,25, 118, 265] ]

        df_column1 = tabula.read_pdf(path, pages = str(Activo_pag),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='columns')
        keys = df_column1.keys()
        df_1 = df_column1[[keys[0], keys[1] ]]
        df_2 = df_column1[[keys[2], keys[3] ]]
        df_2.rename(columns={keys[2]: keys[0]},inplace=True)
        df_2.rename(columns={keys[3]: keys[1]},inplace=True)
        new_df_column1 = df_1.append(df_2).dropna(axis='rows',how='all').reset_index()
        new_df_column1.rename(columns={new_df_column1.keys()[2]: new_df_column1.keys()[1]+f'{count}'},inplace=True)
        #print(new_df_column1)
        return new_df_column1
    
    
    elif modo == "Resultados":
    #Acciones para Estado de resultados

        Activo_pag = (Texto_indice[Texto_indice.find('Estado de Result',Texto_indice.find('Estados Financieros'))+152:Texto_indice.find('Estado de Result',Texto_indice.find('Estados Financieros')) +160])
        Activo_pag = Activo_pag.replace('\n', '')
        Activo_pag = Activo_pag.replace(' ', '')
        Activo_pag = Activo_pag.replace('E', '')
        Activo_pag = Activo_pag.replace('s', '')
        Activo_pag = int(Activo_pag.replace('.', ''))

        value_top = [55,54]
        value_left = [19,30]
        value_bottom = [175,183]
        value_right = [169,189]
        
        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count], 205]]

        df_column1 = tabula.read_pdf(path, pages = str(Activo_pag),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='columns')
        print(df_column1.keys())
        
        if count == 0:
            df_column1['Unnamed: 1'] = df_column1['Estado de Resultados Consolidado 2T'].str.replace(r"[a-zA-Z]",'')
            df_column1['Unnamed: 1'] = df_column1['Unnamed: 1'].str.replace("ó",'')
            df_column1['Unnamed: 1'] = df_column1['Unnamed: 1'].str.replace("(",'')
            df_column1['Unnamed: 1'] = df_column1['Unnamed: 1'].str.replace(")",'')
            df_column1['Unnamed: 1'] = df_column1['Unnamed: 1'].str.replace(", ",'')
            df_column1['Unnamed: 1'] = df_column1['Unnamed: 1'].str.replace(" ,",'')
            df_column1['Unnamed: 1'] = df_column1['Unnamed: 1'].str.replace(" ",'')
            df_column1['Unnamed: 1'] = df_column1['Unnamed: 1'].str.replace("é",'')
            df_column1['Estado de Resultados Consolidado 2T'] = df_column1['Estado de Resultados Consolidado 2T'].str.replace('\d+', '')
            df_column1['Estado de Resultados Consolidado 2T'] = df_column1['Estado de Resultados Consolidado 2T'].str.replace('(', '')
            df_column1['Estado de Resultados Consolidado 2T'] = df_column1['Estado de Resultados Consolidado 2T'].str.replace(')', '')
            df_column1 = df_column1[['Estado de Resultados Consolidado 2T','Unnamed: 1','3T','4T','1T','2T']]
        df_column1.rename(columns={df_column1.keys()[1]: df_column1.keys()[1]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[2]: df_column1.keys()[2]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[3]: df_column1.keys()[3]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[4]: df_column1.keys()[4]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[5]: df_column1.keys()[5]+f'{count}'},inplace=True)
        
        #print(df_column1)
        return df_column1
    
    elif modo == "Estado de flujos":
        #Acciones para Cuentas de orden

        Activo_pag = (Texto_indice[Texto_indice.find('Estado de Flujos',Texto_indice.find('Estados Financieros'))+146:Texto_indice.find('Estado de Flujos',Texto_indice.find('Estados Financieros')) +155])
        Activo_pag = Activo_pag.replace('\n', '')
        Activo_pag = Activo_pag.replace(' ', '')
        Activo_pag = Activo_pag.replace('E', '')
        Activo_pag = Activo_pag.replace('s', '')
        Activo_pag = Activo_pag.replace('t', '')
        Activo_pag = int(Activo_pag.replace('.', ''))
        
        value_top = [42,42,42,42,42]
        value_left = [58,57,56,50,65]
        value_bottom = [184,188,184,189,179]
        value_right = [160,160,165,169,154]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count],value_right[count] ]]

        df_column1 = tabula.read_pdf(path, pages = str(Activo_pag),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='columns')
        df_column1 = df_column1[[df_column1.keys()[0],df_column1.keys()[2]]]
        #df_column1.rename(columns={df_column1.keys()[1]: df_column1.keys()[0]+f'{count}'},inplace=True)

        return df_column1

    elif modo == "Estado de variaciones":
        #Acciones para Cuentas de orden
        
        value_top = [ 60.05, 51.40, 56.42, 64.11, 59.79]
        value_left = [ 25.25, 25.41, 25.43, 25.09, 25.45]
        value_bottom = [ 131.96, 126.55, 138.55, 135.12, 138.27]
        value_right = [ 264.43, 252.72, 260.06, 239.67, 263.58]
        pages = [ 58, 61, 58, 59, 61]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count],value_right[count] ]]

        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='columns')
        df_column1 = df_column1[[df_column1.keys()[0],df_column1.keys()[2]]]
        #df_column1.rename(columns={df_column1.keys()[1]: df_column1.keys()[0]+f'{count}'},inplace=True)

        return df_column1
    
    elif modo == "Movimiento de cartera":
        #Acciones para Cuentas de orden
        
        value_top = [ 161.33, 39.01, 127.6, 117.65, 39.73 ]
        value_left = [ 14.40, 14.89, 14.73, 15.16, 14.81 ]
        value_bottom = [ 261.18, 144.67, 220.63, 221.03, 139.72 ]
        value_right = [ 197.13, 195.17, 193.74, 196.15, 197.2 ]
        pages = [ 65, 68, 64, 65, 68]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count],value_right[count] ]]

        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='columns')
        df_column1 = df_column1[[df_column1.keys()[0],df_column1.keys()[2]]]
        #df_column1.rename(columns={df_column1.keys()[1]: df_column1.keys()[0]+f'{count}'},inplace=True)

        return df_column1

    elif modo == "Coeficiente de cobertura":
        #Acciones para Cuentas de orden
        
        value_top = [ 99.55, 25.42, 99.46, 99.89, 25.05]
        value_left = [ 21.25, 25.59, 14.35, 24.87, 21.56]
        value_bottom = [ 237.63, 150.16, 231.79, 240.35, 163.49]
        value_right = [ 203.43, 192.13, 194.52, 196.94, 202.39]
        pages = [ 41, 44, 41, 42, 44]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count],value_right[count] ]]

        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='columns')
        #df_column1 = df_column1[[df_column1.keys()[0],df_column1.keys()[2]]]
        #df_column1.rename(columns={df_column1.keys()[1]: df_column1.keys()[0]+f'{count}'},inplace=True)

        return df_column1

def createDataframe( path, pages, valueTop, valueLeft, valueBottom, valueRight, count  ):

    if valueTop[count][1] == 0:
        print("Raa oages")
        areaTable = [i*2.83 for i in [valueTop[count][0] ,valueLeft[count][0], valueBottom[count][0],valueRight[count][0] ]] 
        print("raaaa pages", pages[count][0] )
        dfCreated = tabula.read_pdf(path, pages = str(pages[count][0]),stream= True,area = areaTable, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='columns')
        print("Dataframe cretaed without 0", dfCreated)
        #dfCreated = dfCreated[[dfCreated.keys()[0],dfCreated.keys()[2]]]
    else:
        areaTable1 = [i*2.83 for i in [valueTop[count][0] ,valueLeft[count][0], valueBottom[count][0],valueRight[count][0] ]] 
        dfCreated1 = tabula.read_pdf(path, pages = str(pages[count][0]),stream= True,area = areaTable1, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='columns')
        #dfCreated1 = dfCreated1[[dfCreated1.keys()[0],dfCreated1.keys()[2]]]
        
        areaTable2 = [i*2.83 for i in [valueTop[count][1] ,valueLeft[count][1], valueBottom[count][1],valueRight[count][1] ]] 
        dfCreated2 = tabula.read_pdf(path, pages = str(pages[count][1]),stream= True,area = areaTable2, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='columns')
        #dfCreated2 = dfCreated2[[dfCreated2.keys()[0],dfCreated2.keys()[2]]]
        
        dfCreated1.append(dfCreated2)
        dfCreated = dfCreated1
        print("Dataframe cretaed with 0", dfCreated)

    return dfCreated

def extract_balance_santander(path,count,modo):
    print("santandereeee:", modo)
    """if os.path.exists(path):
        print ("File exist")
        pass
    else:
        print ("File not exist")
        return 0"""

    
    if modo == 'Activo':
        ##Para balance activo
        value_top = [42,39]
        value_left = [10,4]
        value_bottom = [255,251]
        value_right = [85,90]
        pages = [41,42]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count], 205]]
        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='columns')
        return df_column1
    
    elif modo == 'Pasivo':
    ##Para balance pasivo
        value_top = [42,39]
        value_left = [10,4]
        value_bottom = [255,251]
        value_right = [85,90]
        pages = [42,43]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count], 205]]
        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0].dropna(axis='rows',how='all')
        df_column1 = df_column1.reset_index()
        return df_column1
    
    elif modo == 'Cuentas_Orden':
        ##Para cuentas de orden
        value_top = [47,41]
        value_left = [10,5]
        value_bottom = [125,119]
        #value_right = [85,90]
        pages = [43,44]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count], 205]]
        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0].dropna(axis='rows',how='all').dropna(axis='columns',how='all')
        df_column1.rename(columns={'Jun': 'Jun'+f'{count}'},inplace=True)
        df_column1.rename(columns={'Mar':'Mar'+f'{count}'},inplace=True)
        df_column1.rename(columns={'Dic': 'Dic'+f'{count}'},inplace=True)
        df_column1.rename(columns={'Sep': 'Sep'+f'{count}'},inplace=True)
        df_column1 = df_column1.reset_index()
        #print(df_column1)
        return df_column1
    
    elif modo == 'Resultados':
        ##Para cuentas de orden
        value_top = [37,34]
        value_left = [10,10]
        value_bottom = [144,145]
        #value_right = [85,90]
        pages = [44,45]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count], 203]]
        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0].dropna(axis='rows',how='all').dropna(axis='columns',how='all')
        df_column1 = df_column1.reset_index()
        df_column1.rename(columns={df_column1.keys()[1]: df_column1.keys()[1]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[2]: df_column1.keys()[2]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[3]: df_column1.keys()[3]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[4]: df_column1.keys()[4]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[5]: df_column1.keys()[5]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[6]: df_column1.keys()[6]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[7]: df_column1.keys()[7]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[8]: df_column1.keys()[8]+f'{count}'},inplace=True)

        return df_column1

    elif modo == 'Estado de flujos':
        ##Para cuentas de orden
        value_top = [29,29,29,29,29]
        value_left = [19,19,19,19,19]
        value_bottom = [240,249,249,253,247]
        value_right = [190,190,190,190,190]

        pages = [46,47,48,47,44]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count], value_right[count] ]]
        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0].dropna(axis='rows',how='all') #.dropna(axis='columns',how='all')
        df_column1 = df_column1[[df_column1.keys()[0],df_column1.keys()[2]]]
        df_column1.rename(columns={df_column1.keys()[1]: df_column1.keys()[1]+f'{count}'},inplace=True)
        #print(df_column1)
        return df_column1

    elif modo == "Estado de variaciones":
        #Acciones para Cuentas de orden
        
        value_top = [ 20.62, 20.49, 20.39, 20.43, 20.17]
        value_left = [ 7.19, 7.31, 7.32, 7.32, 7.33]
        value_bottom = [ 149.72, 150.58, 156.65, 149.5, 149.73]
        value_right = [ 271.89, 273.17, 271.90, 272.19, 272.41]
        pages = [ 44, 45, 46, 45, 42]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count],value_right[count] ]]

        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='columns')
        df_column1 = df_column1[[df_column1.keys()[0],df_column1.keys()[2]]]
        #df_column1.rename(columns={df_column1.keys()[1]: df_column1.keys()[0]+f'{count}'},inplace=True)

        return df_column1
    
    elif modo == "Coeficiente de cobertura":
        #Acciones para Cuentas de orden
        
        value_top    = [ (113.36,0), (111.76,0), (33.565,0), (86.82,0),  (170.01, 20.02) ]
        value_left   = [ (24.56,0),  (20.01,0),  (18.45,0),  (24.66,0),  (24.39, 25.14) ]
        value_bottom = [ (255.70,0), (255.53,0), (175.86,0),  (228.88,0),  (261.83, 85.21) ]
        value_right  = [ (202.72,0), (190.28,0), (195.61,0),  (203.1,0), (203.21, 203.22) ]
        pages        = [ (117,0),    (118,0),    (117,0),    (116,0),    (113,114) ]

        df_column1 = createDataframe( path, pages, value_top, value_left, value_bottom, value_right, count)
        print("Dataframe cretaed", df_column1)
        #df_column1.rename(columns={df_column1.keys()[1]: df_column1.keys()[0]+f'{count}'},inplace=True)

        return df_column1

def extract_balance_banorte(path,count,modo):
    print("banorteeeee", modo)
    """"if os.path.exists(path):
        print ("File exist")
        pass
    else:
        print ("File not exist")
        return 0"""

    if modo == 'Activo':
        ##Para balance activo
        value_top = [19,22]
        value_left = [33,41]
        value_bottom = [265,230]
        value_right = [179,170]
        pages = [32,34]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count], 205]]
        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='columns')
        
        df_columns_names = ['GFNorte – Balance General', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5','Unnamed: 6']

        df_column1.rename(columns={df_columns_names[0]: df_columns_names[0]+ ' '+str(df_column1[str(df_columns_names[0])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[1]: df_columns_names[1]+ ' '+str(df_column1[str(df_columns_names[1])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[2]: df_columns_names[2]+ ' '+str(df_column1[str(df_columns_names[2])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[3]: df_columns_names[3]+ ' '+str(df_column1[str(df_columns_names[3])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[4]: df_columns_names[4]+ ' '+str(df_column1[str(df_columns_names[4])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[5]: df_columns_names[5]+ ' '+str(df_column1[str(df_columns_names[5])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[6]: df_columns_names[6]+ ' '+str(df_column1[str(df_columns_names[6])][0])},inplace=True)
        
        return df_column1

    
    elif modo == 'Pasivo':
        ##Para balance pasivo
        value_top = [19,22]
        value_left = [27,39]
        value_bottom = [265,240]
        value_right = [179,170]
        pages = [33,35]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count], 205]]
        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0].dropna(axis='rows',how='all')
        df_columns_names = ['GFNorte – Balance General', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5','Unnamed: 6']
        df_column1 = df_column1.reset_index()
        df_column1.rename(columns={df_columns_names[0]: df_columns_names[0]+ ' '+str(df_column1[str(df_columns_names[0])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[1]: df_columns_names[1]+ ' '+str(df_column1[str(df_columns_names[1])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[2]: df_columns_names[2]+ ' '+str(df_column1[str(df_columns_names[2])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[3]: df_columns_names[3]+ ' '+str(df_column1[str(df_columns_names[3])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[4]: df_columns_names[4]+ ' '+str(df_column1[str(df_columns_names[4])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[5]: df_columns_names[5]+ ' '+str(df_column1[str(df_columns_names[5])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[6]: df_columns_names[6]+ ' '+str(df_column1[str(df_columns_names[6])][0])},inplace=True)
        
        return df_column1

    elif modo == 'Cuentas_Orden':
        ##Para Cuentas de orden
        value_top = [19,22]
        value_left = [27,39]
        value_bottom = [265,240]
        value_right = [179,170]
        pages = [34,36]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count], 205]]
        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0] #.dropna(axis='rows',how='all')
        df_columns_names = ['GFNorte - Cuentas de Orden', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5','Unnamed: 6']
        df_column1 = df_column1.reset_index()
        df_column1.rename(columns={df_columns_names[0]: df_columns_names[0]+ ' '+f'{count}'+str(df_column1[str(df_columns_names[0])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[1]: df_columns_names[1]+ ' '+f'{count}'+str(df_column1[str(df_columns_names[1])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[2]: df_columns_names[2]+ ' '+f'{count}'+str(df_column1[str(df_columns_names[2])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[3]: df_columns_names[3]+ ' '+f'{count}'+str(df_column1[str(df_columns_names[3])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[4]: df_columns_names[4]+ ' '+f'{count}'+str(df_column1[str(df_columns_names[4])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[5]: df_columns_names[5]+ ' '+f'{count}'+str(df_column1[str(df_columns_names[5])][0])},inplace=True)
        df_column1.rename(columns={df_columns_names[6]: df_columns_names[6]+ ' '+f'{count}'+str(df_column1[str(df_columns_names[6])][0])},inplace=True)
        
        return df_column1

    elif modo == 'Resultados':
        ##Para Cuentas de orden
        value_top = [43,43]
        value_left = [38,39]
        value_bottom = [266,262]
        value_right = [179,170]
        pages = [31,33]

        area_activo_1 = [i*2.83 for i in [value_top[count] ,value_left[count], value_bottom[count], 205]]
        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0]#.dropna(axis='rows',how='all')
        #df_column1 = df_column1.reset_index()
        df_column1.rename(columns={df_column1.keys()[0]: df_column1.keys()[0]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[1]: df_column1.keys()[1]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[2]: df_column1.keys()[2]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[3]: df_column1.keys()[3]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[4]: df_column1.keys()[4]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[5]: df_column1.keys()[5]+f'{count}'},inplace=True)
        df_column1.rename(columns={df_column1.keys()[6]: df_column1.keys()[6]+f'{count}'},inplace=True)
        
        return df_column1
    
    elif modo == 'Estado de flujos':
        ##Para estado de flujos
        value_top = [41,37,36,40,34]
        value_left = [44,44,44,44,44]
        value_bottom = [262,230,257,233,228]
        value_right = [170,170,170,170,170]
        pages = [35,35,37,34,35]

        area_activo_1 = [i*2.83 for i in [value_top[count]-3 ,value_left[count], value_bottom[count], value_right[count]]]
        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0].dropna(axis='columns',how='all')
        df_column1.rename(columns={df_column1.keys()[1]: df_column1.keys()[1]+ ' '+f'{count}'},inplace=True)
       
        return df_column1
    
    elif modo == 'Estado de variaciones':
        ##Para estado de variaciones
        value_top = [49,39,41,42,41]
        value_left = [21,21,22,22,22]
        value_bottom = [176,176,166,177,168]
        value_right = [192,192,192,192,192]
        pages = [36,36,38,35,36]

        area_activo_1 = [i*2.83 for i in [value_top[count]-4 ,value_left[count], value_bottom[count], value_right[count]]]
        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0].dropna(axis='columns',how='all')
        
        return df_column1

    elif modo == 'Liquidez':
        ##Para estado de variaciones
        value_top = [71,63,70,68,68]
        value_left = [23,24,23,24,24]
        value_bottom = [230,232,229,228,228]
        value_right = [(171,197),(170,194),(171,196),(172,197),(172,197)]
        pages = [23,23,25,23,23]
        

        area_activo_1 = [i*2.83 for i in [value_top[count],value_left[count], value_bottom[count], value_right[count][0]]]
        area_activo_2 = [i*2.83 for i in [value_top[count],value_right[count][0], value_bottom[count], value_right[count][1]]]

        df_column1 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_1, multiple_tables = False,output_format="dataframe")[0].dropna(axis='columns',how='all')
        df_column2 = tabula.read_pdf(path, pages = str(pages[count]),stream= True,area = area_activo_2, multiple_tables = False,output_format="dataframe")[0].dropna(axis='columns',how='all')
        df_column = df_column1.join(df_column2)
        #print(df_column)
        return df_column






"""list_bbva_pdf = ['Datos/Reportes GF BBVA/1T21.pdf',
'Datos/Reportes GF BBVA/2T20.pdf',
            'Datos/Reportes GF BBVA/2T21.pdf',
            'Datos/Reportes GF BBVA/3T20.pdf',
            'Datos/Reportes GF BBVA/4T20.pdf']"""



def sacar_balance_bbva(modo):
    """list_bbva_balances_pdf = ['Datos/Reportes GF BBVA/2T20.pdf',
                                'Datos/Reportes GF BBVA/2T21.pdf']"""
    list_bbva_balances_pdf = [ File.objects.get(id=1).url_file, File.objects.get(id=5).url_file ]

    if modo == 'Activo':

        df_list = []
        for count, lista in enumerate(list_bbva_balances_pdf):
            df_list.append(extract_balance_BBVA(lista,count,modo))

        df_general = df_list[0].join(df_list[1][["Sep 2020", "Dic 2020", "Mar 2021", "Jun 2021"]])
        print(df_general)
        return df_general

    elif modo == "Pasivo":
        df_list = []
        for count, lista in enumerate(list_bbva_balances_pdf):
            df_list.append(extract_balance_BBVA(lista,count,modo))

        df_general = df_list[0].join(df_list[1][["Sep 10427082603", "Dic 10824022207", "Mar 11162000281", "Jun.1 11322012511"]])
        #print(df_general)
        return df_general
    
    elif modo == "Cuentas_Orden":
        user_inst_files = list(File.objects.filter(id__in=[4,1,5,2,3])
                            .values_list('url_file',flat=True))
        """list_bbva_pdf = ['Datos/Reportes GF BBVA/1T21.pdf',
        'Datos/Reportes GF BBVA/2T20.pdf',
            'Datos/Reportes GF BBVA/2T21.pdf',
            'Datos/Reportes GF BBVA/3T20.pdf',
            'Datos/Reportes GF BBVA/4T20.pdf']"""
        list_bbva_pdf = user_inst_files
        df_list = []
        for count, lista in enumerate(list_bbva_pdf):
            df_list.append(extract_balance_BBVA(lista,count,modo))
        df_1_g = df_list[0]
        df_2_g = pd.DataFrame(df_list[1][df_list[1].keys()[2]])
        df_3_g = pd.DataFrame(df_list[2][df_list[2].keys()[2]])
        df_4_g = pd.DataFrame(df_list[3][df_list[3].keys()[2]])
        df_5_g = pd.DataFrame(df_list[4][df_list[4].keys()[2]])
        df_general = df_1_g.join(df_2_g.join(df_3_g.join(df_4_g.join(df_5_g))))
        print(df_general)
        return df_general

    elif modo == "Resultados":
        df_list = []
        for count, lista in enumerate(list_bbva_balances_pdf):
            df_list.append(extract_balance_BBVA(lista,count,modo))

        df_general = df_list[0].join(df_list[1][["3T1", "4T1", "1T1", "2T.11"]])
        print(df_general)
        return df_general

    elif modo == "Estado de flujos":
        user_inst_files = list(File.objects.filter(id__in=[4,1,5,2,3])
                            .values_list('url_file',flat=True))
        list_bbva_pdf = user_inst_files
        """list_bbva_pdf = ['Datos/Reportes GF BBVA/1T21.pdf',
            'Datos/Reportes GF BBVA/2T20.pdf',
            'Datos/Reportes GF BBVA/2T21.pdf',
            'Datos/Reportes GF BBVA/3T20.pdf',
            'Datos/Reportes GF BBVA/4T20.pdf']"""
        df_list = []
        for count, lista in enumerate(list_bbva_pdf):
            print(count, lista)
            df_list.append(extract_balance_BBVA(lista,count,modo))

        df_1_g = df_list[0]
        df_2_g = pd.DataFrame(df_list[1][df_list[1].keys()[1]])
        df_3_g = pd.DataFrame(df_list[2][df_list[2].keys()[1]])
        df_4_g = pd.DataFrame(df_list[3][df_list[3].keys()[1]])
        df_5_g = pd.DataFrame(df_list[4][df_list[4].keys()[1]])
        df_general = df_1_g.join(df_2_g.join(df_3_g.join(df_4_g.join(df_5_g))))
        print(df_general)
        return df_general

    elif modo == "Estado de variaciones":
        """list_bbva_pdf = ['Datos/Reportes GF BBVA/1T21.pdf','Datos/Reportes GF BBVA/2T20.pdf',
            'Datos/Reportes GF BBVA/2T21.pdf','Datos/Reportes GF BBVA/3T20.pdf',
            'Datos/Reportes GF BBVA/4T20.pdf']"""
        user_inst_files = list(File.objects.filter(id__in=[4,1,5,2,3])
                            .values_list('url_file',flat=True))
        list_bbva_pdf = user_inst_files
        df_list = []
        for count, lista in enumerate(list_bbva_pdf):
            print(count, lista)
            print(extract_balance_BBVA(lista,count,modo))
            df_list.append(extract_balance_BBVA(lista,count,modo))
        return df_list
    
    elif modo == "Movimiento de cartera":
        """list_bbva_pdf = ['Datos/Reportes GF BBVA/1T21.pdf','Datos/Reportes GF BBVA/2T20.pdf',
            'Datos/Reportes GF BBVA/2T21.pdf','Datos/Reportes GF BBVA/3T20.pdf',
            'Datos/Reportes GF BBVA/4T20.pdf']"""
        user_inst_files = list(File.objects.filter(id__in=[4,1,5,2,3])
                            .values_list('url_file',flat=True))
        list_bbva_pdf = user_inst_files
        df_list = []
        for count, lista in enumerate(list_bbva_pdf):
            print(count, lista)
            print(extract_balance_BBVA(lista,count,modo))
            df_list.append(extract_balance_BBVA(lista,count,modo))
        return df_list

    elif modo == "Coeficiente de cobertura":
        """list_bbva_pdf = ['Datos/Reportes GF BBVA/1T21.pdf','Datos/Reportes GF BBVA/2T20.pdf',
            'Datos/Reportes GF BBVA/2T21.pdf','Datos/Reportes GF BBVA/3T20.pdf',
            'Datos/Reportes GF BBVA/4T20.pdf']"""
        user_inst_files = list(File.objects.filter(id__in=[4,1,5,2,3])
                            .values_list('url_file',flat=True))
        list_bbva_pdf = user_inst_files
        df_list = []
        for count, lista in enumerate(list_bbva_pdf):
            print(count, lista)
            print(extract_balance_BBVA(lista,count,modo))
            df_list.append(extract_balance_BBVA(lista,count,modo))
        return df_list


def sacar_balance_santander(modo):
    list_santander_balances_pdf = ['Datos/Reportes Santander/2T20.pdf',
                                'Datos/Reportes Santander/2T21.pdf']
    list_santander_balances_pdf = list(File.objects.filter(id__in=[9,13])
                            .values_list('url_file',flat=True))
    if modo == 'Activo':
        df_list = []
        for count, lista in enumerate(list_santander_balances_pdf):
            print(lista,count)
            df_list.append(extract_balance_santander(lista,count,modo))

        df_general = df_list[0].join(df_list[1][["Jun", "Mar", "Dic", "Sep"]])
        print(df_general)
        return df_general
    
    elif modo == 'Pasivo':
        df_list = []
        for count, lista in enumerate(list_santander_balances_pdf):
            print(lista,count)
            df_list.append(extract_balance_santander(lista,count,modo))

        df_general = df_list[0].join(df_list[1][["Jun", "Mar", "Dic", "Sep"]])
        print(df_general)
        return df_general

    elif modo == 'Cuentas_Orden':
        df_list = []
        for count, lista in enumerate(list_santander_balances_pdf):
            print(lista,count)
            df_list.append(extract_balance_santander(lista,count,modo))

        df_general = df_list[0].join(df_list[1][["Jun1", "Mar1", "Dic1", "Sep1"]])
        print(df_general)
        return df_general

    elif modo == 'Resultados':
        df_list = []
        for count, lista in enumerate(list_santander_balances_pdf):
            print(lista,count)
            df_list.append(extract_balance_santander(lista,count,modo))

        df_1 = df_list[0][['Unnamed: 00','20200','Unnamed: 30','Unnamed: 50','20190','Unnamed: 70','Unnamed: 8']]
        df_2 = df_list[1][['20211','Unnamed: 31','Unnamed: 51','20201']]
        df_general = df_1.join(df_2)
        print(df_general)
        return df_general
    
    elif modo == 'Estado de flujos':
        df_list = []
        list_santander_pdf = ['Datos/Reportes Santander/1T21.pdf','Datos/Reportes Santander/2T20.pdf',
            'Datos/Reportes Santander/2T21.pdf','Datos/Reportes Santander/3T20.pdf',
            'Datos/Reportes Santander/4T20.pdf']
        for count, lista in enumerate(list_santander_pdf):
            print(lista,count)
            
            df_list.append(extract_balance_santander(lista,count,modo))
        return df_list

    elif modo == "Estado de variaciones":
        list_bbva_pdf = ['Datos/Reportes Santander/1T21.pdf',
        'Datos/Reportes Santander/2T20.pdf',
            'Datos/Reportes Santander/2T21.pdf',
            'Datos/Reportes Santander/3T20.pdf',
            'Datos/Reportes Santander/4T20.pdf']
        list_bbva_pdf = list(File.objects.filter(
            id__in=[11,9,13,10,12])
                            .values_list('url_file',flat=True))
        df_list = []
        for count, lista in enumerate(list_bbva_pdf):
            print(count, lista)
            print(extract_balance_santander(lista,count,modo))
            df_list.append(extract_balance_santander(lista,count,modo))
        return df_list


    elif modo == "Coeficiente de cobertura":
        list_bbva_pdf = ['Datos/Reportes Santander/1T21.pdf','Datos/Reportes Santander/2T20.pdf',
            'Datos/Reportes Santander/2T21.pdf','Datos/Reportes Santander/3T20.pdf',
            'Datos/Reportes Santander/4T20.pdf']
        list_bbva_pdf = list(File.objects.filter(
            id__in=[11,9,13,10,12])
                            .values_list('url_file',flat=True))
        df_list = []
        for count, lista in enumerate(list_bbva_pdf):
            print(count, lista)
            df_list.append(extract_balance_santander(lista,count,modo))
        return df_list

def sacar_balance_banorte(modo):
    list_santander_balances_pdf = ['Datos/Reportes GF Banorte/2T20 Reporte trimestral.pdf',
                                'Datos/Reportes GF Banorte/2T21 Reporte trimestral.pdf']
    list_santander_balances_pdf = list(File.objects.filter(
            id__in=[7,16]).values_list('url_file',flat=True))
    print("hola banorte", list_santander_balances_pdf)
    if modo == 'Activo':
        df_list = []
        for count, lista in enumerate(list_santander_balances_pdf):
            print(lista,count)
            df_list.append(extract_balance_banorte(lista,count,modo))

        df_general = df_list[0].join(df_list[1][["Unnamed: 3 3T20", "Unnamed: 4 4T20", "Unnamed: 5 1T21", "Unnamed: 6 2T21"]])
        print(df_general)
        return df_general

    elif modo == 'Pasivo':
        df_list = []
        for count, lista in enumerate(list_santander_balances_pdf):
            print(lista,count)
            df_list.append(extract_balance_banorte(lista,count,modo))

        df_general = df_list[0].join(df_list[1][["Unnamed: 3 3T20", "Unnamed: 4 4T20", "Unnamed: 5 1T21", "Unnamed: 6 2T21"]])
        print(df_general)
        return df_general

    elif modo == 'Cuentas_Orden':
        df_list = []
        for count, lista in enumerate(list_santander_balances_pdf):
            print(lista,count)
            df_list.append(extract_balance_banorte(lista,count,modo))
        print(df_list[0])
        print(df_list[1])
        df_general = df_list[0].join(df_list[1][["Unnamed: 3 13T20", "Unnamed: 4 14T20", "Unnamed: 5 11T21", "Unnamed: 6 12T21"]])
        print(df_general)
        return df_general
    
    elif modo == 'Resultados':
        df_list = []
        for count, lista in enumerate(list_santander_balances_pdf):
            print(lista,count)
            df_list.append(extract_balance_banorte(lista,count,modo))

        df_general = df_list[0].join(df_list[1][["3T201", "4T201", "1T211", "2T211"]])
        print(df_general)
        return df_general

    elif modo == 'Estado de flujos':
        df_list = []
        list_santander_pdf = ['Datos/Reportes Santander/1T21.pdf',
        'Datos/Reportes Santander/2T20.pdf',
            'Datos/Reportes Santander/2T21.pdf',
            'Datos/Reportes Santander/3T20.pdf',
            'Datos/Reportes Santander/4T20.pdf']
        list_santander_pdf = list(File.objects.filter(
            id__in=[15,7,16,14,17])
                            .values_list('url_file',flat=True))
        for count, lista in enumerate(list_santander_pdf):
            print(lista,count)
            df_list.append(extract_balance_banorte(lista,count,modo))
        

        df_1_g = df_list[0]
        df_2_g = pd.DataFrame(df_list[1][df_list[1].keys()[1]])
        df_3_g = pd.DataFrame(df_list[2][df_list[2].keys()[1]])
        df_4_g = pd.DataFrame(df_list[3][df_list[3].keys()[1]])
        df_5_g = pd.DataFrame(df_list[4][df_list[4].keys()[1]])
        df_general = df_1_g.join(df_2_g.join(df_3_g.join(df_4_g.join(df_5_g))))
        print(df_general)

        return df_general

    elif modo == "Estado de variaciones":
        list_bbva_pdf = ['Datos/Reportes Santander/1T21.pdf','Datos/Reportes Santander/2T20.pdf',
            'Datos/Reportes Santander/2T21.pdf','Datos/Reportes Santander/3T20.pdf',
            'Datos/Reportes Santander/4T20.pdf']
        df_list = []
        list_santander_pdf = list(File.objects.filter(
            id__in=[15,7,16,14,17])
                            .values_list('url_file',flat=True))
        df_list = []
        for count, lista in enumerate(list_santander_pdf):
            print(lista,count)
            df_list.append(extract_balance_banorte(lista,count,modo))
        return df_list

    elif modo == "Coeficiente de cobertura":
        list_bbva_pdf = ['Datos/Reportes Santander/1T21.pdf','Datos/Reportes Santander/2T20.pdf',
            'Datos/Reportes Santander/2T21.pdf','Datos/Reportes Santander/3T20.pdf',
            'Datos/Reportes Santander/4T20.pdf']
        df_list = []
        list_santander_pdf = list(File.objects.filter(
            id__in=[15,7,16,14,17])
                            .values_list('url_file',flat=True))
        df_list = []
        for count, lista in enumerate(list_santander_pdf):
            print(lista,count)
            df_list.append(extract_balance_banorte(lista,count,modo))
        return df_list
#sacar_balance_bbva('Activo')
#sacar_balance_bbva('Pasivo')



def string2float(string_data):
    if type(string_data) != type('str'):
        if math.isnan(string_data):
          return 0.0
    else:
        string_data = string_data.replace(',','').replace('(','').replace(')','').replace('-','')
        if len(string_data) == 0:
            amount = 0
        else:
            amount = float(string_data)
        return amount


def create_detail_feature(feature, data_amounts,number_bank):
    bank = Institution.objects.get(id=number_bank)
    for index,data in enumerate(data_amounts):
        if number_bank == 1:
            season_id = index + 2
        else:
            season_id = index + 1
        if Season.objects.filter(id=season_id).exists():
            season = Season.objects.filter(id=season_id).last()
            detail_q = Detail.objects.filter(season=season,bank=bank)
            #print("--feature bbva")
            if detail_q.exists():
                list_details = list(detail_q.values_list('id',flat=True))
                detail_feature_q = DetailFeature.objects.filter(feature=feature,detail_id__in=list_details)
                if detail_feature_q.exists():
                    detail_feature = detail_feature_q.last()
                    detail = detail_feature.detail
                    #print('feature data if',string2float(data))
                    detail.amount = string2float(data)
                    #print('amount',detail.amount)
                    detail.save()
                else:
                    detail = Detail.objects.create(season=season,bank=bank,amount=string2float(data))
                    detail_feature = DetailFeature.objects.create(detail=detail,feature=feature)
            else:
                #print('feature data else',string2float(data))
                detail = Detail.objects.create(season=season,bank=bank,amount=string2float(data))
                detail_feature = DetailFeature.objects.create(detail=detail,feature=feature)

def create_detail_subfeature(subfeature, data_amounts,number_bank):
    bank = Institution.objects.get(id=number_bank)
    #print("--sub feature bbva", subfeature.name)
    #print(data_amounts)
    for index,data in enumerate(data_amounts):
        if number_bank == 1:
            season_id = index + 2
        else:
            season_id = index + 1
        if Season.objects.filter(id=season_id).exists():
            season = Season.objects.filter(id=season_id).last()
            detail_q = Detail.objects.filter(season=season,bank=bank)
            
            if detail_q.exists():
                list_details = list(detail_q.values_list('id',flat=True))
                detail_subfeature_q = DetailSubfeature.objects.filter(subfeature=subfeature,detail_id__in=list_details)
                if detail_subfeature_q.exists():
                    detail_subfeature = detail_subfeature_q.last()
                    detail = detail_subfeature.detail
                    #print('subfeature data if',string2float(data))
                    detail.amount = string2float(data)
                    #print('amount',detail.amount)
                    detail.save()
                else:
                    detail = Detail.objects.create(season=season,bank=bank,amount=string2float(data))
                    detail_subfeature = DetailSubfeature.objects.create(detail=detail,subfeature=subfeature)
            else:
                #print('subfeature data else',string2float(data))
                detail = Detail.objects.create(season=season,bank=bank,amount=string2float(data))
                detail_subfeature = DetailSubfeature.objects.create(detail=detail,subfeature=subfeature)