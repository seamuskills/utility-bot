#old version of bot for archival perposes... really its just in case I need it
import discord,os,time,json,random
from test import keep_alive
from discord.ext import commands
TOKEN = os.getenv("BOT_TOKEN")

#invite link for bot: https://discord.com/oauth2/authorize?client_id=781009158399852557&scope=bot

client = discord.Client()

@client.event
async def on_ready():
	print("ready")

@client.event
async def on_message(message):
	msg = message.content
	if message.author == client.user:
		return
	if message.content[0] == "!":
		if "!space" in message.content.lower():
			list_msg = msg.split()
			for i in range(len(list_msg)):
				if list_msg[i].lower() != "!space":
					list_msg[i] = list_msg[i]+" "
			newmsg = message.author.name +":\n"
			final_list = [word for word in list_msg if word.lower() != "!space"]
			msg = "".join(final_list)
			for i in msg:
				newmsg += i+" "
			await message.channel.send(content=newmsg)
			await message.delete()
		elif "!suddenlypineapples" in message.content.lower() or "!sp" in message.content.lower():
			await message.channel.send(":pineapple::pineapple::pineapple:")
		if "!boldtilt" in message.content.lower() or "!bt" in message.content.lower():
			newmsg = message.author.name +": \n "
			list_msg = msg.split()
			for i in range(len(list_msg)):
				if list_msg[i].lower() != "!boldtilt" and list_msg[i].lower() != "!bt":
					list_msg[i] = list_msg[i]+" "
			final_list = [word for word in list_msg if word.lower() != "!boldtilt"]
			final_list = [word for word in final_list if word.lower() != "!bt"]
			new_list = ["***"]
			for i in final_list:
				new_list.append(i)
			new_list.append("***")
			newmsg += "".join(new_list)
			await message.channel.send(content=newmsg)
			await message.delete()
		if "!nya" in message.content.lower():
			await message.channel.send(message.author.name+":\nhttps://www.youtube.com/watch?v=QH2-TGUlwu4&list=PLbRUzU8R_JMJ68MGQ9PJHYS4TxD29jwVu")
			await message.delete()
		if "!rick" in message.content.lower():
			await message.channel.send(message.author.name+":\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO")
			await message.delete()
		if "!countdown" in message.content.lower():
			msg = msg.split()
			if len(msg) > 2:
				if msg[2].lower() == "true":
					ping = True
				else:
					ping = False
			else:
				ping = True
			seconds = int(msg[1])
			seconds = min(200,max(0,seconds))
			if seconds < 0: seconds = 0
			cmsg = await message.channel.send("beginning countdown with "+str(seconds)+" seconds")
			while seconds > 0:
				seconds -= 1
				await cmsg.edit(content=message.author.name+"'s countdown: "+str(seconds))
				time.sleep(1)
			if ping:
				await message.channel.send("countdown done "+message.author.mention)
			else:
				await message.channel.send("countdown done "+message.author.name)
		if  "!report" in message.content.lower():
			reported = msg
			c = client.get_channel(782377204155285544)
			await c.send(reported+" was reported by"+message.author.mention)
		if "!quiz" in message.content.lower():
			with open("quiz.json","r") as f:
				quiz = json.loads(f.read())
			question,answers = random.choice(list(quiz.items()))
			await message.channel.send(question)
			answermsg = ""
			for k,v in answers.items():
				answermsg += k+" | "
			amsg = await message.channel.send(answermsg)
			await amsg.add_reaction("🇦")
			await amsg.add_reaction("🇧")
			await amsg.add_reaction("🇨")
			await amsg.add_reaction("🇩")
			user = 0
			times = 0
			while user != message.author and times < 3:
				reaction, user = await client.wait_for('reaction_add', timeout=120.0)
				times += 1
			if user == message.author:
				reaction = str(reaction)
				if reaction == "🇦": a = 0
				if reaction == "🇧": a = 1
				if reaction == "🇨": a = 2
				if reaction == "🇩": a = 3
				if not reaction in ["🇦","🇧","🇨","🇩"]: await message.channel.send("invalid"); a = ""
				print(reaction)
				if answers[list(answers.keys())[a]] == True:
					await message.channel.send("correct")
				else:
					answer = 0
					for i in answers:
						if answers[i] == True: answer = i; break
					await message.channel.send("sorry, the answer was "+str(answer))
		if "!sga" in message.content:
			splitmsg = message.content.split()
			splitmsg.remove("!sga")
			msg = " ".join(splitmsg)
			sga = ['ᔑ', 'ʖ', 'ᓵ', '↸', 'ᒷ', '⎓', '⊣', '⍑', '╎', '⋮', 'ꖌ', 'ꖎ', 'ᒲ', 'リ', '𝙹', '!¡', 'ᑑ', '∷', 'ᓭ', 'ℸ ̣ ', '⚍', '⍊', '∴', ' ̇/', '||', '⨅']
			newmsg = message.author.name+":\n`"
			for i in msg:
				if ord(i) in range(97,122):
					newmsg += sga[ord(i)-97]
				else:
					newmsg += i
			newmsg += "`"
			await message.channel.send(newmsg)
			await message.delete()
	if "§help" in message.content.lower():
		commands = ["help","space","boldtilt","nya","rick","countdown","quiz","suddenlypineapples","sga"]
		commandDescs = ["A command to describe other commands/list the commands.\narguments:<command with no !>\nno aliases","puts a space inbetween all the characters in your message.\narguments:[message]\nno aliases","a command to add `***` to your message so it is bold and italic.\narguments:[message]\nalias:bt","A command that gives the nyan cat video.\narguments:none\nno aliases","A command that gives a rick roll.\narguments:none\nno aliases","Starts a countdown timer and pings you when its done unless you put false.\narguments:[number], <ping (true/false)>\nno aliases","Gives a random question about minecraft for you to answer\narguments:none\nno aliases","Returns pineapple! shhhh this command is secret\narguments:none\nalias:sp","returns your message in standard galactic alphabet (only where applicable)\narguments:[message]\nno aliases"]
		helpofcommand = False; commandtohelp = ""
		msglist = message.content.split()
		for word in msglist:
			print(word)
			if word in commands:
				helpofcommand = True;commandtohelp = word; break
		if not helpofcommand:
			await message.channel.send("<optional> [required] commands: §help <command with no !>, !space [message], !boldtilt [message], !nya, !rick, !countdown [number] <ping (true/false)>, !quiz, !sga [message]")
		else:
			await message.channel.send(commandDescs[commands.index(commandtohelp)])

keep_alive()
client.run(TOKEN)