import asyncio
import os
import random

import babel.numbers
import discord
from discord.ext import commands

from keep_alive import keep_alive

"""
==========
INCOME TAX
==========
On the first 24,000	10%
On the next 8,333	25%
On all income over 32,333	30%

============
NHIF CHARGES
============
Ksh. 0 to Ksh. 5,999 – Ksh. 150
Ksh. 6,000 to Ksh. 7,999 – Ksh. 300
Ksh. 8,000 to Ksh. 11,999 – Ksh. 400
Ksh. 12,000 to Ksh. 14,999 – Ksh. 500
Ksh. 15,000 to Ksh. 19,999 – Ksh. 600
Ksh. 20,000 to Ksh. 24,999 – Ksh. 750
Ksh. 25,000 to Ksh. 29,999 – Ksh. 850
Ksh. 30,000 to Ksh. 34,999 – Ksh. 900
Ksh. 35,000 to Ksh. 39,000 – Ksh. 950
Ksh. 40,000 to Ksh. 44,999 – Ksh. 1,000
Ksh. 45,000 to Ksh. 49,000 – Ksh. 1,100
Ksh. 50,000 to Ksh. 59,999 – Ksh. 1,200
Ksh. 60,000 to Ksh. 69,999 – Ksh. 1,300
Ksh. 70,000 to Ksh. 79,999 – Ksh. 1,400
Ksh. 80,000 to Ksh. 89,999 – Ksh. 1,500
Ksh. 90,000 to Ksh. 99,999 – Ksh. 1,60
Ksh. 100,000 and above – Ksh. 1,700
"""


def nhif_calculator(salary):
    nhif = 0

    if salary <= 5999:
        nhif = 150
    elif salary >= 6000 and salary <= 7999:
        nhif = 300
    elif salary >= 8000 and salary <= 11999:
        nhif = 400
    elif salary >= 12000 and salary <= 14999:
        nhif = 500
    elif salary >= 15000 and salary <= 19999:
        nhif = 600
    elif salary >= 20000 and salary <= 24999:
        nhif = 750
    elif salary >= 25000 and salary <= 29999:
        nhif = 850
    elif salary >= 30000 and salary <= 34999:
        nhif = 900
    elif salary >= 35000 and salary <= 39999:
        nhif = 950
    elif salary >= 40000 and salary <= 44999:
        nhif = 1000
    elif salary >= 45000 and salary <= 49999:
        nhif = 1100
    elif salary >= 50000 and salary <= 59999:
        nhif = 1200
    elif salary >= 60000 and salary <= 69999:
        nhif = 1300
    elif salary >= 70000 and salary <= 79999:
        nhif = 1400
    elif salary >= 80000 and salary <= 89999:
        nhif = 1500
    elif salary >= 90000 and salary <= 99999:
        nhif = 1600
    elif salary >= 100000:
        nhif = 1700

    return nhif


NSSF = 200
personal_relief = 2400


def calculate_tax(salary):

    taxable_pay = salary - NSSF
    if salary > 0 and salary <= 24000:
        income_tax = taxable_pay * 0.1

    if salary > 24000 and salary <= 32333:
        first_iteration = taxable_pay - 24000
        first_tax = 2380
        second_tax = first_iteration * 0.25
        income_tax = first_tax + second_tax

    if salary > 32333:
        first_iteration = 8333
        second__iteration = taxable_pay - 24000 - 8333

        first_tax = 2380
        second_tax = 0.25 * first_iteration
        third_tax = 0.30 * second__iteration

        income_tax = first_tax + second_tax + third_tax

    return income_tax


client = commands.Bot(command_prefix="!")

__games__ = [
    (discord.ActivityType.playing, "with iamksm"),
    (discord.ActivityType.watching, "over {guilds} Server"),
    (discord.ActivityType.watching, "over {members} Members"),
    (discord.ActivityType.listening, "to ! commands"),
]
__gamesTimer__ = 60 * 60  # 60 minutes


@client.event
async def on_ready():
    print("Bot's Ready")
    while True:
        guildCount = len(client.guilds)
        memberCount = len(list(client.get_all_members()))
        randomGame = random.choice(__games__)
        await client.change_presence(
            activity=discord.Activity(
                type=randomGame[0],
                name=randomGame[1].format(guilds=guildCount, members=memberCount),
            )
        )
        await asyncio.sleep(__gamesTimer__)


@client.command(aliases=["tax"])
async def calculate_net_pay(ctx, salary):
    NSSF = 200
    personal_relief = 2400

    salary = int(salary)
    if salary >= 0 and salary <= 23999:
        embed = discord.Embed(
            title="KRA TAX CALCULATOR",
            description="P.A.Y.E is chargeable to persons of employment monthly income of Kshs. 24,000 and above",
            color=discord.Color.red(),
        )
        embed.set_thumbnail(
            url="https://pbs.twimg.com/profile_images/1412006848857772032/9txppbC0.jpg"
        )

        return await ctx.send(embed=embed)

    taxable_pay = salary - NSSF
    income_tax = calculate_tax(salary)
    nhif = nhif_calculator(salary)

    if salary >= 24000:
        PAYE = income_tax - personal_relief
    else:
        PAYE = 0

    pay_after_tax = taxable_pay - PAYE
    net_pay = pay_after_tax - nhif

    format_currency = babel.numbers.format_currency

    salary = format_currency(salary, "KES", locale="en_KE")
    NSSF = format_currency(NSSF, "KES", locale="en_KE")
    taxable_pay = format_currency(taxable_pay, "KES", locale="en_KE")
    income_tax = format_currency(income_tax, "KES", locale="en_KE")
    nhif = format_currency(nhif, "KES", locale="en_KE")
    PAYE = format_currency(PAYE, "KES", locale="en_KE")
    pay_after_tax = format_currency(pay_after_tax, "KES", locale="en_KE")
    net_pay = format_currency(net_pay, "KES", locale="en_KE")
    personal_relief = format_currency(personal_relief, "KES", locale="en_KE")

    payslip = {
        "BASIC PAY": salary,
        "NSSF": NSSF,
        "TAXABLE PAY": taxable_pay,
        "INCOME TAX": income_tax,
        "PERSONAL RELIEF": personal_relief,
        "P.A.Y.E.": PAYE,
        "PAY AFTER TAX": pay_after_tax,
        "NHIF": nhif,
        "NET PAY": net_pay,
    }

    print(payslip)

    embed = discord.Embed(
        title="KRA TAX CALCULATOR",
        description="INCOME TAX",
        color=discord.Color.red(),
    )
    embed.set_thumbnail(
        url="https://pbs.twimg.com/profile_images/1412006848857772032/9txppbC0.jpg"
    )
    embed.add_field(name="BASIC PAY", value=salary.replace("Ksh", "Ksh ")),
    embed.add_field(name="NSSF", value=NSSF.replace("Ksh", "Ksh ")),
    embed.add_field(name="TAXABLE PAY", value=taxable_pay.replace("Ksh", "Ksh ")),
    embed.add_field(name="INCOME TAX", value=income_tax.replace("Ksh", "Ksh ")),
    embed.add_field(
        name="PERSONAL RELIEF", value=personal_relief.replace("Ksh", "Ksh ")
    ),
    embed.add_field(name="P.A.Y.E.", value=PAYE.replace("Ksh", "Ksh ")),
    embed.add_field(name="PAY AFTER TAX", value=pay_after_tax.replace("Ksh", "Ksh ")),
    embed.add_field(name="NHIF", value=nhif.replace("Ksh", "Ksh ")),
    embed.add_field(
        name="======================================",
        value="=====================================",
        inline=False,
    )
    embed.add_field(name="NET PAY", value=net_pay.replace("Ksh", "Ksh "), inline=False),

    await ctx.send(embed=embed)


keep_alive()
client.run(os.getenv("TOKEN"))
