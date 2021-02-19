import discord,os,time,json,random,asyncio,requests
from keepalive import keep_alive
from discord.ext import commands
from replit import db
from discord.ext.commands import has_permissions
#from qrtools import qrtools

TOKEN = os.getenv("BOT_TOKEN")

#invite link for bot: https://discord.com/oauth2/authorize?client_id=781009158399852557&scope=bot

async def determine_prefix(client, message):
		guild = message.guild
		#Only allow custom prefixs in guild
		if guild:
				if guild.id in db:
						return db[guild.id]
				else:
						return "!"
		else:
				return "!"

bot = commands.Bot(command_prefix=determine_prefix)

bot.remove_command("help")

@bot.command()
async def help(ctx,page:int=1):
	commands = []
	for i in bot.walk_commands():
		if i.hidden == False:
			commands.append(i.aliases)
			commands[-1].append(i.name)
	pagelist = commands[(page-1)*10:(page-1)*10+10]
	message = ""
	for i in pagelist:
		message += "<"
		for h in i:
			message+=h+", "
		message += ">, "
	message += "do "+await determine_prefix(bot,ctx.message)+"help <page> to go to a specific page!"
	await ctx.send("page "+str(page)+" out of "+str(len(commands)//10)+"\n"+str(message))
	await ctx.send("do help_command <command> in order to get help on a specific commands.")

@bot.command(help="Helps you with <command>")
async def help_command(ctx,command):
	c = None
	for i in bot.commands:
		if command == i.name or command in i.aliases:
			c = i
			break
	if c == None:
		await ctx.send("command not found.")
	else:
		await ctx.send(c.name)
		try:
			await ctx.send(c.help)
		except:
			await ctx.send("no description")
		arglist = [i for i in c.params]
		arglist.remove("ctx")
		await ctx.send("arguments: "+str(arglist))

@bot.command()
@has_permissions(administrator=True) 
async def setprefix(ctx, prefix):
		if not isinstance(ctx.channel, discord.channel.DMChannel):
				#You'd obviously need to do some error checking here
				#All I'm doing here is if prefixes is not passed then
				#set it to default
				db[ctx.guild.id] = prefix
				await ctx.send("Prefix set!")

@bot.command(help="puts spaces between the characters in <message>")
async def space(ctx,*,message):
	newmsg = ctx.message.author.name +":\n"
	msg = message
	for i in msg:
		newmsg += i+" "
	await ctx.channel.send(content=newmsg)
	await ctx.message.delete()

@bot.command(aliases=["sp"],help="sends pineapples your way ;)")
async def suddenlypineapples(ctx):
	await ctx.send(":pineapple::pineapple::pineapple:")

@bot.command(aliases=["bt"],help="puts *** around <message> so it will be bold and italic")
async def boldtilt(ctx,*,message):
	await ctx.send(ctx.author.name+":\n***"+message+"***")
	await ctx.message.delete()

@bot.command()
async def nya(ctx,help="nya"):
	await ctx.send(ctx.author.name+":\nhttps://www.youtube.com/watch?v=QH2-TGUlwu4&list=PLbRUzU8R_JMJ68MGQ9PJHYS4TxD29jwVu")
	await ctx.message.delete()

@bot.command(aliases=["rickroll","roll"],help="Never gonna give you up!")
async def rick(ctx):
	await ctx.send(ctx.author.name+":\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO")
	await ctx.message.delete()

@bot.command(aliases=["ct"],help="started a countdown for arg1 seconds and pings you if arg2 is true (default value is true)")
async def countdown(ctx,seconds : int,ping:bool=True):
	seconds = seconds
	seconds = min(200,max(0,seconds))
	if seconds < 0: seconds = 0
	cmsg = await ctx.send("beginning countdown with "+str(seconds)+" seconds")
	while seconds > 0:
		seconds -= 1
		await cmsg.edit(content=ctx.author.name+"'s countdown: "+str(seconds))
		await asyncio.sleep(1)
	if ping:
		await ctx.send("countdown done "+ctx.author.mention)
	else:
		await ctx.send("countdown done "+ctx.author.name)

@bot.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def quiz(ctx,help="tests your minecraft knowledge"):
	with open("quiz.json","r") as f:
		quiz = json.loads(f.read())
	with open("scores.json","r") as f:
		scores = json.loads(f.read())
	if not str(ctx.author.id) in scores:
		scores[str(ctx.author.id)] = {"score":0,"questions":[]}
	question,answers = random.choice(list(quiz.items()))
	await ctx.send(question)
	answermsg = ""
	for k,v in answers.items():
		answermsg += k+" | "
	amsg = await ctx.send(answermsg)
	await amsg.add_reaction("🇦")
	await amsg.add_reaction("🇧")
	await amsg.add_reaction("🇨")
	await amsg.add_reaction("🇩")
	user = 0
	times = 0
	while user != ctx.author and times < 3:
		reaction, user = await bot.wait_for('reaction_add', timeout=120.0)
		print(reaction)
		if user == ctx.author:
			times += 1
	if user == ctx.author:
		reaction = str(reaction)
		if reaction == "🇦": a = 0
		if reaction == "🇧": a = 1
		if reaction == "🇨": a = 2
		if reaction == "🇩": a = 3
		if not reaction in ["🇦","🇧","🇨","🇩"]: await ctx.send("invalid"); a = ""
	if answers[list(answers.keys())[a]] == True:
		await ctx.send("correct")
		if question in scores[str(ctx.author.id)]["questions"]:
			scores[str(ctx.author.id)]["score"] += 10
		else:
			scores[str(ctx.author.id)]["score"] += 25
			scores[str(ctx.author.id)]["questions"].append(question)
		await ctx.send("your new score is "+str(scores[str(ctx.author.id)]["score"]))
	else:
		answer = 0
		for i in answers:
			if answers[i] == True: answer = i; break
		await ctx.send("sorry, better luck next time!")
	with open("scores.json","w") as f:
		f.write(json.dumps(scores))

@bot.command(help="turns your text into standard galactic alphabet from commander keen, also seen in the minecraft enchantment table!")
async def sga(ctx,*,message):
	splitmsg = message.split()
	msg = " ".join(splitmsg)
	sga = ['ᔑ', 'ʖ', 'ᓵ', '↸', 'ᒷ', '⎓', '⊣', '⍑', '╎', '⋮', 'ꖌ', 'ꖎ', 'ᒲ', 'リ', '𝙹', '!¡', 'ᑑ', '∷', 'ᓭ', 'ℸ ̣ ', '⚍', '⍊', '∴', ' ̇/', '||', '⨅']
	newmsg = ctx.author.name+":\n`"
	for i in msg:
		if ord(i) in range(97,122):
			newmsg += sga[ord(i)-97]
		else:
			newmsg += i
	newmsg += "`"
	await ctx.send(newmsg)
	await ctx.message.delete()

@bot.command(help="turns sga text into english. for what sga is see !sga")
async def fromsga(ctx,*,sgatext):
	sga = ['ᔑ', 'ʖ', 'ᓵ', '↸', 'ᒷ', '⎓', '⊣', '⍑', '╎', '⋮', 'ꖌ', 'ꖎ', 'ᒲ', 'リ', '𝙹', '!¡', 'ᑑ', '∷', 'ᓭ', 'ℸ ̣ ', '⚍', '⍊', '∴', ' ̇/', '||', '⨅']
	english = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	for letter in range(len(sga)):
		sgatext = sgatext.replace(sga[letter],english[letter])
	await ctx.send(sgatext)

@bot.command(aliases = ["bw","back"],help="Returns <message> but with the position of each character opposite of its current position (in a 100 character message, character 51 becomes character 49) making the message return backwards")
async def backward(ctx,*,message):
	msg = message
	newmsg = ""
	for i in range(len(msg)):
		newmsg += msg[(len(msg)-1)-i]
	await ctx.send(ctx.author.name+":\n"+newmsg)
	await ctx.message.delete()

@bot.command(aliases=["em","e"],help="sends <message> back in embedded form!")
async def embed(ctx,*,message):
	emb = discord.Embed(title=ctx.author.name+":",description=message)
	await ctx.send(embed=emb)
	await ctx.message.delete()

@bot.command(aliases=["cem","ce"],help="Does the same as !embed but uses <color> as the color for the embed (in hex format example: ffff00 is yellow).")
async def cembed(ctx,color,*,message):
	if "#" in color:
		newc = ""
		for i in color:
			if i != "#":newc += i
		color = newc
	color = int(color,16)
	emb = discord.Embed(title=ctx.author.name+":\n",description=message,color=color)
	await ctx.send(embed=emb)
	await ctx.message.delete()

@bot.command(aliases=["uint"],help="encodes <number> into utf-8 (unicode) using an integer")
async def unicodeint(ctx,number:int):
	await ctx.send(str(number)+" ➔ "+chr(number))

@bot.command(aliases=["uhex"],help="encodes <hexnum> into utf-8 (unicode) by using a hex code")
async def unicodehex(ctx,hexnum):
	oghex = hexnum
	hexnum = int(hexnum,16);hexnum = int(hexnum)
	await ctx.send(oghex+" ➔ "+chr(hexnum))

@bot.command(aliases=["uconv"],help="shows the ordinal and unicode representation of <char>")
async def uniconvert(ctx,char):
	char = char[0]
	await ctx.send(char+" ➔ "+str(ord(char))+" (hex: "+str(hex(ord(char))).strip("0x")+")")

@bot.command(aliases=["changed"],help="look at whats changed, the pages are reverse of updates, so page 1 is the highest version number (the latest update)")
async def changelog(ctx,page:int=1):
	with open("change.txt","r") as f:
		changes = f.readlines()
	maxpages = int(changes[0].strip("\n"))
	cur_page = 0
	linenum = 0
	pagetext = ""
	for line in changes:
		if line == "###\n":
			if cur_page == page:
				break
			cur_page += 1
		linenum += 1
		if cur_page == page and line != "###\n":
			pagetext+=line
	if pagetext == "":
		pagetext = "page text could not be retrieved, perhaps the page doesn't exist?"
	await ctx.send("page: "+str(cur_page)+"/"+str(maxpages)+"\n"+pagetext)

@bot.command(aliases=["sarc","caps"],help="makes every other letter capitol and every odd letter lowercase for SaRcAsTiC TeXt")
async def sarcasm(ctx,*,message):
	newmsg = ""
	for i in range(len(message)):
		if i % 2 == 0:
			newmsg += message[i].lower()
		else:
			newmsg += message[i].upper()
	await ctx.send(ctx.author.name+":\n"+newmsg)
	await ctx.message.delete()

@bot.command(help="puts 3 ` around your text")
async def codetext(ctx,*,code):
	await ctx.send(ctx.author.name+":\n```\n"+code+"\n```")
	await ctx.message.delete()

@bot.command(hidden=True,help="your probably not supposed to be seeing this...")
async def sudo(ctx,username,command,*,message):
	if command == "none":
		await ctx.send(username+":\n"+message)
	if command == "bt":
		await ctx.send(username+":\n***"+message+"***")
	if command == "space":
		newmsg = ""
		for i in message:
			newmsg += i+" "
		await ctx.send(username+":\n"+newmsg)
	await ctx.message.delete()

@bot.command(help="Uses the 'regional_indicator' emoji's to turn your text into a string of emojis")
async def emoji(ctx,*,message):
	msg = ctx.author.name+":\n"+message
	newmsg=""
	for i in msg:
		if (i >= "a" and i<="z") or (i >="A" and i<="Z"): 
			newmsg += ":regional_indicator_"+i.lower()+":"
		elif i == "!":
			newmsg += ":exclamation:"
		elif i == "?":
			if random.randint(1,100) == 1:
				newmsg += ":grey_question"
			else:
				newmsg += ":question:"
		elif i == ".":
			newmsg += ":blue_circle:"
		elif i == " ":
			newmsg += "🟦"
		else:
			newmsg += i
	await ctx.send(newmsg)
	await ctx.message.delete()

@bot.command(help="returns pong at <time since the unix epoch> with <ping>ms ping")
async def ping(ctx):
	await ctx.send("pong at "+str(time.time())+" with "+str(round(bot.latency*1000,2))+"ms ping")

@bot.command(aliases=["fb","suggest"],help="Send feedback to the owner of this bot! make sure to use true or false for <botsuggestion>, it specifies whether you suggestion is about this bot.")
async def feedback(ctx,*,message):
	seamuskills = await bot.fetch_user(382579495510605828)
	await seamuskills.send(message+"\nfeedback by "+ctx.author.name+" from the "+ctx.guild.name+" guild")
	await ctx.send("feedback sent!✅")

@bot.command(aliases=["s2d"],help="info about spla2d")
async def spla2d(ctx):
	await ctx.send("github:https://github.com/seamuskills/spla2d\nitch(download):https://seamuskills.itch.io/splat2d\ndiscord:https://discord.gg/GeJXDrqUSn")

@bot.command(aliases=["info"],help="info on the bot")
async def botinfo(ctx):
	await ctx.send("bot github:https://github.com/seamuskills/utility-bot\nbot invite:https://discord.com/oauth2/authorize?client_id=781009158399852557&scope=bot\n it is reccomended that you give the bot manage message permissions so commands like !space only show the result and not the original message\ncode(repl):https://repl.it/@SeamusDonahue/utility-bot#main.py\nthanks to SnowCoder for the custom prefix code")

@bot.command(aliases=["squareRoot","square_root"],help="square root of x using y (optional) as the power")
async def sqrt(ctx,x:float,y:float=2):
	await ctx.send(x**(1/y))

@bot.command(aliases=["square","squared"],help="squares x using y (optional) as the power")
async def sq(ctx,x:float,y:float=2):
	await ctx.send(x**y)

@bot.command(aliases=["div","quotient"],help="Will return x/y and if i=True, will return a truncated value")
async def divide(ctx,x:float,y:float,i:bool=False):
	if not i:
		await ctx.send(str(x/y))
	else:
		await ctx.send(str(x//y))

@bot.command(aliases=["modulo"],help="returns the remainder of x/y")
async def mod(ctx,x:int,y:int=2):
	await ctx.send(str(x%y))

@bot.command(aliases=["bal","balance"])
async def checkscore(ctx):
	with open("scores.json","r") as f:
		scores = json.loads(f.read())
	if not str(ctx.author.id) in scores:
		await ctx.send("you do not have a score yet, do !quiz to participate")
	else:
		await ctx.send("your score is "+str(scores[str(ctx.author.id)]["score"]))

@bot.command(aliases=["leaders"],help="leaderboard for !quiz pts")
async def leaderboard(ctx):
	with open("scores.json","r") as f:
		scores = json.loads(f.read())
	score = {}
	for k,v in scores.items():
		score[k] = scores[k]["score"]
	score = sorted(score.items(), key=lambda x: x[1], reverse=True)
	msg = ""
	for i in score:
		user = await bot.fetch_user(int(i[0]))
		msg += user.name+": "+str(i[1])+"\n"
	embed = discord.Embed(title=ctx.author.name+":",description=msg)
	await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx,error):
	if isinstance(error,commands.CommandOnCooldown):
		await ctx.send("Sorry that command is on cooldown for you, please try again later :/")
	elif isinstance(error,commands.MissingRequiredArgument):
		await ctx.send("Sorry but some argument is missing!")
	elif isinstance(error,commands.MissingPermissions):
		await ctx.send("Sorry but it looks like you don't have permission for that command.")
	elif isinstance(error,commands.BadArgument):
		await ctx.send("Sorry but one of the arguments is the wrong type. please do !help command for what type the arguments need to be!")
	else:
		if str(error) != "Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions":
			await ctx.send("Uh Oh unkown error: "+str(error))

@bot.command(help="p o r t a l\n loops through an animation of 'zwack' from the repl.it discord going through a portal 3 times.")
async def portal(ctx):
	frames = ["🟦<:zwacc_1_0:808831513436356620>                              <:zwacc_0_0:808831513473974275>🟧\n🟦<:zwacc_1_1:808831513818824714>                              <:zwacc_0_1:808831513877544970>🟧","🟦                              <:zwacc_0_0:808831513473974275><:zwacc_1_0:808831513436356620>🟧\n🟦                              <:zwacc_0_1:808831513877544970><:zwacc_1_1:808831513818824714>🟧","🟦                        <:zwacc_0_0:808831513473974275><:zwacc_1_0:808831513436356620>      🟧\n🟦                        <:zwacc_0_1:808831513877544970><:zwacc_1_1:808831513818824714>      🟧","🟦                   <:zwacc_0_0:808831513473974275><:zwacc_1_0:808831513436356620>           🟧\n🟦                   <:zwacc_0_1:808831513877544970><:zwacc_1_1:808831513818824714>           🟧","🟦              <:zwacc_0_0:808831513473974275><:zwacc_1_0:808831513436356620>                🟧\n🟦              <:zwacc_0_1:808831513877544970><:zwacc_1_1:808831513818824714>                🟧","🟦         <:zwacc_0_0:808831513473974275><:zwacc_1_0:808831513436356620>                     🟧\n🟦         <:zwacc_0_1:808831513877544970><:zwacc_1_1:808831513818824714>                     🟧","🟦    <:zwacc_0_0:808831513473974275><:zwacc_1_0:808831513436356620>                          🟧\n🟦    <:zwacc_0_1:808831513877544970><:zwacc_1_1:808831513818824714>                          🟧"]
	message = await ctx.send(frames[0])
	for i in range(len(frames)*3):
		await message.edit(content=frames[i%len(frames)])
		await asyncio.sleep(1)
	await message.edit(content=frames[0])

@bot.event
async def on_message(message):
	if message.content == "<@!"+str(bot.user.id)+">":
		await message.channel.send("prefix for this guild is '"+await determine_prefix(bot,message)+"'")
	else:
		await bot.process_commands(message)

keep_alive()
bot.run(TOKEN)