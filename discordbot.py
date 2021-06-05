import discord
import json
import asyncio 
from discord.ext import commands
from discord.ext.commands.core import command
from random import randint

bot = commands.Bot(command_prefix = '.')

queue = []

@bot.command()
async def b(self, member: discord.Member = None):
    if member == None:
        with open('economy.json', 'r') as f:
            money = json.load(f)
        if not str(self.author.id) in money:
            money[str(self.author.id)] = {}
            money[str(self.author.id)]['money'] = 0
        emb = discord.Embed(description = f"У вас {money[str(self.author.id)]['money']} денежных единиц.")
        emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url)
        await self.send(embed = emb)
    
    else:
        with open('economy.json', 'r') as f:
            money = json.load(f)
        if not str(member.id) in money:
            money[str(member.id)] = {}
            money[str(member.id)]['money'] = 0
        emb = discord.Embed(description = f"У {member} {money[str(member.id)]['money']} денежных единиц.")
        emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url)
        await self.send(embed = emb)

@bot.command()
async def timely(self):
    with open('economy.json', 'r') as f:
        money = json.load(f)

    if not str(self.author.id) in money:
        money[str(self.author.id)] = {}
        money[str(self.author.id)]['money'] = 0

    if not str(self.author.id) in queue:
        emb = discord.Embed(description = "Вы получил 100 денежных единиц, возвращайтесь через 4 часа.")
        emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url)
        await self.send(embed = emb)
        money[str(self.author.id)]['money'] += 100
        with open('economy.json', 'w') as f:
            json.dump(money, f)
        queue.append(str(self.author.id))
        await asyncio.sleep(4 * 60)
        queue.remove(str(self.author.id))

    if str(self.author.id) in queue:
        emb = discord.Embed(description = "Вы уже получали денежные единицы.")
        emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url) 
        await self.send(embed = emb)

@bot.command()
async def ahelp(self):
    emb = discord.Embed(title = "Помощь по командам", color = 0x00ff00)
    emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url)
    emb.add_field(name = "Калькулятор:", value = ".calc (1 число) (знак) (2 число)", inline = False)
    emb.add_field(name = "Эхо:", value = ".echo (фраза)", inline = False)
    emb.add_field(name = "Генератор случайных чисел:", value = ".calc (от) (до)", inline = False)
    emb.add_field(name = "Информация о пользователе:", value = ".user (имя#тег)", inline = False)
    await self.send(embed = emb)

@bot.command()
async def calc(self, num1: float, sign, num2: float):
    emb = discord.Embed(title = "Калькулятор", color = 0x00ff00)
    emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url)
    try:
        if sign == '+':
            emb.add_field(name = "Результат:", value = num1 + num2, inline = False)
            await self.send(embed = emb)
        elif sign == '-':
            emb.add_field(name = "Результат:", value = num1 - num2, inline = False)
            await self.send(embed = emb)
        elif sign == '*':
            emb.add_field(name = "Результат:", value = num1 * num2, inline = False)
            await self.send(embed = emb)
        elif sign == '/':
            emb.add_field(name = "Результат:", value = num1 / num2, inline = False)
            await self.send(embed = emb)
        elif sign == "=":
            if num1 == num2:
                emb.add_field(name = "Результат:", value = "Верно.", inline = False)
                await self.send(embed = emb)
            else:
                emb.add_field(name = "Результат:", value = "Неверно.", inline = False)
                await self.send(embed = emb)
        elif sign == "<=":
            if num1 <= num2:
                emb.add_field(name = "Результат:", value = "Верно.", inline = False)
                await self.send(embed = emb)
            else:
                emb.add_field(name = "Результат:", value = "Неверно.", inline = False)
                await self.send(embed = emb)
        elif sign == ">=":
            if num1 >= num2:
                emb.add_field(name = "Результат:", value = "Верно.", inline = False)
                await self.send(embed = emb)
            else:
                emb.add_field(name = "Результат:", value = "Неверно.", inline = False)
                await self.send(embed = emb)
        else:
            await self.send("Команда задана неверно.")
    except ValueError as err:
        await self.send("Команда задана неверно.")

@bot.command()    
async def echo(self, *words):
    emb = discord.Embed(title = "Эхо", color = 0x00ff00)
    emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url)
    ask = ""
    for word in words:
        ask += word + " "
    emb.add_field(name = "Ответ:", value = ask, inline = False)
    await self.send(embed = emb)

@bot.command()
async def rand(self, x: int, y: int):
    emb = discord.Embed(title = "Генератор случайных чисел", color = 0x00ff00)
    emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url)
    emb.add_field(name = f"Диапазон от {x} до {y}:", value = randint(x, y), inline = False)
    emb.set_footer(text = f"Запрос от {self.message.author}")
    await self.send(embed = emb)

@bot.command()
async def pay(self, member: discord.Member, mon: float):
    with open('economy.json', 'r') as f:
        money = json.load(f)
    if not str(self.author.id) in money:
            money[str(self.author.id)] = {}
            money[str(self.author.id)]['money'] = 0
    if money[str(self.author.id)]['money'] >= mon:
        money[str(self.author.id)]['money'] -= mon
        if not str(member.id) in money:
            money[str(member.id)] = {}
            money[str(member.id)]['money'] = 0
        money[str(member.id)]['money'] += mon
        with open('economy.json', 'w') as f:
            json.dump(money, f)
        emb = discord.Embed(description = f"Вы успешно перевели {member} {mon} денежных единиц.")
        emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url)
        await self.send(embed = emb)
    else:
        emb = discord.Embed(description = "У вас недостаточно денег, проверьте баланс командой .b")
        emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url)
        await self.send(embed = emb)

@bot.command()
async def user(self, member: discord.Member):
    emb = discord.Embed(title = "Пользователь", color = 0x00ff00)
    emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url)
    emb.set_thumbnail(url = member.avatar_url)
    emb.add_field(name = "Имя:", value = member.display_name, inline = False)
    emb.add_field(name = "ID:", value = member.id, inline = False)
    emb.add_field(name = "На сервере с:", value = member.joined_at, inline = False)
    emb.add_field(name = "Дата регистрации:", value = member.created_at, inline = False)
    emb.set_footer(text = f"Запрос от {self.message.author}")
    await self.send(embed = emb)

@bot.command()
async def level(self, member: discord.Member = None):
    if member == None:
        with open('level.json', 'r') as f:
            level = json.load(f)
        if not str(self.author.id) in level:
            level[str(self.author.id)] = {}
            level[str(self.author.id)]['xp'] = 0
            level[str(self.author.id)]['level'] = 1
        emb = discord.Embed(description = f"У вас {level[str(self.author.id)]['level']} уровень и {level[str(self.author.id)]['xp']} опыта.")
        emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url)
        await self.send(embed = emb)
    else:
        with open('level.json', 'r') as f:
            level = json.load(f)
        if not str(member.id) in level:
            level[str(member.id)] = {}
            level[str(member.id)]['xp'] = 0
            level[str(member.id)]['level'] = 1
        emb = discord.Embed(description = f"У {member} {level[str(member.id)]['level']} уровень и {level[str(member.id)]['xp']} опыта.")
        emb.set_author(name = self.message.author, icon_url = self.message.author.avatar_url)
        await self.send(embed = emb)

@bot.event
async def on_message(message):
    if message.author.bot == False:
        with open('level.json', 'r') as f:
            level = json.load(f)
        async def updatedata(user, level):
            if not user in level:
                level[user] = {}
                level[user]['xp'] = 0
                level[user]['level'] = 1  
        async def xp(user, level):
            level[user]['xp'] += randint(5, 12)
        async def lvl(user, level):
            if level[user]['xp'] > level[user]['level'] * 100 + 100:
                level[user]['xp'] = 0
                level[user]['level'] += 1
                emb = discord.Embed(description = f"{message.author} достиг {level[user]['level']} уровня. Поздровляем!")
                await message.channel.send(embed = emb)
        await updatedata(str(message.author.id), level)
        await xp(str(message.author.id), level)
        await lvl(str(message.author.id), level)
        with open('level.json', 'w') as f:
            json.dump(level, f)
        await bot.process_commands(message)

bot.run('')