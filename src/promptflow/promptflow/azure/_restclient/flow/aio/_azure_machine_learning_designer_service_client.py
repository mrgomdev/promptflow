# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator (autorest: 3.8.0, generator: @autorest/python@5.12.2)
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from copy import deepcopy
from typing import Any, Awaitable, Optional

from azure.core import AsyncPipelineClient
from azure.core.rest import AsyncHttpResponse, HttpRequest
from msrest import Deserializer, Serializer

from .. import models
from ._configuration import AzureMachineLearningDesignerServiceClientConfiguration
from .operations import BulkRunsOperations, ConnectionOperations, ConnectionsOperations, FlowRuntimesOperations, FlowRuntimesWorkspaceIndependentOperations, FlowSessionsOperations, FlowsOperations, FlowsProviderOperations, ToolsOperations, TraceSessionsOperations

class AzureMachineLearningDesignerServiceClient:
    """AzureMachineLearningDesignerServiceClient.

    :ivar bulk_runs: BulkRunsOperations operations
    :vartype bulk_runs: flow.aio.operations.BulkRunsOperations
    :ivar connection: ConnectionOperations operations
    :vartype connection: flow.aio.operations.ConnectionOperations
    :ivar connections: ConnectionsOperations operations
    :vartype connections: flow.aio.operations.ConnectionsOperations
    :ivar flow_runtimes: FlowRuntimesOperations operations
    :vartype flow_runtimes: flow.aio.operations.FlowRuntimesOperations
    :ivar flow_runtimes_workspace_independent: FlowRuntimesWorkspaceIndependentOperations
     operations
    :vartype flow_runtimes_workspace_independent:
     flow.aio.operations.FlowRuntimesWorkspaceIndependentOperations
    :ivar flows: FlowsOperations operations
    :vartype flows: flow.aio.operations.FlowsOperations
    :ivar flow_sessions: FlowSessionsOperations operations
    :vartype flow_sessions: flow.aio.operations.FlowSessionsOperations
    :ivar flows_provider: FlowsProviderOperations operations
    :vartype flows_provider: flow.aio.operations.FlowsProviderOperations
    :ivar tools: ToolsOperations operations
    :vartype tools: flow.aio.operations.ToolsOperations
    :ivar trace_sessions: TraceSessionsOperations operations
    :vartype trace_sessions: flow.aio.operations.TraceSessionsOperations
    :param base_url: Service URL. Default value is ''.
    :type base_url: str
    :param api_version: Api Version. The default value is "1.0.0".
    :type api_version: str
    """

    def __init__(
        self,
        base_url: str = "",
        api_version: Optional[str] = "1.0.0",
        **kwargs: Any
    ) -> None:
        self._config = AzureMachineLearningDesignerServiceClientConfiguration(api_version=api_version, **kwargs)
        self._client = AsyncPipelineClient(base_url=base_url, config=self._config, **kwargs)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)
        self._serialize.client_side_validation = False
        self.bulk_runs = BulkRunsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.connection = ConnectionOperations(self._client, self._config, self._serialize, self._deserialize)
        self.connections = ConnectionsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.flow_runtimes = FlowRuntimesOperations(self._client, self._config, self._serialize, self._deserialize)
        self.flow_runtimes_workspace_independent = FlowRuntimesWorkspaceIndependentOperations(self._client, self._config, self._serialize, self._deserialize)
        self.flows = FlowsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.flow_sessions = FlowSessionsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.flows_provider = FlowsProviderOperations(self._client, self._config, self._serialize, self._deserialize)
        self.tools = ToolsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.trace_sessions = TraceSessionsOperations(self._client, self._config, self._serialize, self._deserialize)


    def _send_request(
        self,
        request: HttpRequest,
        **kwargs: Any
    ) -> Awaitable[AsyncHttpResponse]:
        """Runs the network request through the client's chained policies.

        >>> from azure.core.rest import HttpRequest
        >>> request = HttpRequest("GET", "https://www.example.org/")
        <HttpRequest [GET], url: 'https://www.example.org/'>
        >>> response = await client._send_request(request)
        <AsyncHttpResponse: 200 OK>

        For more information on this code flow, see https://aka.ms/azsdk/python/protocol/quickstart

        :param request: The network request you want to make. Required.
        :type request: ~azure.core.rest.HttpRequest
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The response of your network call. Does not do error handling on your response.
        :rtype: ~azure.core.rest.AsyncHttpResponse
        """

        request_copy = deepcopy(request)
        request_copy.url = self._client.format_url(request_copy.url)
        return self._client.send_request(request_copy, **kwargs)

    async def close(self) -> None:
        await self._client.close()

    async def __aenter__(self) -> "AzureMachineLearningDesignerServiceClient":
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *exc_details) -> None:
        await self._client.__aexit__(*exc_details)
