import pandas as pd
import numpy as np
import re

class clean:
    def __init__(self,data):
        self.data = data
    def clean_number(self,decimal=0,dealnull='mean'):
        flt="%."+str(decimal)+"f"
        flt2='{:.'+str(decimal)+'f}'
        pd.set_option('display.float_format', flt2.format)
        def clean_num_process(pass_data): # This function does the cleaning
            x = str(pass_data)
            if x=='nan':
                return pass_data
            else:
                new_string = re.sub("[ ,'?/\@#&*!%$]",'',x)
                try:
                    return flt %float(new_string)
                except:
                    new_string = re.sub(r"[a-z]", "", new_string, flags = re.I)
                    print(f'value {x} at INDEX : {x.index} \t replaced as {new_string}')
                    try:
                        return flt %float(new_string)
                    except:
                        print('Yove passed non-numerical data which cannot be cleaned unless there is atleast 1 numerical number')
        def num_dealnull(data,how,mean=0,median=0): #This function deals with all the null values
            if how=='delete':
                data=data.dropna()
            elif how=='zero':
                data=data.fillna(0)
            elif how=='fill_prev':
                data= data.ffill()
            elif how=='fill_next':
                data= data.bfill()
            elif how=='mean':
                data= data.fillna(mean)
            elif how=='median':
                data= data.fillna(median)
            return data
        #----------Checks to see if user passed Dataframe or Series then calls cleaning function above--------------
        if 'DataFrame' in str(type(self.data)):
            print('Data passed as : dataframe')
            for i in self.data.columns:
                self.data[i]= self.data[i].map(clean_num_process)
            if self.data.isnull().sum().any():
                null_excluded = self.data[~self.data.isnull()]
                nexm = null_excluded.astype(float).mean()
                nexmed = null_excluded.astype(float).median()
                self.data = num_dealnull(self.data,dealnull,nexm,nexmed)
            self.data = self.data.astype(float)
            return self.data
        elif 'Series' in str(type(self.data)):
            print('Data passed as : Series')
            copy_df =  self.data.map(clean_num_process)
            if copy_df.isnull().sum()>0:
                null_excluded = copy_df[~copy_df.isnull()]
                nexm = null_excluded.astype(float).mean()
                nexmed = null_excluded.astype(float).median()
                copy_df = num_dealnull(copy_df,dealnull,nexm,nexmed)
            copy_df = copy_df.astype(float)
            return copy_df
        else:
            print('ERROR : please pass data as a pandas Series or DataFrame')
        
    def num_summary(self): # This function gives back summary of data
        if 'Series' in str(type(self.data)):
            print(f'\nType of data : {self.data.dtype} ')
            print('\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
            print(f'\nTotal number of rows : {self.data.shape[0]} ')
            print('\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
            print(f'Total number of unique values : {self.data.nunique()} ')
            print('\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
            print(f'Total number Null values : {self.data.isnull().values.sum()} ')
            print('\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
            dupli=None
            if self.data.duplicated().any():
                dup = self.data[self.data.duplicated()]
                print(f'Duplications found')
                dupli=dup.index
                print('\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
            return {'duplicates':dupli,'nullvalues':self.data[self.data.isnull().values].index}
        else:
            print('Data should be passed as a Series')
        
    def num_length(self): # This function gives back the length of each numerical values in data
        if str(self.data.dtype) in ['float64','int64','int32']:    
            if 'Series' in str(type(self.data)):
                length = self.data.map(lambda x: len(str(int(x))))
                return length
            else:
                print('ERROR : Can only pass series')
        else:
            print('ERROR : Please make sure the data passed is either float or int')