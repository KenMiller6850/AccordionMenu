from ReadConfig2 import getSQLCONFIG
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
import pandas as pd

from airium import Airium

currentDBName = 'NRTCUSTOMDB'
DBCaptureID = 27

configFilePath = r'C:\Users\akdmille\Documents\Python Files\configDEV72.ini'
params = ("DRIVER={SQL Server};SERVER=dev_72.sql.caresource.corp\dev_72;DATABASE=ChangeTracking;Trusted_Connection=yes")
dfExtractedTableslParamString = "EXEC [dbo].[usp_WBGetExtractedTables] @DatabaseName = N'" + currentDBName + "', @DBCaptureID = " + str(DBCaptureID) 


try:
   engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
   with engine.begin() as conn:
      print('Connected to database')
      dfExtractedTables = pd.DataFrame(conn.execute(dfExtractedTableslParamString))   
      dfNonStandard = dfExtractedTables[dfExtractedTables['TABLE_SCHEMA'].str.contains('CARESOURCE')]
      dfFinal = pd.concat([dfNonStandard, dfExtractedTables]).drop_duplicates(keep=False)

except SQLAlchemyError as e:
  error = str(e.__dict__['orig'])
  print('database error ', e.args)
  print('Database connection error')  
  engine.dispose   
  
  
a = Airium()

a('<!DOCTYPE html>')
with a.html(klass='no-js', dir='ltr', lang='en'):
    with a.head():
        a.meta(charset='utf-8')
        a.meta(content='ie=edge', **{'http-equiv': 'x-ua-compatible'})
        a.meta(content='width=device-width, initial-scale=1.0', name='viewport')
        a.title(_t='CareSource Database Change Tracking')
        a.link(href='style/foundation.css', rel='stylesheet')
        a.link(href='style/app.css', rel='stylesheet')
        a.link(href='style/custom.css', rel='stylesheet')
        a.link(href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css', rel='stylesheet')
        a.link(href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.7.2/css/all.min.css', rel='stylesheet')
    with a.body(style='background-color:#374d63;'):
        with a.div(klass='grid-container', style='color:#cacfd4;'):
            with a.div(klass='grid-x grid-padding-x'):
                with a.div(klass='large-12 cell'):
                    a.h1(_t='CareSource Change Tracking')
            with a.div(id='header', style='width:500px;'):
                with a.div(klass='row'):
                    with a.div(klass='columns'):
                        a.p(_t='Use this to monitor changes in databases that may lead to issues with reporting, etc..')
                with a.ul(klass='vertical menu accordion-menu', **{'data-accordion-menu': ''}):
                    with a.li():
                        a.a(href='https://get.foundation/', target='_blank', _t='DEV 72')
                        with a.ul(klass='menu vertical nested'):
                            with a.li():
                                a.a(href='#', _t='NRTCUSTOMDB')
                                with a.ul(klass='menu vertical nested'):
                                    with a.li():
                                        a.a(href='#', _t='Tables')
                                        
                                        
                                        with a.ul(klass='menu vertical nested'):
                                        
                                            with a.li():
                                                
                                                i = 0
                                                while i < len(dfFinal.index):
                                                   DBName = dfFinal.iloc[i, dfFinal.columns.get_loc('TABLE_CATALOG')]
                                                   SchemaName = dfFinal.iloc[i, dfFinal.columns.get_loc('TABLE_SCHEMA')]
                                                   TableName = dfFinal.iloc[i, dfFinal.columns.get_loc('TABLE_NAME')]
                                                   ChangedFlag = dfFinal.iloc[i, dfFinal.columns.get_loc('ChangedFlag')]
                                                   
                                                   ChangeString = "href='User_databases\\NRTCUSTOMDB\\Tables\\" +  TableName + ".html', target='DATA' class=" +'"' + 'tablechange' +'"' 
                                                   NormalString = "href='User_databases\\NRTCUSTOMDB\\Tables\\" +  TableName + ".html', target='DATA'"
                                                   
                                                   if ChangedFlag == 0:
                                                      with a.a(NormalString):
                                                        a(SchemaName + '.' + TableName)
                                                   
                                                   if ChangedFlag == 1:                                                
                                                      with a.a(ChangeString):
                                                        a(SchemaName + '.' + TableName)
                                                        
                                                   i += 1 
                                                

    #print("href='User_databases\\NRTCUSTOMDB\\Tables\\" + TableName + ".html', target='DATA'")  #+ ' + ', target=''DATA')
    
    
    #href='User_databases\\NRTCUSTOMDB\\Tables\\Network_Ops_Provider_Network_Prefix_Info.html', target='DATA'
    
    
    #fw.CreateHTMLPage(DBName,SchemaName,TableName)
    

                                                

        a.script(src='scripts/vendor/jquery.js')
        a.script(src='scripts/vendor/what-input.js')
        a.script(src='scripts/vendor/foundation.js')
        a.script(src='scripts/app.js')


if __name__ == '__main__':
    html = str(a) # casting to string extracts the value

#print(html)

with open('C:\\Users\\akdmille\\Documents\\Python Files\\AccordionMenuBuilder\\index.html', 'wb') as f:
        f.write(bytes(html, encoding="utf-8")) 

