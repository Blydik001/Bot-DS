import discord
import datetime
import random
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput

# Класс модального окна для заявки
class GuildApplicationModal(Modal, title="Заявка в гильдию «Отдел 71-75»"):
    name = TextInput(
        label="Ваше имя в игре",
        placeholder="Введите ваше имя...",
        required=True
    )
    experience = TextInput(
        label="Опыт игры (в месяцах)",
        placeholder="Например: 6 месяцев",
        required=True
    )
    why_join = TextInput(
        label="Почему хотите вступить?",
        placeholder="Расскажите о себе...",
        style=discord.TextStyle.paragraph,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Отправляем заявку в канал для заявок
        channel = interaction.guild.get_channel(ВАШ_ID_КАНАЛА)  # Замените на ID канала
        if channel:
            embed = discord.Embed(
                title="Новая заявка в гильдию",
                color=discord.Color.blue()
            )
            embed.add_field(name="Игрок", value=interaction.user.mention, inline=False)
            embed.add_field(name="Имя в игре", value=self.name, inline=False)
            embed.add_field(name="Опыт", value=self.experience, inline=False)
            embed.add_field(name="Причина вступления", value=self.why_join, inline=False)
            await channel.send(embed=embed)

        # Подтверждение пользователю
        await interaction.response.send_message(
            "✅ Ваша заявка отправлена! Ожидайте ответа администрации.",
            ephemeral=True  # Только для пользователя
        )

TECH_QUOTES = [
    "я вкусно покушал",
    "тестовая цитата"
]

MARCH_8_GREETINGS = [
    "Дорогие девушки, с Международным женским днём! 🌸 Пусть весна принесёт вам море радости, улыбок и приятных сюрпризов! 💐",
    "С 8 Марта, прекрасные дамы! ✨ Желаю вам бесконечного счастья, любви и исполнения всех заветных желаний! 💖",
    "От всего сердца поздравляю вас с 8 Марта! 🌺 Пусть каждый день будет наполнен теплом, улыбками и чудесными моментами! 🌷",
    "С праздником весны, милые девушки! 💐 Желаю вам море цветов, комплиментов и незабываемых впечатлений! 🌸",
    "С Международным женским днём! 🌹 Пусть ваша жизнь будет такой же прекрасной, как вы сами — яркой, цветущей и удивительной! ✨",
    "Дорогие дамы, с 8 Марта! 🌟 Желаю вам крепкого здоровья, благополучия и море положительных эмоций! 🌸💐",
    "С праздником, очаровательные девушки! 🌺 Пусть весна подарит вам вдохновение, радость и новые возможности! ✨",
    "От всей души поздравляю вас с 8 Марта! 💐 Желаю счастья, любви, удачи во всех делах и отличного настроения каждый день! 🌸",
    "Милые девушки, с праздником весны! 🌷 Пусть каждый ваш день будет наполнен солнечным светом, теплом и заботой близких! 💖",
    "С 8 Марта, дорогие! 🌸 Желаю вам оставаться такими же прекрасными, вдохновляющими и удивительными! Пусть мечты сбываются! ✨"
]


# Настройки бота
intents = discord.Intents.default()
intents.members = True  # Для отслеживания присоединения пользователей
intents.moderation = True
intents.message_content = True  # Для чтения сообщений
bot = commands.Bot(command_prefix='!', intents=intents)

# ID канала для приветствий (замените на ваш)
WELCOME_CHANNEL_ID = 1407366159795486853


@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен!')

@bot.event
async def on_member_join(member):
    # Отправляем приветствие в канал сервера
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f'Добро пожаловать, {member.mention}! Рады видеть тебя на сервере! 👋')



@bot.command(name='сервер')
async def server_info(ctx):
    """Показывает полную статистику сервера с кнопками действий"""
    guild = ctx.guild

    # Собираем статистику
    total_members = guild.member_count
    human_members = sum(1 for member in guild.members if not member.bot)
    bot_members = total_members - human_members

    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)
    total_channels = text_channels + voice_channels

    roles_count = len(guild.roles)
    online_members = sum(1 for member in guild.members if member.status != discord.Status.offline)

    # Создаём embed со статистикой
    embed = discord.Embed(
        title=f"📊 Статистика сервера: {guild.name}",
        color=discord.Color.blurple(),
        timestamp=ctx.message.created_at
    )

    embed.add_field(name="👥 Участники", value=f"Всего: {total_members}\nЛюдей: {human_members}\nБотов: {bot_members}", inline=True)
    embed.add_field(name="📁 Каналы", value=f"Текстовые: {text_channels}\nГолосовые: {voice_channels}\nКатегории: {categories}\nВсего: {total_channels}", inline=True)
    embed.add_field(name="🛡️ Роли", value=roles_count, inline=True)
    embed.add_field(name="🌍 Онлайн", value=online_members, inline=True)
    embed.add_field(name="👑 Владелец", value=guild.owner.mention, inline=True)
    embed.add_field(name="🗓️ Создан", value=guild.created_at.strftime("%d.%m.%Y"), inline=True)
    embed.add_field(name="🆔 ID сервера", value=guild.id, inline=False)

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    # Добавляем кнопки действий
    view = ServerActionsView(ctx)

    await ctx.send(embed=embed, view=view)

@bot.command(name='цитата')
async def tech_quote(ctx):
    """
    Выводит случайную цитату про технический отдел 71-75 проекта BLACK RUSSIA.
    """
    # Выбираем случайную цитату из списка
    random_quote = random.choice(TECH_QUOTES)

    # Создаём embed-сообщение
    embed = discord.Embed(
        title="📜 Цитата дня",
        description=random_quote,
        color=discord.Color.dark_blue(),
        timestamp=ctx.message.created_at
    )

    # Отправляем сообщение
    await ctx.send(embed=embed)

@bot.command(name='msg')
async def send_to_channel(ctx, channel_id: int, *, message: str):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
        await ctx.send(f"Сообщение отправлено в канал {channel.mention}!")
    else:
        await ctx.send("Канал не найден!")


# Команда выдачи роли
@bot.command(name='role')
@commands.has_permissions(manage_roles=True)
async def role(ctx, member: discord.Member, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await ctx.send(f'Роль "{role_name}" выдана пользователю {member.mention}.')
    else:
        await ctx.send(f'Роль "{role_name}" не найдена.')


# Команда бана
@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, user_identifier: str, *, reason="Причина не указана"):
    """Забанить пользователя по ID, имени или имени#дискриминатору"""

    if user_identifier is None:
        await ctx.send(
            "❌ Укажите пользователя для бана!\n"
            "Использование:\n"
            "- `!бан UserName` (по имени)\n"
            "- `!бан UserName#1234` (по имени и дискриминатору)\n"
            "- `!бан 123456789012345678` (по ID)\n"
            "Дополнительно можно указать причину: `!бан UserName оскорбление`"
        )
        return

    try:
        # Ищем пользователя на сервере
        target_member = None

        # Поиск по ID
        if user_identifier.isdigit():
            user_id = int(user_identifier)
            target_member = ctx.guild.get_member(user_id)

            # Если пользователя нет на сервере, но он может быть забанен по ID
            if not target_member:
                # Пытаемся забанить по ID напрямую
                await ctx.guild.ban(discord.Object(id=user_id), reason=reason)
                await ctx.send(f"✅ Пользователь с ID `{user_id}` забанен (не на сервере). Причина: {reason}")
                return

        else:
            # Поиск по имени или имени#дискриминатору среди участников сервера
            target_member = discord.utils.find(
                lambda m: m.name == user_identifier or str(m) == user_identifier,
                ctx.guild.members
            )

        if not target_member:
            await ctx.send(f"❌ Пользователь `{user_identifier}` не найден на сервере.")
            return

        # Проверяем, можно ли забанить этого пользователя (иерархия ролей)
        if target_member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send("❌ Вы не можете забанить пользователя с равной или более высокой ролью.")
            return

        if target_member.top_role >= ctx.guild.me.top_role:
            await ctx.send("❌ Бот не может забанить пользователя с ролью выше или равной моей.")
            return

        # Выполняем бан
        await target_member.ban(reason=reason)

        embed = discord.Embed(
            title="✅ Пользователь забанен",
            description=f"{ctx.author.mention} забанил {target_member.mention}",
            color=discord.Color.red(),
            timestamp=ctx.message.created_at
        )
        embed.add_field(name="Причина", value=reason, inline=False)
        embed.set_footer(text=f"Выполнено модератором: {ctx.author.display_name}")
        await ctx.send(embed=embed)

    except discord.Forbidden:
        await ctx.send("❌ У бота недостаточно прав для бана.")
    except Exception as e:
        await ctx.send(f"❌ Ошибка при бане: {e}")



# Команда кика
@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} был кикнут. Причина: {reason or "не указана"}')


# Команда мута (временного запрета на отправку сообщений)
@bot.command(name='mute')
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, duration: int, *, reason=None):
    # Создаём роль мута, если её нет
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted", reason="Создание роли для мута")
        # Запрещаем отправку сообщений во всех каналах для этой роли
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False)

    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f'{member.mention} получил мут на {duration} минут. Причина: {reason or "не указана"}')

    # Автоматический размут через указанное время
    import asyncio
    await asyncio.sleep(duration * 60)
    await member.remove_roles(mute_role)
    await ctx.send(f'Мут снят с {member.mention}.')


@bot.command(name='кандидат')
@commands.has_permissions(manage_roles=True)  # Проверка прав администратора
async def кандидат(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Кандидат на теха")
    if not role:
        await ctx.send("❌ Роль «Кандидат на обзвон» не найдена! Создайте её заранее.")
        return

    await user.add_roles(role)
    await ctx.send(f"✅ Роль «Кандидат на обзвон» выдана пользователю {user.mention}.")

@bot.command(name='снят')
@commands.has_permissions(ban_members=True)  # Проверка прав на кик/бан
async def снят(ctx, user: discord.Member):
    # Удаляем все роли пользователя
    await user.remove_roles(*user.roles[1:])  # [1:] — исключаем @everyone

    # Кикаем пользователя с сервера
    await user.kick(reason="Пользователь снят по команде !снят")

    await ctx.send(f"✅ Пользователь {user.mention} снят с сервера, все роли удалены.")

@bot.command(name='stats')
async def stats(ctx, user: discord.Member = None):
    # Если пользователь не указан, берём автора команды
    if user is None:
        user = ctx.author

    # Получаем список ролей пользователя
    roles = ', '.join([role.name for role in user.roles[1:]])  # [1:] — исключаем @everyone
    if not roles:
        roles = "Нет ролей"


    # Время нахождения на сервере (дата присоединения)
    if user.joined_at:
        join_date = user.joined_at.strftime('%d.%m.%Y %H:%M:%S')
        days_on_server = (ctx.message.created_at.date() - user.joined_at.date()).days
    else:
        join_date = "Неизвестно"
        days_on_server = "Неизвестно"

    # Подсчёт сообщений в текущем канале
    msg_count = 0
    try:
        async for message in ctx.channel.history(limit=1000):
            if message.author == user:
                msg_count += 1
    except discord.Forbidden:
        msg_count = "Доступ запрещён"

    # Расчёт времени в голосовом чате
    voice_time_str = "Не был в голосовых каналах"

    if user.voice and user.voice.channel:
        # Пользователь сейчас в голосовом канале
        # Точного времени подключения через API нет, показываем факт присутствия
        voice_time_str = f"В канале: {user.voice.channel.name}"

    # Формируем embed‑сообщение
    embed = discord.Embed(
        title=f"Статистика пользователя {user.display_name}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Никнейм", value=user.display_name, inline=False)
    embed.add_field(name="Роли", value=roles, inline=False)
    embed.add_field(name="Присоединился к серверу", value=join_date, inline=False)
    embed.add_field(name="Дней на сервере", value=str(days_on_server), inline=False)
    embed.add_field(name="Сообщений в этом чате", value=str(msg_count), inline=False)
    embed.add_field(name="Время в голосовых каналах", value=voice_time_str, inline=False)

    # Получение URL аватара
    if user.avatar:
        embed.set_thumbnail(url=user.avatar.url)
    else:
        embed.set_thumbnail(url=user.default_avatar.url)

    await ctx.send(embed=embed)

@bot.command(name='top')
async def top_messages(ctx, limit: int = 10):
    """
    Показывает топ пользователей по количеству сообщений в текущем канале.
    limit — количество пользователей в топе (по умолчанию 10).
    """
    if limit < 1:
        await ctx.send("Лимит должен быть положительным числом!")
        return
    if limit > 50:
        limit = 50  # Ограничиваем максимум 50 для производительности

    await ctx.send(f"Собираю статистику сообщений за последние 1000 сообщений...")

    message_counts = {}

    try:
        # Собираем статистику по сообщениям
        async for message in ctx.channel.history(limit=1000):
            author_id = message.author.id
            if author_id not in message_counts:
                message_counts[author_id] = {
                    'user': message.author,
            'count': 1
        }
            else:
                message_counts[author_id]['count'] += 1

        # Сортируем по убыванию количества сообщений
        sorted_users = sorted(
            message_counts.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )

        # Берём топ‑N пользователей
        top_users = sorted_users[:limit]

        # Создаём embed для отображения топа
        embed = discord.Embed(
            title=f"Топ-{limit} по сообщениям в канале #{ctx.channel.name}",
            color=discord.Color.gold(),
            timestamp=ctx.message.created_at
        )

        for i, (user_id, data) in enumerate(top_users, start=1):
            user = data['user']
            count = data['count']
            # Убираем @everyone из имени ролей для краткости
            roles = [role.name for role in user.roles[1:] if role.name != "@everyone"]
            main_role = roles[0] if roles else "Нет ролей"

            embed.add_field(
                name=f"{i}. {user.display_name}",
                value=f"**Сообщений:** {count}\n**Роль:** {main_role}",
                inline=False
            )

        await ctx.send(embed=embed)

    except discord.Forbidden:
        await ctx.send("У бота нет прав на чтение истории сообщений в этом канале.")
    except Exception as e:
        await ctx.send(f"Произошла ошибка при сборе статистики: {e}")@bot.command(name='топ')
async def top_messages(ctx, limit: int = 10):
    """
    Показывает топ пользователей по количеству сообщений в текущем канале.
    limit — количество пользователей в топе (по умолчанию 10).
    """
    if limit < 1:
        await ctx.send("Лимит должен быть положительным числом!")
        return
    if limit > 50:
        limit = 50  # Ограничиваем максимум 50 для производительности

    await ctx.send(f"Собираю статистику сообщений за последние 1000 сообщений...")

    message_counts = {}

    try:
        # Собираем статистику по сообщениям
        async for message in ctx.channel.history(limit=1000):
            author_id = message.author.id
            if author_id not in message_counts:
                message_counts[author_id] = {
                    'user': message.author,
            'count': 1
        }
            else:
                message_counts[author_id]['count'] += 1

        # Сортируем по убыванию количества сообщений
        sorted_users = sorted(
            message_counts.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )

        # Берём топ‑N пользователей
        top_users = sorted_users[:limit]

        # Создаём embed для отображения топа
        embed = discord.Embed(
            title=f"Топ-{limit} по сообщениям в канале #{ctx.channel.name}",
            color=discord.Color.gold(),
            timestamp=ctx.message.created_at
        )

        for i, (user_id, data) in enumerate(top_users, start=1):
            user = data['user']
            count = data['count']
            # Убираем @everyone из имени ролей для краткости
            roles = [role.name for role in user.roles[1:] if role.name != "@everyone"]
            main_role = roles[0] if roles else "Нет ролей"

            embed.add_field(
                name=f"{i}. {user.display_name}",
                value=f"**Сообщений:** {count}\n**Роль:** {main_role}",
                inline=False
            )

        await ctx.send(embed=embed)

    except discord.Forbidden:
        await ctx.send("У бота нет прав на чтение истории сообщений в этом канале.")
    except Exception as e:
        await ctx.send(f"Произошла ошибка при сборе статистики: {e}")

@bot.command(name='id')
async def user_id(ctx, user: discord.Member = None):
    """
    Показывает ID и никнейм пользователя.
    Если пользователь не указан, показывает данные автора команды.
    """
    if user is None:
        user = ctx.author

    # Получаем отображаемое имя (nickname на сервере)
    display_name = user.display_name

    # Полное имя пользователя Discord: username#discriminator
    full_name = f"{user.name}#{user.discriminator}"

    embed = discord.Embed(
        title="Информация о пользователе",
        color=discord.Color.green(),
        timestamp=ctx.message.created_at
    )

    embed.add_field(
        name="Никнейм на сервере",
        value=display_name,
        inline=False
    )
    embed.add_field(
        name="Полное имя Discord",
        value=full_name,
        inline=False
    )
    embed.add_field(
        name="ID пользователя",
        value=user.id,
        inline=False
    )

    # Добавляем аватар пользователя
    if user.avatar:
        embed.set_thumbnail(url=user.avatar.url)
    else:
        embed.set_thumbnail(url=user.default_avatar.url)

    await ctx.send(embed=embed)


# Обработка ошибок
@role.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('❌ Используйте: `!роль @пользователь (роль)`')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('❌ Не удалось найти пользователя или роль. Проверьте правильность упоминания и названия роли.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ У вас нет прав для выдачи ролей!')
    else:
        await ctx.send(f'❌ Произошла ошибка: {error}')

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('❌ Используйте: `!мут @пользователь время (в минутах) причина`')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('❌ Некорректное время или упоминание пользователя. Пример: `!mute @User 10 Спам`')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ У вас нет прав для выдачи мута!')
    else:
        await ctx.send(f'❌ Произошла ошибка: {error}')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('❌ Используйте: `!кик @пользователь причина`')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('❌ Не удалось найти пользователя. Упомяните его правильно, например: `!kick @User Нарушение правил`')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ У вас нет прав для кика!')
    else:
        await ctx.send(f'❌ Произошла ошибка: {error}')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('❌ Используйте: `!бан @пользователь время (в днях) причина`')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('❌ Некорректное время или упоминание пользователя. Пример: `!ban @User 7 Спам`')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ У вас нет прав для бана!')
    else:
        await ctx.send(f'❌ Произошла ошибка: {error}')

@кандидат.error
async def кандидат_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Используйте: `!кандидат @пользователь`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Не удалось найти пользователя. Упомяните его правильно.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ У вас нет прав для выдачи ролей!")

@снят.error
async def снят_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Используйте: `!снят @пользователь`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Не удалось найти пользователя. Упомяните его правильно.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ У вас нет прав для снятия с должности!")

@bot.command(name='8march')
async def march_8_greeting(ctx):
    """
    Поздравляет девушек с 8 Марта случайным поздравлением из списка.
    """
    # Выбираем случайное поздравление
    random_greeting = random.choice(MARCH_8_GREETINGS)

    # Создаём embed‑сообщение
    embed = discord.Embed(
        title="🌸 С Международным женским днём! 🌸",
        description=random_greeting,
        color=discord.Color.from_rgb(255, 105, 180),  # Нежно‑розовый цвет
        timestamp=ctx.message.created_at
    )

    # Добавляем изображение (опционально)
    embed.set_image(url="https://ibb.co/jvFZpsS8")  # Замените на реальную ссылку

    # Альтернатива: используйте стандартное изображение
    # embed.set_thumbnail(url="https://media.giphy.com/media/3o7aCTPPmYfkuO0b0w/giphy.gif")

    # Футер с подписью
    embed.set_footer(
        text="С любовью от бота • 8 Марта",
        icon_url=ctx.bot.user.avatar.url if ctx.bot.user.avatar else None
    )

    await ctx.send(embed=embed)


@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_identifier: str = None):
    if user_identifier is None:
        await ctx.send(
            "❌ Укажите пользователя для разбана!\n"
            "Использование:\n"
            "- `!unban UserName` (по имени)\n"
            "- `!unbanUserName#1234` (по имени и дискриминатору)\n"
            "- `!unban 123456789012345678` (по ID)"
        )
        return

    try:
        # Получаем список забаненных пользователей
        bans = [entry async for entry in ctx.guild.bans()]
        banned_user = None
        ban_reason = None

        # Обработка разных форматов ввода
        if user_identifier.isdigit():
            # Введён ID пользователя
            user_id = int(user_identifier)
            banned_user = discord.utils.find(
                lambda ban: ban.user.id == user_id,
                bans
            )
            if banned_user:
                banned_user = banned_user.user
        else:
            # Ищем по имени или имени#дискриминатору
            banned_user = discord.utils.find(
                lambda ban: str(ban.user) == user_identifier or ban.user.name == user_identifier,
                bans
            )
            if banned_user:
                banned_user = banned_user.user
                ban_reason = banned_user.reason

        if not banned_user:
            await ctx.send(f"❌ Пользователь `{user_identifier}` не найден в списке забаненных.")
            return

        # Разбаниваем
        await ctx.guild.unban(banned_user, reason=f"Разбан от {ctx.author}")

        embed = discord.Embed(
            title="✅ Пользователь разбанен",
            description=f"{ctx.author.mention} разбанил {banned_user.mention}",
            color=discord.Color.green(),
            timestamp=ctx.message.created_at
        )
        if ban_reason:
            embed.add_field(name="Причина бана", value=ban_reason, inline=False)
        embed.set_footer(text=f"Выполнено модератором: {ctx.author.display_name}")
        await ctx.send(embed=embed)

    except discord.Forbidden:
        await ctx.send("❌ У бота недостаточно прав для разбана.")
    except Exception as e:
        await ctx.send(f"❌ Ошибка при разбане: {e}")

        @bot.command(name='clear')
        @commands.has_permissions(manage_messages=True)
        async def clear(ctx, amount: int = None):
            """Очищает указанное количество сообщений (по умолчанию — 10)"""

            # Проверка аргумента
            if amount is None:
                await ctx.send(
                    "❌ Укажите количество сообщений для удаления!\nИспользование: `!очистить <число>` (максимум 100)")
                return

            if amount <= 0:
                await ctx.send("❌ Количество должно быть положительным числом!")
                return

            if amount > 100:
                await ctx.send("❌ Нельзя удалить больше 100 сообщений за раз!")
                return

            try:
                # Удаляем сообщения (исключаем саму команду)
                deleted = await ctx.channel.purge(limit=amount + 1, check=lambda m: not m.pinned)

                # Показываем результат
                embed = discord.Embed(
                    title="🗑️ Сообщения удалены",
                    description=f"Удалено **{len(deleted) - 1}** сообщений в канале {ctx.channel.mention}",
                    color=discord.Color.orange(),
                    timestamp=ctx.message.created_at
                )
                embed.set_footer(text=f"Выполнено модератором: {ctx.author.display_name}")
                msg = await ctx.send(embed=embed)

                # Автоматически удаляем сообщение о результате через 5 секунд
                await asyncio.sleep(5)
                await msg.delete()

            except discord.Forbidden:
                await ctx.send("❌ У бота нет прав на удаление сообщений в этом канале.")
            except discord.HTTPException as e:
                await ctx.send(f"❌ Ошибка при удалении сообщений: {e}")
            except Exception as e:
                await ctx.send(f"❌ Непредвиденная ошибка: {e}")




# Запуск бота
bot.run('MTQ4MDI0NjYxMzI3NTQ0NzM0Nw.GNCSl2.UnKWAQrUFZebq-89ebCea23gSyWrn4Ao_g3XnI')  # Замените на токен вашего бота
