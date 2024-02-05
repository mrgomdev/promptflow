import asyncio
import json
import sys
from unittest.mock import patch

import pytest

from promptflow._core._errors import UnexpectedError
from promptflow._core.operation_context import OperationContext
from promptflow._utils.exception_utils import JsonSerializedPromptflowException
from promptflow.exceptions import ErrorTarget
from promptflow.executor._service._errors import ExecutionTimeoutError
from promptflow.executor._service.utils.process_utils import invoke_function_in_process

MOCK_CONTEXT_DICT = {"context_test_key": "test_value"}


async def target_function(request: int):
    operation_context = OperationContext.get_instance()
    assert operation_context.context_test_key == "test_value"
    if request == 0:
        # raise exception to simulate error during executing the target function
        raise Exception("Test exception")
    elif request < 0:
        # exit current process with exit code -1 to simulate unexpected error
        sys.exit(1)
    # sleep for the request seconds to simulate the timeout case
    await asyncio.sleep(request)
    return request


@pytest.mark.unittest
class TestProcessUtils:
    @pytest.mark.asyncio
    async def test_invoke_function_in_process_completed(self):
        with patch("promptflow.executor._service.utils.process_utils.service_logger") as mock_logger:
            result = await invoke_function_in_process(1, MOCK_CONTEXT_DICT, target_function)
            assert result == 1
            assert mock_logger.info.call_count == 2
            mock_logger.error.assert_not_called()

    @pytest.mark.asyncio
    async def test_invoke_function_in_process_timeout(self):
        with patch("promptflow.executor._service.utils.process_utils.service_logger") as mock_logger:
            with pytest.raises(ExecutionTimeoutError) as exc_info:
                await invoke_function_in_process(10, MOCK_CONTEXT_DICT, target_function, wait_timeout=2)
            assert exc_info.value.message == "Execution timeout for exceeding 2 seconds"
            assert exc_info.value.target == ErrorTarget.EXECUTOR
            mock_logger.info.assert_called_once()
            mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_invoke_function_in_process_exception(self):
        with patch("promptflow.executor._service.utils.process_utils.service_logger") as mock_logger:
            with pytest.raises(JsonSerializedPromptflowException) as exc_info:
                await invoke_function_in_process(0, MOCK_CONTEXT_DICT, target_function)
            assert json.loads(exc_info.value.message)["message"] == "Test exception"
            mock_logger.info.assert_called_once()
            mock_logger.error.assert_not_called()

    @pytest.mark.asyncio
    async def test_invoke_function_in_process_unexpected_error(self):
        with patch("promptflow.executor._service.utils.process_utils.service_logger") as mock_logger:
            with pytest.raises(UnexpectedError) as exc_info:
                await invoke_function_in_process(-1, MOCK_CONTEXT_DICT, target_function)
            assert exc_info.value.message == "Unexpected error occurred while executing the request"
            assert exc_info.value.target == ErrorTarget.EXECUTOR
            mock_logger.info.assert_called_once()
            mock_logger.error.assert_not_called()
