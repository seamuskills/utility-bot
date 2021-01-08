import discord,os,time,json,random
from keepalive import keep_alive
from discord.ext import commands
TOKEN = os.getenv("BOT_TOKEN")

#invite link for bot: https://discord.com/oauth2/authorize?client_id=781009158399852557&scope=bot

bot = commands.Bot(command_prefix='!')

@bot.command(description="puts spaces between the characters in <message>")
async def space(ctx,*,message):
	newmsg = ctx.message.author.name +":\n"
	msg = message
	for i in msg:
		newmsg += i+" "
	await ctx.channel.send(content=newmsg)
	await ctx.message.delete()

@bot.command(aliases=["sp"],description="sends pineapples your way ;)")
async def suddenlypineapples(ctx):
	await ctx.send(":pineapple::pineapple::pineapple:")

@bot.command(aliases=["bt"],description="puts *** around <message> so it will be bold and italic")
async def boldtilt(ctx,*,message):
	await ctx.send(ctx.author.name+":\n***"+message+"***")
	await ctx.message.delete()

@bot.command()
async def nya(ctx,description="nya"):
	await ctx.send(ctx.author.name+":\nhttps://www.youtube.com/watch?v=QH2-TGUlwu4&list=PLbRUzU8R_JMJ68MGQ9PJHYS4TxD29jwVu")
	await ctx.message.delete()

@bot.command(aliases=["rickroll","roll"],description="Never gonna give you up!")
async def rick(ctx):
	await ctx.send(ctx.author.name+":\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO")
	await ctx.message.delete()

@bot.command(aliases=["ct"],description="started a countdown for arg1 seconds and pings you if arg2 is true (default value is true)")
async def countdown(ctx,seconds : int,ping:bool=True):
	seconds = seconds
	seconds = min(200,max(0,seconds))
	if seconds < 0: seconds = 0
	cmsg = await ctx.send("beginning countdown with "+str(seconds)+" seconds")
	while seconds > 0:
		seconds -= 1
		await cmsg.edit(content=ctx.author.name+"'s countdown: "+str(seconds))
		time.sleep(1)
	if ping:
		await ctx.send("countdown done "+ctx.author.mention)
	else:
		await ctx.send("countdown done "+ctx.author.name)

@bot.command()
async def quiz(ctx,description="tests your minecraft knowledge"):
	with open("quiz.json","r") as f:
		quiz = json.loads(f.read())
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
	else:
		answer = 0
		for i in answers:
			if answers[i] == True: answer = i; break
		await ctx.send("sorry, the answer was ||"+str(answer)+"||")

@bot.command(description="turns your text into standard galactic alphabet from commander keen, also seen in the minecraft enchantment table!")
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

@bot.command(aliases = ["bw","back"],description="Returns <message> but with the position of each character opposite of its current position (in a 100 character message, character 51 because character 49) making the message return backwards")
async def backward(ctx,*,message):
	msg = message
	newmsg = ""
	for i in range(len(msg)):
		newmsg += msg[(len(msg)-1)-i]
	await ctx.send(ctx.author.name+":\n"+newmsg)
	await ctx.message.delete()

@bot.command(aliases=["em","e"],description="sends <message> back in embedded form!")
async def embed(ctx,*,message):
	emb = discord.Embed(title=ctx.author.name+":",description=message)
	await ctx.send(embed=emb)
	await ctx.message.delete()

@bot.command(aliases=["cem","ce"],description="Does the same as !embed but uses <color> as the color for the embed (in hex format example: ffff00 is yellow).")
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

@bot.command(aliases=["uint"],description="encodes <number> into utf-8 (unicode) using an integer")
async def unicodeint(ctx,number:int):
	await ctx.send(str(number)+" ➔ "+chr(number))

@bot.command(aliases=["uhex"],description="encodes <hexnum> into utf-8 (unicode) by using a hex code")
async def unicodehex(ctx,hexnum):
	oghex = hexnum
	hexnum = int(hexnum,16);hexnum = int(hexnum)
	await ctx.send(oghex+" ➔ "+chr(hexnum))

@bot.command(aliases=["uconv"],description="shows the ordinal unicode representation of <char>")
async def uniconvert(ctx,char):
	char = char[0]
	await ctx.send(char+" ➔ "+str(ord(char))+" (hex: "+str(hex(ord(char))).strip("0x")+")")

@bot.command(aliases=["changed"])
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

@bot.command(aliases=["sarc","caps"])
async def sarcasm(ctx,*,message):
	newmsg = ""
	for i in range(len(message)):
		if i % 2 == 0:
			newmsg += message[i].lower()
		else:
			newmsg += message[i].upper()
	await ctx.send(newmsg)
	await ctx.message.delete()

@bot.command()
async def codetext(ctx,*,code):
	await ctx.send(ctx.author.name+":\n```\n"+code+"\n```")
	await ctx.message.delete()

@bot.command(hidden=True)
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

@bot.command()
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
		else:
			newmsg += i
	await ctx.send(newmsg)
	await ctx.message.delete()

@bot.command()
async def ping(ctx):
	await ctx.send("pong at "+str(time.time()))

keep_alive()
bot.run(TOKEN)
