from nicegui import ui, app
import asyncio
from core.api import api_get

update_badges_func = None


def apply_theme():
    primary_color = app.storage.user.get('primary_color', '#4F46E5')
    font_family = app.storage.user.get('font_family', 'Inter')

    ui.add_head_html(f'''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto:wght@400;500;700&family=Poppins:wght@400;500;600&family=Montserrat:wght@400;500;600&family=Open+Sans:wght@400;500;600&display=swap');

        body {{
            font-family: '{font_family}', sans-serif !important;
            background-color: #f0f2f5;
        }}

        .dark body {{
            background-color: #000000;
        }}

        .bg-unal {{
            background-image: linear-gradient(
                rgba(0, 0, 0, 0.5),
                rgba(0, 0, 0, 0.7)
            ), url('/static/fondo_unal.jpeg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .bg-primary,
        .q-btn.bg-primary {{
            background-color: {primary_color} !important;
            border-color: {primary_color} !important;
        }}

        .text-primary,
        .q-btn.text-primary {{
            color: {primary_color} !important;
        }}

        .border-primary {{
            border-color: {primary_color} !important;
        }}

        .q-field--outlined.q-field--focused .q-field__control::after {{
            border-color: {primary_color} !important;
        }}

        .q-field--outlined.q-field--focused .q-field__label {{
            color: {primary_color} !important;
        }}

        .app-header {{
            min-height: 84px;
        }}

        .app-logo {{
            height: 58px !important;
            width: auto !important;
            object-fit: contain !important;
            flex-shrink: 0 !important;
            display: block !important;
        }}

        .app-nav-group {{
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 8px !important;
            margin-left: auto !important;
            margin-right: 12px !important;
        }}

        .app-nav {{
            width: 82px !important;
            min-width: 82px !important;
            height: 68px !important;
            min-height: 68px !important;
            padding: 0 !important;
            margin: 0 !important;
            border-radius: 22px !important;
            position: relative !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            cursor: pointer !important;
            box-sizing: border-box !important;
            text-align: center !important;
            color: #374151;
            background: transparent;
            transition:
                transform .2s ease,
                background .2s ease,
                color .2s ease,
                box-shadow .2s ease;
        }}

        .app-nav:hover {{
            background: #eff6ff;
            color: {primary_color};
            transform: translateY(-3px);
        }}

        .app-nav.active {{
            background: #eff6ff;
            color: {primary_color};
            box-shadow: 0 8px 20px rgba(37, 99, 235, .10);
        }}

        .app-nav-icon {{
            font-size: 28px !important;
            line-height: 1 !important;
            margin-bottom: 4px !important;
            display: block !important;
        }}

        .app-nav-label {{
            font-size: 11px !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
            margin: 0 !important;
        }}

        .dark .app-nav {{
            color: #d1d5db;
        }}

        .dark .app-nav:hover {{
            background: #172338;
            color: #60a5fa;
        }}

        .dark .app-nav.active {{
            background: #172b45;
            color: #60a5fa;
        }}

        .app-nav-badge {{
            position: absolute !important;
            top: 4px !important;
            right: 9px !important;
            min-width: 18px !important;
            width: auto !important;
            height: 18px !important;
            padding: 0 5px !important;
            margin: 0 !important;
            border-radius: 999px !important;
            background: #ef4444 !important;
            color: white !important;
            font-size: 10px !important;
            font-weight: 800 !important;
            line-height: 18px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-shadow: 0 2px 6px rgba(239, 68, 68, .35);
            z-index: 5 !important;
        }}

        .app-nav-badge.hidden {{
            display: none !important;
        }}

        .app-header-actions {{
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 2px !important;
            flex-shrink: 0 !important;
        }}

        @media(max-width: 900px) {{
            .app-nav {{
                width: 68px !important;
                min-width: 68px !important;
                height: 62px !important;
                min-height: 62px !important;
                border-radius: 18px !important;
            }}

            .app-nav-icon {{
                font-size: 24px !important;
            }}

            .app-nav-label {{
                font-size: 10px !important;
            }}

            .app-nav-group {{
                gap: 3px !important;
            }}

            .app-logo {{
                height: 50px !important;
            }}
        }}

        @media(max-width: 700px) {{
            .app-header {{
                min-height: 70px;
            }}

            .app-nav {{
                width: 54px !important;
                min-width: 54px !important;
                height: 56px !important;
                min-height: 56px !important;
                border-radius: 16px !important;
            }}

            .app-nav-icon {{
                font-size: 21px !important;
            }}

            .app-nav-label {{
                font-size: 9px !important;
            }}

            .app-nav-group {{
                gap: 1px !important;
            }}

            .app-logo {{
                height: 42px !important;
            }}
        }}
    </style>
    ''')


async def load_badges(notif_badge, chat_badge):
    if 'user_id' not in app.storage.user:
        return

    current_user_id = app.storage.user['user_id']

    res_notif = await api_get(
        f"/notifications/unread/{current_user_id}"
    )

    if res_notif.status_code == 200:
        count = res_notif.json().get('count', 0)

        if count > 0:
            notif_badge.set_text(str(count))
            notif_badge.classes(remove='hidden')
        else:
            notif_badge.set_text('')
            notif_badge.classes(add='hidden')

    res_chat = await api_get(
        f"/users/messages/unread/{current_user_id}"
    )

    if res_chat.status_code == 200:
        count = res_chat.json().get('count', 0)

        if count > 0:
            chat_badge.set_text(str(count))
            chat_badge.classes(remove='hidden')
        else:
            chat_badge.set_text('')
            chat_badge.classes(add='hidden')


def nav_item(icon, label, route, active=False):
    classes = 'app-nav active' if active else 'app-nav'

    with ui.element('div').classes(classes).on(
        'click',
        lambda: ui.navigate.to(route)
    ):
        ui.icon(icon).classes('app-nav-icon')
        ui.label(label).classes('app-nav-label')


def app_header(title: str):
    global update_badges_func

    with ui.header().classes(
        'app-header bg-white dark:bg-black '
        'text-gray-900 dark:text-white '
        'items-center px-4 py-2 '
        'border-b border-gray-200 '
        'dark:border-gray-800 shadow-sm'
    ):

        ui.image('/static/logo_unal.png').classes('app-logo')

        ui.space()

        with ui.row().classes('app-nav-group'):

            nav_item(
                'home',
                'Inicio',
                '/feed'
            )

            nav_item(
                'group',
                'Amigos',
                '/friends'
            )

            nav_item(
                'person',
                'Perfil',
                '/myprofile'
            )

            with ui.element('div').classes('app-nav').on(
                'click',
                lambda: ui.navigate.to('/chat')
            ):
                ui.icon('chat_bubble').classes('app-nav-icon')
                ui.label('Chat').classes('app-nav-label')
                chat_badge = ui.badge('').classes(
                    'app-nav-badge hidden'
                )

            with ui.element('div').classes('app-nav').on(
                'click',
                lambda: ui.navigate.to('/notifications')
            ):
                ui.icon('notifications').classes('app-nav-icon')
                ui.label('Avisos').classes('app-nav-label')
                notif_badge = ui.badge('').classes(
                    'app-nav-badge hidden'
                )

            nav_item(
                'settings',
                'Ajustes',
                '/settings'
            )

        with ui.row().classes('app-header-actions'):
            dark = ui.dark_mode()

            ui.button(
                icon='dark_mode',
                on_click=dark.toggle
            ).props(
                'flat round color=black dark:color=white size=md'
            )

            ui.button(
                icon='logout',
                on_click=lambda: (
                    app.storage.user.clear(),
                    ui.navigate.to('/')
                )
            ).props(
                'flat round color=black dark:color=white size=md'
            )

    update_badges_func = lambda: asyncio.create_task(
        load_badges(notif_badge, chat_badge)
    )

    ui.timer(
        3.0,
        lambda: asyncio.create_task(
            load_badges(notif_badge, chat_badge)
        )
    )