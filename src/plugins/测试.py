from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Message,MessageSegment,Bot,Event
from nonebot.params import CommandArg, Arg

sayback = on_command("",rule=to_me(),priority=80)

@sayback.handle()
async def handle_function(bot: Bot, event: Event,message: Message = CommandArg()):
    pass