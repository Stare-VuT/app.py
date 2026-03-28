import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from database import init_db, get_all_users, get_user, ban_user, unban_user, delete_user, make_admin

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

init_db()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Thay ID này bằng Discord User ID của bạn
ADMIN_IDS = [123456789012345678]


def is_admin():
    async def predicate(ctx):
        return ctx.author.id in ADMIN_IDS
    return commands.check(predicate)


@bot.event
async def on_ready():
    print(f"Bot đã online: {bot.user}")


@bot.command()
@is_admin()
async def userlist(ctx):
    users = get_all_users()

    if not users:
        await ctx.send("Không có tài khoản nào.")
        return

    msg = "**Danh sách tài khoản:**\n"
    for user in users:
        status = "🚫 Banned" if user["banned"] else "✅ Active"
        msg += f"- {user['username']} | {user['role']} | {status}\n"

    await ctx.send(msg)


@bot.command()
@is_admin()
async def userinfo(ctx, username: str):
    user = get_user(username)

    if not user:
        await ctx.send("Không tìm thấy tài khoản.")
        return

    status = "🚫 Banned" if user["banned"] else "✅ Active"

    msg = (
        f"**Thông tin tài khoản:**\n"
        f"Username: {user['username']}\n"
        f"Role: {user['role']}\n"
        f"Status: {status}\n"
        f"Created: {user['created_at']}"
    )
    await ctx.send(msg)


@bot.command()
@is_admin()
async def banuser(ctx, username: str):
    if username == "admin":
        await ctx.send("Không thể khóa tài khoản admin mặc định.")
        return

    if not get_user(username):
        await ctx.send("Không tìm thấy tài khoản.")
        return

    ban_user(username)
    await ctx.send(f"Đã khóa tài khoản: **{username}**")


@bot.command()
@is_admin()
async def unbanuser(ctx, username: str):
    if not get_user(username):
        await ctx.send("Không tìm thấy tài khoản.")
        return

    unban_user(username)
    await ctx.send(f"Đã mở khóa tài khoản: **{username}**")


@bot.command()
@is_admin()
async def deleteuser(ctx, username: str):
    if username == "admin":
        await ctx.send("Không thể xóa tài khoản admin mặc định.")
        return

    if not get_user(username):
        await ctx.send("Không tìm thấy tài khoản.")
        return

    delete_user(username)
    await ctx.send(f"Đã xóa tài khoản: **{username}**")


@bot.command()
@is_admin()
async def makeadminuser(ctx, username: str):
    if not get_user(username):
        await ctx.send("Không tìm thấy tài khoản.")
        return

    make_admin(username)
    await ctx.send(f"Đã cấp quyền admin cho: **{username}**")


bot.run(TOKEN)
