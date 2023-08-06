import pymysql
import pandas as pd
import numpy as np


def generate_insert_values(input_list):

    for index, element in enumerate(input_list):
        #the element could be float, int, or str. date is converted into str

        #for float, check np.nan, and convert nan to None
        if isinstance(element, float):

            if np.isnan(element):
                input_list[index]=None

        #for int, do nothing
        elif isinstance(element, int):
            input_list[index]=input_list[index]

        #for str, if it is str, convert encoding to utf-8
        else:
            input_list[index] = input_list[index].encode('utf-8')

    return input_list

#load_table_encoding() take care of NaN issues of pandas, so we don't have to update by column after inserting all the data into database table
def load_table_encoding(host, port, user, passwrod, database, insert_statement, pd_dataset):
    cnn = pymysql.connect(host=host, port=port, user=user,
                          passwd=passwrod, db=database)

    cur = cnn.cursor()

    # insert into database
    rows = pd_dataset.values.tolist()

    for index, row in enumerate(rows):

        rows[index]=generate_insert_values(row)

    cur.executemany(insert_statement, rows)
    cnn.commit()

    cur.close()
    cnn.close()

    return

def drop_table(table_name, host, port, user, password, database):
    cnn=pymysql.connect(host=host,port=port, user=user, passwd=password, db=database)

    cur=cnn.cursor()

    statement='''drop table if exists '''+table_name

    cur.execute(statement)

    cur.close()
    cnn.close()

    return


def create_table_customized(table_name, table_data, host,port, user, password, database):

    print ('creating the table...')

    cnn=pymysql.connect(host=host,port=port, user=user, passwd=password, db=database)

    cur=cnn.cursor()

    df=table_data

    file_name=table_name

    field_names=df.dtypes.index
    field_types=df.dtypes.values
    field_number=len(df.dtypes)


    df_data_type=pd.read_sql('select * from MASTER_SCHEMA_MAPPING_NS', cnn)

    df_data_type=df_data_type.drop('SYSTEM_ID',axis=1)

    #print (df_data_type)

    statement_prefix='''
    create table if not exists 
    ''' + file_name + '''( SYSTEM_ID int NOT NULL AUTO_INCREMENT UNIQUE, '''

    statement_middle=''

    for index in range(0, field_number):

        attr_name='`'+field_names[index]+'`'

        if field_names[index] in df_data_type['NS_ATTRIBUTE'].tolist():

            for row_index, row in df_data_type.iterrows():

                if row['NS_TABLE_NAME']==table_name and row['NS_ATTRIBUTE']==field_names[index]:

                    statement_middle=statement_middle+' '+row['MYSQL_ATTRIBUTE']+' '+row['DATA_TYPE']+','
        else:

            print(attr_name, 'hasn\'t been defined in the MASTER_SCHEMA_MAPPING_GOOGLE table in MySQL')

            return

    statement_suffix='''
    primary key(SYSTEM_ID))
    '''

    statement_full=statement_prefix+statement_middle+statement_suffix

    #add the constrain module in table creation process
    # statement_constrained=create_table_constrains(table_name,statement_full)

    statement_constrained=statement_full

    print (statement_constrained)

    cur.execute(statement_constrained)

    print ('table is successfully created')

    cur.close()
    cnn.close()

    return



def import_data(table_name, table_data, host, port, user, password, database):

    print ('loading the data...')

    cnn=pymysql.connect(host=host,port=port, user=user, passwd=password, db=database)

    df=table_data

    field_names=df.dtypes.index
    # field_types=df.dtypes.values
    field_number=len(df.dtypes)

    df_data_type=pd.read_sql('select * from MASTER_SCHEMA_MAPPING_NS', cnn)

    df_data_type=df_data_type.drop('SYSTEM_ID',axis=1)

    statement_prefix='''insert into '''+ table_name +''' ('''

    statement_middle_1=''

    for index in range(0, field_number):

        attr_name='`'+field_names[index]+'`'

        if field_names[index] in df_data_type['NS_ATTRIBUTE'].tolist():

            for row_index, row in df_data_type.iterrows():

                if row['NS_TABLE_NAME']==table_name and row['NS_ATTRIBUTE']==field_names[index]:
                    statement_middle_1=statement_middle_1+row['MYSQL_ATTRIBUTE']+','
        else:

            print(attr_name, 'hasn\'t been defined in the MASTER_SCHEMA_MAPPING_GOOGLE table in MySQL')

            return

    #get rid of the last ','
    statement_middle_1=statement_middle_1[:-1]

    statement_middle_2=''') value ('''

    statement_middle_3=''

    for index in range(0, field_number):
        statement_middle_3=statement_middle_3+'%s,'

    statement_middle_3=statement_middle_3[:-1]

    statement_suffix=''')'''

    insert_statement=statement_prefix+statement_middle_1+statement_middle_2+statement_middle_3+statement_suffix

    cnn.close()

    print (insert_statement)

    load_table_encoding(host, port, user, password, database, insert_statement, df)

    print ('data is successfully loaded')

    return


#this method creates a table in mysql database from a dataframe, and then import the data from the dataframe as well, it works with dataframe that doesn't have a long string
#data_source: 'NS', 'WOO', 'GOOGLE',  or 'Other'
def load_into_mysql_dataframe(table_name, path, host, port, user, password, database):

    df=pd.read_csv(path)

    drop_table(table_name, host, port, user, password, database)

    create_table_customized(table_name, df, host, port, user, password, database)

    import_data(table_name, df, host, port, user, password, database)

    return

load_into_mysql_dataframe('NS_DOWNLOAD', '/Users/haoguoxuan/Documents/updated_data/net_suite_download.csv', 'abs01100.cebepnjwfkfe.us-west-1.rds.amazonaws.com', 3306, 'abs', '2VB3&2riK!pO', 'abs')
