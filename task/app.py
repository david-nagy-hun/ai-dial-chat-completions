import asyncio

from task.clients.client import DialClient
from task.clients.custom_client import CustomDialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool) -> None:
    client = DialClient('gpt-4o')
    custom_client = CustomDialClient('gpt-4o')
    conversation = Conversation()

    print("Provide System prompt or press 'enter' to continue.")
    prompt = input().strip()

    if prompt:
        conversation.add_message(Message(Role.SYSTEM, prompt))
        print("System prompt successfully added to conversation.")
    else:
        conversation.add_message(Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT))
        print(f"No System prompt provided. Will be used default System prompt: '{DEFAULT_SYSTEM_PROMPT}'")

    print()

    print("Type your question or 'exit' to quit.")

    while True:
        user_message = input().strip()

        if user_message.lower() == 'exit':
            print("Exiting the chat. Goodbye!")
            break

        conversation.add_message(Message(Role.USER, user_message))

        if stream:
            conversation.add_message(await custom_client.stream_completion(conversation.get_messages()))
        else:
            conversation.add_message(custom_client.get_completion(conversation.get_messages()))

asyncio.run(
    start(True)
)
