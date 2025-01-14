import pytest
from utils import workflow_manager
from models import WorkflowResults

@pytest.mark.asyncio
async def test_run_full_workflow():
    mock_query = "Test query"
    results: WorkflowResults = await workflow_manager.run_full_workflow(mock_query)
    assert isinstance(results, WorkflowResults)
    # Depending on how your LLM is mocked or if it actually calls an API,
    # you might just check that no exceptions occur and that the result is an instance of WorkflowResults.
