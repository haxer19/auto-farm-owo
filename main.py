import os
os.system("pip install -U git+https://github.com/dolfies/discord.py-self.git")
os.system("pip install colorama")
import json, discord,random,re,time,asyncio
from colorama import Fore, Style, init
from discord.ext import commands

init(autoreset=True)

with open("config.json", "r") as config_file:
    config = json.load(config_file)

_token_=config["TOKEN"]
_prefix_=config["PREFIX"]
TienThanh = commands.Bot(command_prefix=_prefix_, case_insensitive=True, self_bot=True)
TienThanh.remove_command("help")

async def getUser(bot, user_id: int, guild=None):
    user = await bot.fetch_user(user_id)
    member = None

    if guild:
        member = guild.get_member(user_id)
    else:
        member = discord.utils.find(lambda m: m.id == user_id, bot.get_all_members())

    info = {
        "id": user.id,
        "username": user.name,
        "created_at": user.created_at.strftime('%d/%m/%Y | %H:%M:%S'),
        "banner_color": str(user.accent_color) if user.accent_color else " ",
        "avatar_url": user.display_avatar.url,
        "display_name": user.global_name,
    }

    if member:
        info.update({
            "in_guild": True,
            "nickname": member.nick if member.nick else " ",
            "joined_at": member.joined_at.strftime('%d/%m/%Y | %H:%M:%S') if member.joined_at else " ",
            "role_count": len(member.roles) - 1,
            "guild_avatar": member.avatar.url if member.avatar else " ",
        })
    else:
        info.update({
            "in_guild": False,
            "display_name": user.name,
        })

    return info

@TienThanh.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    Tiến_Thành=await getUser(TienThanh,TienThanh.user.id)
    menu = f"""
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}╔═══════════════════════╗
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}║       {Fore.LIGHTGREEN_EX}MENU USER{Fore.LIGHTCYAN_EX}       ║
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}╚═══════════════════════╝
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Tên hiển thị [ {Style.RESET_ALL}{Tiến_Thành['display_name']}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Username [ {Style.RESET_ALL}@{Tiến_Thành['username']}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> ID [ {Style.RESET_ALL}{Tiến_Thành['id']}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Ngày tạo [ {Style.RESET_ALL}{Tiến_Thành['created_at']}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Banner Color [ {Style.RESET_ALL}{Tiến_Thành['banner_color']}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Prefix [ {Style.RESET_ALL}{_prefix_}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Có [ {Style.RESET_ALL}{len(TienThanh.guilds)}{Fore.LIGHTRED_EX}{Style.BRIGHT} ] máy chủ
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}═════════════════════════
"""
    print(menu)

@TienThanh.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        await ctx.send(f"sử dụng {_prefix_}help xem lệnh đang có.")
    else:
        raise error

@TienThanh.command(name="help", description="Hiển thị danh sách lệnh")
async def help(ctx):
    await ctx.message.delete()
    cmds = []
    for cmd in TienThanh.commands:
        cmds.append(f"{_prefix_}{cmd.name} - {cmd.description}")

    await ctx.send("COMMAND LIST:\n" + "\n".join(cmds))

running=False
lasst_check=0
gem_used=0

async def parse_gems(inventory_message):
    rarity_order = ['f', 'l', 'm', 'e', 'r', 'u', 'c']
    gems_by_tier = {
        '1': [],
        '2': [],
        '3': [],
        '4': []
    }
    lines = inventory_message.split('\n')
    for line in lines:
        for tier in ['1', '2', '3', '4']:
            for rarity in rarity_order:
                pattern = fr'`(\d+)`<:({rarity}gem{tier}):\d+>'
                match = re.search(pattern, line)
                if match:
                    gem_number = match.group(1)  
                    gems_by_tier[tier].append((rarity, gem_number))
    for tier in gems_by_tier:
        gems_by_tier[tier].sort(key=lambda x: rarity_order.index(x[0]))
    selected_gems = []
    for tier in ['1', '2', '3', '4']:
        if gems_by_tier[tier]:
            selected_gems.append(gems_by_tier[tier][0][1])

    return selected_gems

async def gem_check(ctx):
    global gem_used
    await ctx.send("owo inventory")
    await asyncio.sleep(3)  
    try:
        latest_messages = [msg async for msg in ctx.channel.history(limit=2)]
        for message in latest_messages:
            if message.author.id == 408785106942164992:  
                if "inventory" in message.content.lower():
                    gem_numbers = await parse_gems(message.content)
                    if gem_numbers: 
                        use_command = "owo use " + " ".join(gem_numbers)
                        gem_used+=len(gem_numbers)
                        await ctx.send(use_command)
                        await asyncio.sleep(3)
                    break
    except:
        pass

def emoji(text):
    return re.sub(r'<a?:\w+:\d+>', '', text)

async def check_warning(ctx):
    global running
    try:
        messages = [msg async for msg in ctx.channel.history(limit=10)]
        for msg in messages:
            if msg.author.id != 408785106942164992:
                continue 

            if msg.stickers:
                continue 

            if TienThanh.user.mention not in msg.content:
                continue  
                
            cemoji = emoji(msg.content).lower()

            warning_phrases = [
                "are you a real human",
                "please complete this within",
                "please complete your captcha",
                "verify that you are human",
                "you have been banned for",
                "macros or botting"
            ]

            if any(phrase in cemoji for phrase in warning_phrases):
                running = False
                return True

        return False
    except Exception:
        return False

@TienThanh.command(name="startowo", description="bắt đầu farm")
async def startowo(ctx):
    await ctx.message.delete()
    global running,lasst_check
    running=True
    lasst_check =time.time()
    last_command=None
    farm_count=0
    start_time=time.time()
    def n_cmd(farm_count):
        base_cmds = ["owo hunt","owo battle"]
        #if farm_count % 5 == 0:
        #    base_cmds.append("owo sell all")
        if farm_count % 20 == 0:
            base_cmds.append("owo roll")
        if farm_count % 30 == 0:
            base_cmds.append("owo pray")
        #if random.random() < 0.1:
            #base_cmds += ["owo kill <@408785106942164992>", "owo punch <@408785106942164992>", "owo hug <@408785106942164992>"]

        if last_command in base_cmds and len(base_cmds)>1:
            base_cmds.remove(last_command)

        return random.choice(base_cmds)

    async def auto_rest(start_time):
        if time.time() - start_time >= 600: 
            await asyncio.sleep(random.uniform(290, 320))
            return time.time()
        return start_time

    async def xamm(ctx):
        if random.random() < 0.08:
            sus_cmd = random.choice(["owo zoo", "owo cry", "owo dance"])
            #await ctx.send(sus_cmd)
            await asyncio.sleep(random.uniform(2.0, 4.0))

    while running:
        try:
            now = time.time()
            if now - lasst_check > 480:
                if await check_warning(ctx): break
                await gem_check(ctx)
                lasst_check = now

            start_time=await auto_rest(start_time)
            await xamm(ctx)
            command=n_cmd(farm_count)
            #while command==last_command: command=n_cmd(farm_count)
            last_command=command
            async with ctx.channel.typing(): await asyncio.sleep(random.uniform(2.0, 4.0))
            await ctx.send(command)
            if await check_warning(ctx): break
            farm_count+=1
            await asyncio.sleep(max(10,random.betavariate(2.0,5.0)*20))
        except:
            pass

@TienThanh.command(name="stopowo", description="dừng farm") 
async def stopowo(ctx):
    await ctx.message.delete()
    global running  
    running=False

TienThanh.run(_token_)
