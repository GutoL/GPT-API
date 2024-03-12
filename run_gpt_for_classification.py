import pandas as pd
import json
from code.gpt_class import ChatGPT
import sys


assert len(sys.argv) == 4, "Please, run the code: python run_gpt_for_classification.py <year> <batch> <key_name>"


chat_gpt_keys = json.load(open('config/open_ai_keys.json'))
chatgpt_client = ChatGPT(api_key=chat_gpt_keys[sys.argv[3]], model_name='gpt-3.5-turbo-1106') # 'gpt-4-1106-preview', 'gpt-3.5-turbo' 'gpt-3.5-turbo-1106'

with open('prompts/hate_speech_prompt.txt', 'r') as file:
    prompt = file.read()

text_column = 'text'
path = '../../' # local
year = sys.argv[1]
batch_index = sys.argv[2]

if year in ['2008','2012', '2016', '2020']:
    gender = 'men'
else:
    gender = 'women'

print('****', year)

df = pd.read_csv(path+'datasets/Euros/'+gender+'/'+year+'/euro_'+str(year)+'_no_rt_batch_'+batch_index+'.csv')

print('Originally, the dataset has', df.shape[0], 'rows')

df.dropna(subset=[text_column], inplace=True)
df.drop_duplicates(subset=[text_column], inplace=True)
df.reset_index(inplace=True)

print('After remove duplicates and NaN, the dataset has', df.shape[0], 'rows')

general_results_file_name = path+'results/chatGPT/Euros/'+year+'/'+'all_results_'+year+'_with_id.csv'
bacth_results_file_name = path+'results/chatGPT/Euros/'+year+'/'+'all_results_'+year+'_with_id_batch_'+batch_index+'.csv'

chatgpt_client.classify_dataframe_2(prompt=prompt, data_frame=df, general_results_file_name=general_results_file_name,
                                    bacth_results_file_name=bacth_results_file_name, batch_size=50, 
                                    resulting_columns=['is_hate_speech', 'hate_speech_type', 'explanation'],
                                    text_column='text', id_column='id')