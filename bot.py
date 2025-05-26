
import discord
from discord.ext import commands, tasks
import aiohttp
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

async def pegar_dados_btc():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&tickers=false&market_data=true'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            preco = data['market_data']['current_price']['usd']
            variacao = data['market_data']['price_change_percentage_24h']
            return preco, variacao

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    atualizar_status.start()

@tasks.loop(seconds=60)
async def atualizar_status():
    try:
        preco, variacao = await pegar_dados_btc()
        simbolo = "⬆️" if variacao >= 0 else "⬇️"
        status = f'BTC: ${preco:,.2f} {simbolo}'
        await bot.change_presence(activity=discord.Game(name=status))
    except Exception as e:
        print(f'Erro ao atualizar status: {e}')

@bot.command(name='preco')
async def preco(ctx):
    try:
        preco, variacao = await pegar_dados_btc()
        simbolo = "⬆️" if variacao >= 0 else "⬇️"
        mensagem = f"**📈 BTC**: ${preco:.2f} ({variacao:+.2f}%) {simbolo}"
        await ctx.send(mensagem)
    except Exception as e:
        await ctx.send("Erro ao buscar preço do BTC.")
        print(f'Erro: {e}')

bot.run(TOKEN)
