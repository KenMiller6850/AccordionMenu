
from ReadConfig2 import getSQLCONFIG
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
import pandas as pd


currentDBName = 'NRTCUSTOMDB'
DBCaptureID = 27

configFilePath = r'C:\Users\akdmille\Documents\Python Files\configDEV72.ini'
params = ("DRIVER={SQL Server};SERVER=dev_72.sql.caresource.corp\dev_72;DATABASE=ChangeTracking;Trusted_Connection=yes")
dfExtractedTableslParamString = "EXEC [dbo].[usp_WBGetExtractedTables] @DatabaseName = N'" + currentDBName + "', @DBCaptureID = " + str(DBCaptureID) 

#print (dfExtractedTableslParamString)

try:
   engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
   with engine.begin() as conn:
      print('Connected to database')
      dfExtractedTables = pd.DataFrame(conn.execute(dfExtractedTableslParamString))   

except SQLAlchemyError as e:
  error = str(e.__dict__['orig'])
  print('database error ', e.args)
  print('Database connection error')  
  engine.dispose   

print(dfExtractedTables)

                                
i = 0
while i < len(dfExtractedTables.index):
    DBName = dfExtractedTables.iloc[i, dfExtractedTables.columns.get_loc('TABLE_CATALOG')]
    SchemaName = dfExtractedTables.iloc[i, dfExtractedTables.columns.get_loc('TABLE_SCHEMA')]
    TableName = dfExtractedTables.iloc[i, dfExtractedTables.columns.get_loc('TABLE_NAME')]
    print("href='User_databases\\NRTCUSTOMDB\\Tables\\" + TableName + ".html', target='DATA'")  #+ ' + ', target=''DATA')
    
    
    #href='User_databases\\NRTCUSTOMDB\\Tables\\Network_Ops_Provider_Network_Prefix_Info.html', target='DATA'
    
    
    #fw.CreateHTMLPage(DBName,SchemaName,TableName)
    i += 1 

                                    
                                    


#fw.CreateHTMLPage('NRTCUSTOMDB','dbo','Facets_ProviderSetupQualityCheck_Audit_Stg')

