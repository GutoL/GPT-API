import pandas as pd
import time
import os
from openai import OpenAI
import json

class ChatGPT():

    def __init__(self, api_key, model_name='gpt-4-1106-preview'):

        self.api_key = api_key
        self.model_name = model_name # 'gpt-4-1106-preview', #"gpt-3.5-turbo" "gpt-4"


    def text_classify_chatgpt_several_texts_simultaneously(self, text_list, prompt):
        # Setting the API key
        client = OpenAI(api_key=self.api_key)

        messages_list = [{"role": "system", "content": prompt}]

        for i, text in enumerate(text_list):
            message = {"role":"user", "content":str(i+1)+": ```"+text+"```"}
            messages_list.append(message)


        completion = client.chat.completions.create(
            model=self.model_name,
            messages=messages_list
        )

        print(completion)

        chat_gpt_classification = pd.DataFrame(json.loads(completion.choices[0].message.content))

        return chat_gpt_classification
    

    def text_classify_chatgpt_one_text_add_id(self, id_list, text_list, prompt, resulting_columns):

        # Setting the API key
        client = OpenAI(api_key=self.api_key)

        df_chatgpt = pd.DataFrame(columns=['id','text']+resulting_columns)

        for i, text in enumerate(text_list):
            text = text.replace('\\', '')

            print('_________________________________________')
            print(text)

            completion = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role":"user", "content":"```"+text+"```"}
                ],
                temperature=0.2
            )

            # print(i, completion)
            print(i, completion.choices[0].message.content)

            # chatgpt_classification = json.loads(completion.choices[0].message.content)
            if '||' not in completion.choices[0].message.content:
                chatgpt_classification = [None]*len(resulting_columns)
            else:
                chatgpt_classification = completion.choices[0].message.content.split('||')

            data = {
                    'id': [id_list[i]],
                    'text':[text],
                    # 'classification':[chatgpt_classification['Classification']],
                    # 'explanation':[chatgpt_classification['Explanation']]
                  }

            for x, col in enumerate(resulting_columns):
                # data[col] = [chatgpt_classification[col]]
                data[col] = [chatgpt_classification[x]]

            df_chatgpt = pd.concat([df_chatgpt, pd.DataFrame.from_dict(data)])

        return df_chatgpt  
     

    def text_classify_chatgpt_one_text(self, text_list, prompt, resulting_columns):
        # Setting the API key
        client = OpenAI(api_key=self.api_key)

        df_chatgpt = pd.DataFrame(columns=['text']+resulting_columns)

        for i, text in enumerate(text_list):
            text = text.replace('\\', '')
            print('-----------------------------')
            print(text)

            completion = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role":"user", "content":"```"+text+"```"}
                ],
                temperature=0.2
            )

            # print(i, completion)
            print(i, completion.choices[0].message.content)

            # chatgpt_classification = json.loads(completion.choices[0].message.content)
            chatgpt_classification = completion.choices[0].message.content.split('||')

            data = {
                    'text':[text],
                    # 'classification':[chatgpt_classification['Classification']],
                    # 'explanation':[chatgpt_classification['Explanation']]
                  }

            for x, col in enumerate(resulting_columns):
                # data[col] = [chatgpt_classification[col]]
                data[col] = [chatgpt_classification[x]]

            df_chatgpt = pd.concat([df_chatgpt, pd.DataFrame.from_dict(data)])

        return df_chatgpt


    def classify_dataframe(self, prompt, data_frame, batch_size, results_path, resulting_columns, text_column='Document', 
                           classify_one_text_per_time=True, start_index=0, end_index=None, id_column=None):

        if end_index is None:
            end_index = data_frame.shape[0]

        for i in range(start_index, end_index, batch_size):

            first_index = i
            second_index = i+batch_size

            results_file_name = results_path+str(first_index)+'_'+str(second_index)+'.xlsx'

            if os.path.isfile(results_file_name):
                print('Skipping', results_file_name)
                continue

            print('Classifying between', first_index, 'and', second_index)

            text_list = list(data_frame.iloc[first_index:second_index][text_column].values)

            if classify_one_text_per_time:
                if id_column:
                    id_list = list(data_frame.iloc[first_index:second_index][id_column].values)
                    df_chatgpt = self.text_classify_chatgpt_one_text_add_id(id_list=id_list, text_list=text_list, prompt=prompt, resulting_columns=resulting_columns)
                else:    
                    df_chatgpt = self.text_classify_chatgpt_one_text(text_list=text_list, prompt=prompt, resulting_columns=resulting_columns)
            else:
                df_chatgpt = self.text_classify_chatgpt_several_texts_simultaneously(text_list=text_list, prompt=prompt, columns=['text','classification','explanation'])

            df_chatgpt.to_excel(results_file_name, index=False)
            time.sleep(3)

        return df_chatgpt
    
    def classify_dataframe_2(self, prompt, data_frame, general_results_file_name, bacth_results_file_name, batch_size, resulting_columns, 
                             text_column='Document', id_column='id'):
        
        df_results_general = pd.read_csv(general_results_file_name, sep=';')

        if os.path.isfile(bacth_results_file_name):
            df_results_batch = pd.read_csv(bacth_results_file_name, sep=';')
        else:
            df_results_batch = pd.DataFrame()
        
        df_results = pd.concat([df_results_general, df_results_batch], axis=0)

        data_frame[id_column] = data_frame[id_column].astype(int)
        df_results[id_column] = df_results[id_column].astype(int)

        df_results.drop_duplicates(subset=[id_column], inplace=True)


        column_to_filter = text_column # id_column

        values_in_results = set(df_results[column_to_filter])

        print('Already classified', len(values_in_results), 'texts')

        df_to_classify = data_frame[~data_frame[column_to_filter].isin(values_in_results)]

        if df_to_classify.shape[0] > 0:
            print('Classifying', df_to_classify.shape[0], 'texts...')

            for i in range(0, df_to_classify.shape[0], batch_size):

                first_index = i
                second_index = i+batch_size

                text_list = list(df_to_classify.iloc[first_index:second_index][text_column].values)
                id_list = list(df_to_classify.iloc[first_index:second_index][id_column].values)

                df_chatgpt = self.text_classify_chatgpt_one_text_add_id(id_list=id_list, text_list=text_list, prompt=prompt, resulting_columns=resulting_columns)

                df_results_batch = pd.concat([df_results_batch, df_chatgpt], axis=0)

                print('Saving more', batch_size, 'texts', second_index, '/', df_to_classify.shape[0])
                print(bacth_results_file_name)
                df_results_batch.to_csv(bacth_results_file_name, index=False, sep=';')
                time.sleep(2)
        else:
            print('There is no text to classify!')