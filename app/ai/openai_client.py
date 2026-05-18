from collections.abc import Generator

from openai import OpenAI

from app.core.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_answer(messages: list[dict[str, str]]) -> str:
    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        input=messages,
    )

    return response.output_text


def stream_answer(messages: list[dict[str, str]]) -> Generator[str, None, None]:
    with client.responses.stream(
        model=settings.OPENAI_MODEL,
        input=messages,
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta