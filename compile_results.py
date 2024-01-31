import pandas as pd
import os

year = ['2022_1', '2022_2']

path = '../../'


if year[0] in ['2012', '2016_1', '2020_1']:
    gender = 'men'
else:
    gender = 'women'


df_result = pd.DataFrame()

for y in year:
    file_name = path+'datasets/Euros/'+gender+'/euro_'+str(y)+'_no_rt.csv'
    df_result = pd.concat([df_result, pd.read_csv(file_name)])

df_result.drop_duplicates(subset=['text'], inplace=True)

print('total of tweets:', df_result.shape)

# --------------------------------------------------------------------------------------------------------------

path = '../../'+'results/chatGPT/Euros/'

path_results = path+str(year[0])+'/'

compiled_file_name = path+str(year[0])+'/'+'all_tweets_'+str(year[0])

count = 0
number_of_tweets = 0

df_result = pd.DataFrame()

for file_name in os.listdir(path_results):
    if '.xlsx' not in file_name:
        continue

    df = pd.read_excel(path_results+file_name)

    df_result = pd.concat([df_result, df])

    number_of_tweets += df.shape[0]

    # if df_result.shape[0] >= 1000000:
    #     df_result.drop_duplicates(subset=['text'], inplace=True)
    #     df_result.to_csv(compiled_file_name+'_'+str(count)+'.csv', index=False)
    #     df_result = pd.DataFrame()
    #     count += 1

print('***', year)
print(df_result.shape)
print('number_of_tweets', number_of_tweets)

if df_result.shape[0] > 0:
    df_result.drop_duplicates(subset=['text'], inplace=True)
    print('After remove duplicates:', df_result.shape)
    df_result.to_csv(compiled_file_name+'_'+str(count)+'.csv', index=False)