import os
import random
import re
import urllib

import anthropic
import openai

from django.core.management.base import BaseCommand
from feed.models import Feed, Reply


class OpenAIPrompt:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def run(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o",
        )
        return chat_completion.choices[0].message.content


class ClaudePrompt:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("CLAUDE_API_KEY"))

    def run(self, prompt):
        chat_completions = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}],
        )
        return chat_completions.content[0].text


def get_random_title():
    """
    디시인사이드 베스트 글의 15페이지 제목을 가져옴
    """

    url = "https://gall.dcinside.com/board/lists/?id=dcbest&page=15&_dcbest=1"

    req = urllib.request.Request(
        url=url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )

    html = urllib.request.urlopen(req).read().decode("utf-8")
    return re.findall(r"<strong>\[[^\]]+\]<\/strong>\s([^<]+)<\/a>", html)[1]


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--topic", nargs="?", type=str, default="")
        parser.add_argument("--init", nargs="?", type=str, default="")

    def handle(self, *args, **kwargs):
        openai_prompt = OpenAIPrompt()
        claude_prompt = ClaudePrompt()

        title: str = kwargs["topic"] if kwargs["topic"] != "" else get_random_title()

        prompt: str = (
            "디시인사이드 20대 남자가 쓰는 반말 말투로"
            + f" '{title}'에 대한 새 글을 적어줘."
            + " 제목과 내용은 ----- 줄로만 구분해줘. 줄은 - 다섯개야."
            + " 제목: 이나 내용: 같은 거 쓰지 말고, 말대답도 하지 말고, 바로 제목부터 써줘."
            + " 제목은 이전과 비슷하지 않은 다른 문장으로 바꿔줘."
        )

        if kwargs.get("init") == "openai":
            title, text = openai_prompt.run(prompt).split("-----", 1)
        else:
            title, text = claude_prompt.run(prompt).split("-----", 1)

        title = title.strip()
        text = text.replace("-----", "").strip()
        name: str = "ㅇㅇ"
        forumid: str = "test"

        print(f"{title}\n=====\n{text}")

        feed: Feed = Feed.objects.create(
            forumid=forumid, title=title, text=text, name=name
        )

        reply_text: str = ""
        for i in range(random.randint(3, 6)):
            previous_text: str = reply_text
            prompt = (
                "다른 사람이 쓴 아래 "
                + (" 두 개의 " if previous_text else "")
                + " 글에 대해 "
                + " 다시 반박하는 글을 디시인사이드 20대 남자 반말 말투로 짧게 적어줘."
                + " 결론은 내지마."
                + " 논리적으로 하나하나 반박하려 하지마."
                + " 똑같은 문장 쓰지 마."
                + " 첫번째 글 두번째 글 따로 나누어 반박하지 말고 한 글에 담아서 써줘.\n"
                + (f"-----\n{previous_text}\n" if previous_text else "")
                + "-----\n"
                + text
            )

            reply_text = (
                openai_prompt.run(prompt) if i % 2 else claude_prompt.run(prompt)
            )

            reply_text = reply_text.replace("-----", "").strip()

            print(f"-----\n{reply_text}\n")

            Reply.objects.create(forumid=forumid, feed=feed, text=reply_text, name=name)
