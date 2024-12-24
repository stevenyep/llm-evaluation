# models/evaluater.py

import asyncio
from typing import List, Dict
import pandas as pd
from pydantic import BaseModel

from deepeval.test_case import ConversationalTestCase, LLMTestCase, LLMTestCaseParams
from deepeval.metrics import ConversationalGEval
from models.metric import MetricDefinition
from .preprocessing import preprocess_csv

class EvaluationResult(BaseModel):
    ConversationID: str
    ConversationContent: str
    scores: Dict[str, float]
    reasons: Dict[str, str]


async def evaluate_single_conversation(
    convo_id: str,
    df: pd.DataFrame,
    metrics: List[MetricDefinition]
) -> EvaluationResult:

    turns = []
    conversation_content = []
    user_input = None

    for _, row in df.iterrows():
        if row['Role'] == 'user':
            user_input = row['Content']
            conversation_content.append(f"User: {user_input}")
        elif row['Role'] == 'assistant' and user_input:
            turns.append(
                LLMTestCase(input=user_input, actual_output=row['Content'])
            )
            conversation_content.append(f"Assistant: {row['Content']}")
            user_input = None  

    if not turns:
        return EvaluationResult(
            ConversationID=convo_id,
            ConversationContent="\n".join(conversation_content),
            scores={},
            reasons={}
        )

    test_case = ConversationalTestCase(turns=turns)

    scores = {}
    reasons = {}
    for metric in metrics:
        from deepeval.metrics import ConversationalGEval
        eval_metric = ConversationalGEval(
            name=metric.name,
            criteria=metric.criteria,
            evaluation_steps=metric.evaluation_steps,
            evaluation_params=metric.evaluation_params,
        )
        eval_metric.measure(test_case)  
        scores[metric.name] = eval_metric.score
        reasons[metric.name] = eval_metric.reason

    return EvaluationResult(
        ConversationID=convo_id,
        ConversationContent="\n".join(conversation_content),
        scores=scores,
        reasons=reasons
    )


async def evaluate_all_conversations(
    file_path: str,
    metrics: List[MetricDefinition],
    limit: int = 50,
    **kwargs
) -> List[EvaluationResult]:

    conversation_dict: Dict[str, pd.DataFrame] = await preprocess_csv(file_path, **kwargs)

    tasks = []
    for convo_id in conversation_dict.keys():
        tasks.append(
            evaluate_single_conversation(convo_id, conversation_dict[convo_id], metrics)
        )

    results = await asyncio.gather(*tasks)
    return list(results)
