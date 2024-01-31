import pandas as pd
import os
from glob import glob
import sys
import re

assert len(sys.argv) == 2, "Please, run the code: python temp_compile.py <year>"


year = sys.argv[1]
path = '../../'

if year in ['2008','2012', '2016', '2020']:
    gender = 'men'
else:
    gender = 'women'

## compiling all the files that GPT already classified
# ---------------------------------------------------------------------------------------------------------

# number_of_files = 0
# path += 'results/chatGPT/Euros/'

# if number_of_files > 0:
#     results_df = pd.DataFrame()

#     for i in range(number_of_files):
#         for j, file_name in enumerate(glob(path+year+'_'+str(i+1)+'/*.xlsx')):
#             print('Reading:',j, file_name)
#             results_df = pd.concat([results_df, pd.read_excel(file_name)], axis=0)

#             results_df.drop_duplicates(subset=['text'], inplace=True)
        
#     results_df.to_csv(path+'all_results_'+year+'.csv', index=False)

# else:
#     results_df = pd.DataFrame()

#     for j, file_name in enumerate(glob(path+year+'/*.xlsx')):
#         print('Reading:',j, file_name)
#         results_df = pd.concat([results_df, pd.read_excel(file_name)], axis=0)

#         results_df.drop_duplicates(subset=['text'], inplace=True)
    
# results_df.to_csv(path+'all_results_'+year+'.csv', index=False)


## Getting the ID column from the original Euro datasets and adding this column into the datasets that were classified by GPT
# ---------------------------------------------------------------------------------------------------------

# def extract_id(string):
#     pattern = r'ObjectId\((\w{24})\)'
#     match = re.match(pattern, string)
#     if match:
#         return match.group(1)
#     else:
#         return None
    
# def merge_id(df_original, df_classifications):
   
#     df_original['text'] = df_original['text'].str.replace('\\', '')
#     df_classifications['text'] = df_classifications['text'].str.replace('\\', '')

#     # df_original['id'] = df_original['id'].astype(int)
    
#     # Merge the dataframes based on the 'text' column
#     merged_df = pd.merge(df_classifications, df_original[['text', 'id']], on='text', how='left')

#     merged_df.drop_duplicates(subset=['text'], inplace=True)
#     # merged_df.dropna(subset=['id'], inplace=True)

#     # merged_df['id'] = merged_df['id'].astype(int)

#     return merged_df

# df_original = pd.read_csv(path+'datasets/Euros/'+gender+'/euro_'+year+'_no_rt.csv')
# df_classifications = pd.read_csv(path+'results/chatGPT/Euros/'+year+'/all_results_'+year+'.csv')

# if year == '2020':
#     df_original['id'] = df_original['id'].apply(extract_id)

# new_df_classifications = merge_id(df_original, df_classifications)

# print(df_original.shape)
# print(df_classifications.shape)
# print(new_df_classifications.shape)

# new_df_classifications.to_csv(path+'results/chatGPT/Euros/'+year+'/all_results_'+year+'_with_id.csv',index=False, sep=';')


## Split the complete data sets
# ----------------------------------------------------------------------------------------------------------------------------------------
    
df_original = pd.read_csv(path+'datasets/Euros/'+gender+'/'+year+'/euro_'+year+'_no_rt.csv')
batch_size = 100000

batches = [df_original[i:i + batch_size] for i in range(0, len(df_original), batch_size)]

for i, batch in enumerate(batches):
    batch_file_name = path+'datasets/Euros/'+gender+'/'+year+'/euro_'+year+'_no_rt_batch_'+str(i+1)+'.csv'
    print(batch_file_name, batch.shape)
    batch.to_csv(batch_file_name, index=False)

