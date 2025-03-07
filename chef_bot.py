#-- Program: chef_bot.py
#-- Author: Drew Ratliff
#-- Description: Bot for individual server torment
import os
import random
import discord
import datetime
from discord.ext import tasks
from discord.ext import commands
from dotenv import load_dotenv

#Target Funcion Variables
NUM_TARGETS = 3
REFRESH_RATE = 30 #Minutes

#-- Reply Function Variables
TEXT_CHANNEL = 707325634887548950
LOG_CHANNEL = 1073976750536659004
REQUIRED_RANGE = (0,1000)
CHANCE_RANGE = 2
#Total chance for reply = REQUIRED_RANGE[1]/CHANCE_RANGE

#If true, use secondary chef_members dict

#-- Debug 1: Always send text on_message
#-- Debug 2: Never send text on_message
#-- Debug 3: Testing birthday
debug = 0
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=intents, command_prefix="$")
#client = discord.Client(intents=intents)
#-- Responses for random chosen chef members in chef bois channel
responses = [
    """You're a putrescence mass, a walking vomit. You are a spineless little worm deserving nothing but the profoundest contempt. You are a jerk, a cad, a weasel. Your life is a monument to stupidity. You are a stench, a revulsion, a big suck on a sour lemon.""",
    """You are a bleating fool, a curdled staggering mutant dwarf smeared richly with the effluvia and offal accompanying your alleged birth into this world. An insensate, blinking calf, meaningful to nobody, abandoned by the puke-drooling, giggling beasts who sired you and then killed themselves in recognition of what they had done.""",
    """I will never get over the embarrassment of belonging to the same species as you. You are a monster, an ogre, a malformity. I barf at the very thought of you. You have all the appeal of a paper cut. Lepers avoid you. Because off your face the rabbit population actually decreased. You are vile, worthless, less than nothing. You are a weed, a fungus, the dregs of this earth. And did I mention you smell?""",
    """You snail-skulled little rabbit. Would that a hawk pick you up, drive its beak into your brain, and upon finding it rancid set you loose to fly briefly before spattering the ocean rocks with the frothy pink shame of your ignoble blood. May you choke on the queasy, convulsing nausea of your own trite, foolish beliefs.""",
    """You are a waste of flesh. You have no rhythm. You are ridiculous and obnoxious. You are the moral equivalent of a leech. You are a living emptiness, a meaningless void. You are sour and senile. You are a disease, you puerile one-handed slack-jawed drooling meatslapper.""",
    """On a good day you're a half-wit. You remind me of drool. You are deficient in all that lends character. You have the personality of wallpaper. You are dank and filthy. You are asinine and benighted. You are the source of all unpleasantness. You spread misery and sorrow wherever you go.""",
    """Your mom.\n\nP.S.: You are hypocritical, greedy, violent, malevolent, vengeful, cowardly, deadly, mendacious, meretricious, loathsome, despicable, belligerent, opportunistic, barratrous, contemptible, criminal, fascistic, bigoted, racist, sexist, avaricious, tasteless, idiotic, brain-damaged, imbecilic, insane, arrogant, deceitful, demented, lame, self-righteous, byzantine, conspiratorial, satanic, fraudulent, libelous, bilious, splenetic, spastic, ignorant, clueless, illegitimate, harmful, destructive, dumb, evasive, double-talking, devious, revisionist, narrow, manipulative, paternalistic, fundamentalist, dogmatic, idolatrous, unethical, cultic, diseased, suppressive, controlling, restrictive, malignant, deceptive, dim, crazy, weird, dystopic, stifling, uncaring, plantigrade, grim, unsympathetic, jargon-spouting, censorious, secretive, aggressive, mind-numbing, arassive, poisonous, flagrant, self-destructive, abusive, socially-retarded, puerile, clueless, and generally Not Good.""",
    """Fellows like you don't grow from trees, they swing from trees""",
    """How did you get here? Did someone leave your cage open?"""
    """You gem. You absolute masterpiece of God. You shining piece of gold. You are a piece of art, that the Angels drawn angels Earth,and forgot the paint brush. You have a freckle on your neck. Did you know that?
    It's rather cute.

    You are absolute,astoundingly gorgeous and that's the less interesting thing about you. You are Ethereal. A Heavenly Angel that God send down to Earth to put a smile in people in the worst days. You are so beautiful that you holy light cures depression itself. You are the pinnacle of perfection.

    You are the most gorgeous person that i have ever seen. You hair is one of the most gorgeous that i've ever seen. And you smell like strawberrys.

    You are always so happy and kind to people, it's like a big breath of fresh air when i walk into the street and see you! You haven't worn makeup all week? Damn, you're gorgeous! You carry yourself with much more maturity than most people on the Internet!

    I love talking to you. You dress in a stunning way, and you look really nice every day. You look just like your mother,she was a beautiful human being.

    Damn,that confidence looks really sexy on you! You think your beauty is on your considerably big breasts? Look up! I adore you. You are a real life Mona Lisa. You are the breathing,talking,living equivalent of a piece of art. I love seeing your smile,it brightens my day every time. I wish i could make you laught like that more often. You're beautiful all the time,but when you smile like that,i swear my world stops!

    I cannot believe how incredibly smart you are. Amazingly smart. Beautifully smart. Q.I. of 100 smart. Higher than Einstein Q.I smart. Einstein would be envious os you. You could decyphre the secrets of the universe if you could,and you will one day.

    You're that "nothing" when people ask me what i'm thinking about. You look great today. You're a smart cookie. I bet you make babies smile. You have impeccable manners. I like your style. You have the best laught.I aprecciate you. You are the most perfect you there is. Our system of inside jokes is so advanced that only you and i get it. And I like it. You light up the room. You should be proud of yourself. If cartoon bluebirds were real,they would be sitting on your shoulders singing with you right now. You're a great listener. I bet you sweat glitter. Jokes are funnier when you tell them. Your bellybutton is kind of adorable. You're irrestible when you blush. Babies and small animals probably love you. There's ordinary,and then there's you. You're someone's reason to smile. You're even better than a Unicorn,because
    you're real. How do you keep so funny and making everyone laugh? Has anyone ever told you that you have a great posture? The way you treasure your loved ones is incredible. You're really something special,you're a gift to those around you.

    Did i mentioned that i love you?"""
]

ninja_words = [
    "LIL CUB",
    "LIL PUP"
]

#-- List of valid chef members to target
chef_members = {
    "Oogi": 191369798788186112, 
    "Yolo": 694651316986707988, 
    "Ridge": 221986056193441792,
    "Charpop": 388455185468620820,
    "Wam": 356895872853999621,
    "Shane": 489853259130077185,
    "Toast": 318561633834106880,
    "Kid": 289601944346034176,
    "Spoonly": 226124570233536533,
    "Traxex": 284075942014484480,
    "Looke": 537008849987698688,
    "Darshauwn": 709565709696368671,
    "Skord": 160980489719644161,
    "Drew": 103233630515531776,
    "Gage": 126535729156194304,
    "Tal": 325803101007380483
    }

chef_birthdays = {
    "Charpop": datetime.date(1999,1,12),
    "Drew": datetime.date(1999,10,8)
}

channel_purge = {
    "Looke's Lagoon": 980651423270305803,
    "Yolo's Yacht": 984852499653623858,
    "Skord's Study": 987807674412449803,
    "Toast's Trail": 990449471399821362,
    "Oogi's Oasis": 991870918332788777,
    "Wam's Ward": 995100127855390830,
    "Trax's Turf": 1021517821601128621,
    "Kid's Kiosk": 1023309027800793249,
    "Ridge's Rehab": 1027234497231605802,
    "Shane's Society": 1056299604934676520,
    "Darshauwn's Dinghy": 1045761097480802385,
    "Charpop's Cinema": 1064752137478885396,
    "Drew's Dojo": 1070158474245328958,
    "Spoonly's Spoon": 1073762909970235442,
    "Gage's Gallery": 1131413528100745246,
    "Tal's Tower": 1142241135159427144
}

if debug == 1:
    chef_members = {"Drew": 103233630515531776}
    channel_purge = []
    NUM_TARGETS = 1
    CHANCE_RANGE = REQUIRED_RANGE[1]
    TEXT_CHANNEL = 500885037659455498
elif debug == 2:
    chef_members = {"Drew": 103233630515531776}
    NUM_TARGETS = 1
    CHANCE_RANGE = REQUIRED_RANGE[0]
elif debug == 3:
    chef_members = {"Drew": 103233630515531776}
    NUM_TARGETS = 1
    CHANCE_RANGE = REQUIRED_RANGE[0]
    chef_birthdays["Drew"] = datetime.datetime.now().date()
elif debug == 4:
    chef_members = {"Drew": 103233630515531776}
    NUM_TARGETS = 0
    channel_purge = {"DrewTest": 1074128958242697238}
    TEXT_CHANNEL = 500885037659455498

target_dict = {}

@client.command()
async def status(ctx):
    message = "Current Targets:\n"
    for x in target_dict.keys():
        message += x + "\n"
    await ctx.send(message)

#-- Populate target dict from chef dict
def set_list(adict: dict):
    time = datetime.datetime.now()
    adict.clear()
    print(f"\n[{time.hour}:{str(time.minute).zfill(2)}] Updating target list...\nNew Targets:")
    targ_list = random.sample(list(chef_members.keys()),NUM_TARGETS)
    if NUM_TARGETS > 0:
        for name in targ_list:
            adict[name] = chef_members[name]
            print(f"- {name}: {chef_members[name]}")
        
async def set_activity():
    activity = ""
    for i in range(len(target_dict)):
        activity += list(target_dict.keys())[i] + ", "
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity[0:len(activity)-2]))
    
    
#-- Disconnect each target from channel containing targets as a subset
async def disconnect_targets():
    for guild in client.guilds:
            if guild.name == GUILD:
                break
            
    await set_activity()
    
    for channel in guild.voice_channels:
        if set(target_dict.values()).issubset(channel.voice_states.keys()):
            for key in target_dict:
                await guild.get_member(target_dict[key]).move_to(None, reason=None)
            refreshList.restart()
            return

#-- Given a message, if it's the authors birthday say happy birthday
async def happy_birthday(message):
    for key in chef_members.keys():
        if chef_members[key] == message.author.id:
            if key in chef_birthdays:
                if datetime.datetime.now().date().day == chef_birthdays[key].day:
                    await message.reply("Happy Birthday!")
                    print(f"\nHappy Birthday! Sent to: {message.author.name}")
                    return
    
#-- Discord task for refreshing the list of target users
@tasks.loop(minutes = REFRESH_RATE)
async def refreshList():
    set_list(target_dict)
    await set_activity()

bois_channel: discord.channel
log_channel: discord.channel
guild: discord.guild
#-- On bot load, initialize
@client.event
async def on_ready():
    global bois_channel, log_channel, guild
    for guild in client.guilds:
        if guild.name == GUILD:
            break
            
    print(
        f'\n{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = f'\n- '.join([member.name for member in guild.members])
    print(f'Guild Members:\n- {members}')
    
    for channel in guild.channels:
        if channel.id == TEXT_CHANNEL:
            bois_channel = channel
        elif channel.id == LOG_CHANNEL:
            log_channel = channel
    
    refreshList.start()
    
#-- Checks for members in target_dict voice state update and kicks accordingly
@client.event
async def on_voice_state_update(member, before, after):
    global guild
    #-- No point in running if target doesn't trigger
    if member.id in target_dict.values() and after.channel is not None:
        if not target_dict:
            refreshList()

        await disconnect_targets()
       
    channelChance = random.randint(0, 125)
    if not before.channel and after.channel and (member.id in chef_members.values()):
        for key in chef_members.keys():
            if chef_members[key] == member.id:
                for name in channel_purge.keys():
                    if key in name:
                        channel = guild.get_channel(channel_purge[name])
                        if key in after.channel.name:
                            channelChance = random.randint(85, 125)
                        if channelChance == 96 and channel.name :
                            await channel.delete()
                            await bois_channel.send(f"<@{member.id}>... sorry bro, that shit got deleted. See ya later {channel.name}")
                            await log_channel.send(f"[{member.name}] joined {after.channel.name}. Rolled {channelChance}! Lucky number! {channel.name}, deleted.")
                        else:
                            await log_channel.send(f"[{member.name}] joined {after.channel.name}. Rolled {channelChance}. {channel.name} got away this time.")
                        break
                break
                
       
#-- Handle messages send in the-bois, respond randomly
@client.event
async def on_message(message):
    await client.process_commands(message)
    #await happy_birthday(message)
    for phrase in ninja_words:
        if phrase.upper() in message.content.upper():
            await message.reply("Faggot",delete_after=15)
            return
    #randNum = random.randint(REQUIRED_RANGE[0],REQUIRED_RANGE[1])
    #if message.channel.id == TEXT_CHANNEL and randNum < CHANCE_RANGE and not message.author.bot:
    #    response = random.choice(responses)
    #    responses.remove(response)
    #    await message.reply(response)
    #    print(f"\nGot Lucky! Replied to: {message.author.name} ({randNum}/{REQUIRED_RANGE[1]})")
    #elif message.channel.id == TEXT_CHANNEL and not message.author.bot:
    #    print(f"\nMissed chance for random interaction with: {message.author.name} ({randNum}/{REQUIRED_RANGE[1]})")
    
client.run(TOKEN)