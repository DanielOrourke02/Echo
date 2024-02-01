import os
from datetime import datetime
from pathlib import Path

from discord import Color, Embed


DEFAULT_BET = 100
B_MULT = 5
B_COOLDOWN = 12


def make_embed(title=None, description=None, color=None, author=None,
               image=None, link=None, footer=None) -> Embed:
    """Wrapper for making discord embeds"""
    embed = Embed(
        title=title,
        description=description,
        url=link,
        color=color if color else Color.random()
    )
    if author: 
        embed.set_author(name=author)
    if image: 
        embed.set_image(url=image)
    if footer: 
        embed.set_footer(text=footer)
    else: 
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
    return embed