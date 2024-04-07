import random
import re
import httpx


from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot import logger

gpt4_1106_preview = on_command("",rule=to_me(),priority=90)

async def register():
    session = httpx.Client()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }
    email = str(random.randint(1000000000, 9999999999)) + "@qq.com"
    data = {
        "name": "haozai",
        "username": "haozai",
        "email": email,
        "password": "147258369",
        "confirm_password": "147258369"
    }
    register_res = session.post("https://gptchina.io/api/auth/register", data=data)
    if register_res.status_code != 200:
        return register()
    session.headers.update({'Authorization': register_res.headers['Authorization']})
    return session


async def get_resp(message: str):
    session = await register()
    data = {
        "text": message,
        "sender": "User",
        "isCreatedByUser": True,
        "parentMessageId": "00000000-0000-0000-0000-000000000000",
        "responseMessageId": "00000000-0000-0000-0000-000000000000",
        "conversationId": None,
        "messageId": "fe846644-3fb0-460d-89ea-85a5dd8ac36e",
        "error": False,
        "generation": "",
        "overrideParentMessageId": None,
        "model": "gpt-4-1106-preview",
        "endpoint": "openAI",
        "key": None,
        "isContinued": None
    }
    with session.stream("POST",url="https://gptchina.io/api/ask/openAI", json=data) as r:
        error = False
        for chunk in r.iter_bytes():
            try:
                chunk = chunk.decode("utf-8")
                temp = chunk
            except:
                chunk = temp
                error = True
            if '"final":true' in chunk:
                resp = re.search('"GPT-4","text":"(.*?)",', chunk, re.M | re.I)
                return resp.group(1).replace("\\n", "\n").replace('\\"', '\"')
            elif error:
                resp = re.search('"text":"(.*?)"',chunk, re.M | re.I)
                return resp.group(1).replace("\\n", "\n").replace('\\"', '\"')
        # 如果要即时显示就用这种方式
        # if "text" in message.keys():
        #     print("\r"+message["text"],end="")
        #     sys.stdout.flush()

@gpt4_1106_preview.handle()
async def chat_at_once(bot: Bot,event: MessageEvent, args: Message = CommandArg()):
    await bot.send(event=event,message=await get_resp(args.extract_plain_text()),group_id=str(event.group_id),at_sender=True,reply_message=True)

