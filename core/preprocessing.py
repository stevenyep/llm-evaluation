import asyncio
import pandas as pd
from typing import Dict
from dotenv import load_dotenv
import os

load_dotenv() 

async def preprocess_csv(file_path: str, **kwargs) -> Dict[str, pd.DataFrame]:

    loop = asyncio.get_event_loop()

    def _read_csv() -> pd.DataFrame:
        return pd.read_csv(file_path,
                           header=None,  
                           names=['Content', 'ConversationID', 'UserIP', 'Role'], 
                           dtype={'ConversationID': str},  
                           encoding='utf-8',  
                           sep=',',  
                           engine='python'  
        )

    df = await loop.run_in_executor(None, _read_csv)

    df = df.iloc[::-1].reset_index(drop=True)
    df = df.drop_duplicates(keep='first').reset_index(drop=True)

    grouped = df.groupby('ConversationID', as_index=False)

    def filter_func(x: pd.DataFrame) -> bool:
        return (len(x) % 2 == 0) and (not x['Content'].isnull().any())

    filtered_df = grouped.filter(filter_func)

    def has_consecutive_roles(sub_df: pd.DataFrame) -> bool:
        return not (sub_df['Role'] == sub_df['Role'].shift()).any()

    filtered_df = filtered_df.groupby('ConversationID').filter(has_consecutive_roles)

    filtered_df = filtered_df.reset_index(drop=True)

    conversation_dict: Dict[str, pd.DataFrame] = {}
    for conversation_id, group_df in filtered_df.groupby('ConversationID'):
        conversation_dict[conversation_id] = group_df.reset_index(drop=True)

    return conversation_dict
