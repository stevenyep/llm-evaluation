# tests/test_evaluater.py
# conftest.py or your test setup file
import nest_asyncio
import pytest

@pytest.fixture(autouse=True)
def apply_nest_asyncio():
    nest_asyncio.apply()

import asyncio
from typing import List
from models.metric import MetricDefinition
from core.evaluater import evaluate_all_conversations, EvaluationResult

@pytest.mark.asyncio
async def test_evaluate_all_conversations(correctness_metric: MetricDefinition):

    metrics: List[MetricDefinition] = [correctness_metric]

    test_csv_path = r"tests\data\conversation\Result-YepAI.csv"


    results = await evaluate_all_conversations(
        file_path=test_csv_path,
        metrics=metrics,
    )
    
    assert isinstance(results, list)
    assert all(isinstance(r, EvaluationResult) for r in results)

    if len(results) > 0:
        assert correctness_metric.name in results[0].scores
