import pandas as pd

column_name = ['BANK', 'IFSC', 'MICR', 'BRANCH', 'ADDRESS', 'CITY1', 'CITY 2', 'STATE', 'STD CODE2', 'PHONE']

def create_data_dict(df):    
    data = {row['IFSC'] : { column : row[column] for column in column_name  }for i, row in df.iterrows()}
    return data

def create_bank_lead_board(df):
    lead  = df.groupby('BANK').size()
    data = lead.to_dict()
    return data

def main( dataset ):
    data_dict = create_data_dict(dataset)
    # print(data_dict)/
    bank_lead = create_bank_lead_board(dataset)
    return data_dict , bank_lead