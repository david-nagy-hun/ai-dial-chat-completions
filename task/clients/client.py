from aidial_client import Dial, AsyncDial

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        self.client = Dial(api_key=self._api_key, base_url=DIAL_ENDPOINT)
        self.async_client = AsyncDial(api_key=self._api_key, base_url=DIAL_ENDPOINT)

    def get_completion(self, messages: list[Message]) -> Message:
        response = self.client.chat.completions.create(
            deployment_name=self._deployment_name,
            stream=False,
            messages=[message.to_dict() for message in messages]
        )
        if response.choices and response.choices[0].message:
            content = response.choices[0].message.content
            print(content)
            return Message(Role.AI, content)
        raise Exception("No choices in response found")

    async def stream_completion(self, messages: list[Message]) -> Message:
        chunks = await self.async_client.chat.completions.create(
            deployment_name=self._deployment_name,
            stream=True,
            messages=[message.to_dict() for message in messages]
        )
        contents = []
        async for chunk in chunks:
            if chunk.choices:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    content = delta.content
                    print(content, end='')
                    contents.append(content)
        print()
        return Message(Role.AI, ''.join(contents))
