import json

from pydantic import BaseModel
from typing import List
from deepeval.test_case import LLMTestCaseParams



class MetricDefinition(BaseModel):
    name: str
    criteria: str
    evaluation_steps: List[str]
    evaluation_params: List[LLMTestCaseParams] = [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT]

    @staticmethod
    def from_json(json_path: str):
        metric_json = json.load(open(json_path))
        return MetricDefinition(**metric_json)

