from flask import Flask, request
import discord
from discord.ext import commands
import feedparser
from datetime import datetime, timezone
from dateutil import parser as date_parser
import asyncio
import discord
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=discord.Intents(), command_prefix = ["ec!","Ec!","EC!","eC!"],case_insensitive=True)
dates_recuperees = set()

materiel_references = {
    "3COM": "4210 3CR17333A-91",
    "Alcatel": "0S6250",
    "Alcatel-P24": "0S6250-P24",
    "Alcatel-24": "Lucent 0S6450-24",
    "Alcatel-P24": "Lucent 0S6450-P24",
    "Lucent": "Lucent LS6212",
    "Lucent-P": "Lucent LS6212P",
    "Cisco": "2950",
    "Cisco-XL": "3500 series XL",
    "Cisco-SF200-24P": "SF200-24P",
    "D-Link": "DGS-1024D",
    "D-Link-24": "DGS-1100-24",
    "D-Link-3100-24": "DGS-3100-24",
    "Dell-MD3200i": "MD3200i",
    "Dell-R420": "PowerEdge R420",
    "Dell-R430": "PowerEdge R430",
    "Dell-T310": "PowerEdge T310",
    "Dell-T420": "PowerEdge T420",
    "Fortinet": "Fortigate 100D",
    "HP-J4813A": "2524 J4813A",
    "HP-J4900B": "2626 J4900B",
    "HP-2510G-48": "Procurve 2510G-48",
    "HP-BL460C": "Proliant BL460C",
    "HP-Stockage": "Stockage",
    "Juniper": "SSG-140",
    "Lenovo": "System x 3650 M5",
    "Nortel-PWR": "2526T-PWR",
    "Nortel-GTX": "4526GTX",
    "Proxmox": "VE 6",
    "RAD": "ETX-203ax",
    "Sonicwall": "Pro 200",
    "Synology": "DS416",
    "UniFi-Pro": "UDM Pro",
    "UniFi-USW": "USW",
    "UniFi-Pro-48": "USW Pro 48",
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    await start_rss_checker()

async def start_rss_checker():
    await check_rss()

async def send_rss_notification(channel, title, link):
    embed = discord.Embed(title=title, description=link, color=0x00ff00)
    await channel.send(embed=embed)

async def check_rss():
    date_2024 = datetime(2024, 1, 1, tzinfo=timezone.utc)

    rss_urls = [
        'https://www.cert.ssi.gouv.fr/actualite/feed/',
        'https://www.cert.ssi.gouv.fr/alerte/feed/',
        'https://www.cert.ssi.gouv.fr/avis/feed/',
        'https://www.cert.ssi.gouv.fr/ioc/feed/',
        'https://www.cert.ssi.gouv.fr/cti/feed/',
        'https://www.ansible.com/blog/rss.xml',
        'https://docker.com/blog/feed',
        'https://about.gitlab.com/atom.xml',
        'https://cve.mitre.org/data/rss/official-cve-board-list-approved.xml',
        'https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss-analyzed.xml',
        'https://kb.isc.org/rss.xml',
        'http://127.0.0.1:3000/user'
    ]

    while True:
        for rss_url in rss_urls:
            try:
                feed = feedparser.parse(rss_url)
            except Exception as e:
                print(f"Erreur lors de la récupération du flux RSS {rss_url}: {e}")
                continue

            for entry in feed.entries:
                try:
                    published_date = date_parser.parse(entry.published)
                except ValueError as ve:
                    print(f"Erreur lors de la conversion de la date pour le flux RSS {rss_url}: {ve}")
                    continue

                if published_date > date_2024 and published_date not in dates_recuperees:
                    for material_name, reference in materiel_references.items():
                        if material_name.lower() in entry.title.lower():


                            ch=await bot.fetch_channel(1227632955380203530)
                            await send_rss_notification(ch, f"Nom du matériel : {material_name}\nRéférence : {reference}", entry.link)





                            dates_recuperees.add(published_date)
                            break

        await asyncio.sleep(60)



bot.run(os.getenv('TOKEN'))
