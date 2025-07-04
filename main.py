import os
os.system("pip install -U git+https://github.com/dolfies/discord.py-self.git")
os.system("pip install colorama")
import json,discord,random,re,time,asyncio
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
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}═════════════════════════{Style.RESET_ALL}
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
l_check=0
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
    except Exception as e:
        print(f"[ERROR] {e}")

async def lb_wc(ctx):
    await ctx.send("owo inventory")
    await asyncio.sleep(3)

    try:
        messages = [msg async for msg in ctx.channel.history(limit=5)]
        for msg in messages:
            if msg.author.id == 408785106942164992:
                content = msg.content
                hbox = re.search(r'<:box:\d+>', content)
                hcrate = re.search(r'<:crate:\d+>', content)

                if hbox:
                    await ctx.send("owo lootbox all")
                    await asyncio.sleep(random.uniform(2.0, 3.0))
                    break 
                elif hcrate:
                    await ctx.send("owo weaponcrate all")
                    await asyncio.sleep(random.uniform(2.0, 3.0))
                    break
    except Exception as e:
        print(f"[Loot/Crate]: {e}")
   
async def check_warning(ctx):
    global running
    try:
        messages = [msg async for msg in ctx.channel.history(limit=10)]
        for msg in messages:
            msg_content = str(msg.content).lower()
      
            checkph = [
                "captcha",
                "Please complete thi​s wit​hin 1​0 m​inutes o​r i​t m​ay r​esult i​n a​ ba​n!",
                "P​lease comple​te you​r c​aptcha t​o ver​ify th​at y​ou ar​e huma​n!",
                "a​re y​ou a​ rea​l hu​man?"
            ]

            if any(phrase.lower() in msg_content for phrase in checkph):
                global running
                running = False
                print("[⚠️] Cảnh báo từ OwO Bot được phát hiện!")
                return True
        return False
    except Exception as e:
        print(f"[ERROR - Warning]: {e}")
        return False

@TienThanh.command(name="startowo", description="bắt đầu farm")
async def startowo(ctx):
    await ctx.message.delete()
    global running, l_check
    running = True
    l_check = time.time()
    lb_check = time.time()
    last_command = None
    farm_count = 0
    start_time = time.time()

    def n_cmd(farm_count, last_command):
        cmds = ["owo hunt", "owo battle"]
        if farm_count % 20 == 0: cmds.append("owo roll")
        if farm_count % 30 == 0: cmds.append("owo pray")
        if last_command in cmds and len(cmds) > 1:
            cmds.remove(last_command)
        return random.choice(cmds)

    while running:
        try:
            if await check_warning(ctx) or not running:
                print("[⚠️] Dừng vì bị cảnh báo")
                break

            now = time.time()
            if now - l_check > 480:
                await gem_check(ctx)
                l_check = now
           
            if now - lb_check > 580:
                await lb_wc(ctx)
                lb_check = now
                
            if time.time() - start_time >= 600:
                #print("[💤] Nghỉ 5 phút tránh spam")
                await asyncio.sleep(random.uniform(290, 320))
                start_time = time.time()

            if random.random() < 0.08:
                await ctx.send(random.choice(["owo zoo", "owo cry", "owo dance"]))
                await asyncio.sleep(random.uniform(2.0, 4.0))

            command = n_cmd(farm_count, last_command)
            last_command = command

            async with ctx.channel.typing():
                await asyncio.sleep(random.uniform(2.0, 4.0))

            await ctx.send(command)
            #print(f"[+] Sent: {command}")
            farm_count += 1

            await asyncio.sleep(random.uniform(12, 15))
        except Exception as e:
            print(f"[ERROR] {e}")

@TienThanh.command(name="stopowo", description="dừng farm") 
async def stopowo(ctx):
    await ctx.message.delete()
    global running  
    running=False

TienThanh.run(_token_)
