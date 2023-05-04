import os
import discord
from discord.ext import commands
#import matplotlib.pyplot as plt
import io
import requests
from PIL import Image
import time

from Trading_Bot_V4 import get_current_price, predict_future_prices, predict_signal, model, k, pair

lookback_minutes = 60

# Get your Discord bot token
TOKEN = 'MTEwMDI0MjMzNDM3MDc2Mjc2Mw.G1isKX.FmdvPjCDJNsjXsUyHRW5IowZsKTjrO8cPFBXQ8'

# Create a new bot instance
bot = commands.Bot(command_prefix='!')

# Command to fetch the latest price
@bot.command(name='price', help='Fetches the latest price for the specified asset')
async def get_price(ctx):

    current_price = get_current_price()
    await ctx.send(f'The current price of {pair} is ${current_price:.2f}')

# Command to provide a buy or sell signal based on the model's prediction
@bot.command(name='signal')
async def get_signal(ctx):
    df = fetch_data(pair, interval, num_intervals, lookback_minutes)
    start_time = int(time.time()) - (k * 60)
    num_steps = 1
    interval_minutes = 1
    signal = predict_signal(model, k, start_time, num_steps, interval_minutes, close_scaler)
    await ctx.send(f'Predicted Signal: {signal}')

@bot.command(name='chart')
async def show_chart(ctx):
    df = fetch_data(pair, interval, num_intervals, lookback_minutes)
    start_time = int(time.time()) - (k * 60)
    num_steps = 60
    interval_minutes = 1
    time_range, y_pred = predict_future_prices(model, k, start_time, num_steps, interval_minutes, close_scaler)
    # Plotting code...


    # Plot the chart
    plt.figure(figsize=(16, 8))
    plt.plot(time_range, y_pred)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(f'Projected Prices for {pair}')

    # Save the chart to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert the bytes buffer to a discord.File
    chart_image = discord.File(buf, filename='price_projection_chart.png')

    # Send the chart image in the message
    await ctx.send(file=chart_image)

# Start the bot
bot.run(TOKEN)

