# demo_evaluate.py
import sys
import asyncio
from typing import List
from models.metric import MetricDefinition
from core.evaluater import evaluate_all_conversations
import nest_asyncio


original_apply = nest_asyncio.apply

def patched_apply(*args, **kwargs):
    if not getattr(patched_apply, "applied", False):
        original_apply(*args, **kwargs)
        patched_apply.applied = True

nest_asyncio.apply = patched_apply


nest_asyncio.apply()

async def main():
    correctness_metric = MetricDefinition.from_json(
        r"C:\Users\steqi\Documents\llm-evaluation\tests\data\metrics\correctness.json"
    )
    metrics: List[MetricDefinition] = [correctness_metric]


    file_path = r"tests\data\conversation\Result-YepAI.csv"

    results = await evaluate_all_conversations(file_path=file_path, metrics=metrics)


    for r in results:
        print(f"ConversationID: {r.ConversationID}")
        print(f"Content: {r.ConversationContent}")
        print(f"Scores: {r.scores}")
        print(f"reasons: {r.reasons}")
        print("------")
    print(1)

if __name__ == "__main__":
    asyncio.run(main())
