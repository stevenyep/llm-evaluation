import pytest

from models.metric import MetricDefinition


@pytest.fixture(scope="function")
def correctness_metric() -> MetricDefinition:
    correctness_metric: MetricDefinition = MetricDefinition.from_json(r"C:\Users\steqi\Documents\llm-evaluation\tests\data\metrics\correctness.json")
    print(correctness_metric)
    return correctness_metric