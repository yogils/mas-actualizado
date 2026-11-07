import asyncio
import httpx
from nicegui import ui, app
from core.api import api_get, api_post
from core.theme import apply_theme

API = 'http://localhost:8000'


def media(url):
    return f'{API}{url}' if url else None


def avatar(url, name, classes='w-11 h-11'):
    if url:
        ui.image(media(url)).classes(
            f'{classes} rounded-full object-cover'
        )
    else:
        ui.avatar(
            (name or 'U')[0].upper(),
            color='primary',
            text_color='white'
        ).classes(classes)


def top_button(icon, label, route, active=False):
    color = '#2563eb' if active else '#374151'
    background = '#eff6ff' if active else 'transparent'

    with ui.element('div').classes('nav-item').style(
        f'''
        width:82px;
        height:68px;
        min-width:82px;
        display:flex;
        flex-direction:column !important;
        align-items:center !important;
        justify-content:center !important;
        gap:5px;
        border-radius:22px;
        cursor:pointer;
        background:{background};
        transition:all .2s ease;
        box-sizing:border-box;
        '''
    ).on('click', lambda: ui.navigate.to(route)):

        ui.icon(icon).style(
            f'''
            font-size:28px;
            line-height:28px;
            color:{color};
            display:block;
            margin:0;
            '''
        )

        ui.label(label).style(
            f'''
            font-size:11px;
            line-height:14px;
            font-weight:700;
            color:{color};
            display:block;
            margin:0;
            white-space:nowrap;
            '''
        )


def activity_item(icon, label):
    with ui.row().classes(
        'activity-item w-full items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer'
    ):
        ui.icon(icon).classes(
            'text-[20px] text-blue-600'
        )
        ui.label(label).classes(
            'text-sm font-semibold text-gray-700'
        )


@ui.page('/feed')
async def feed_page():
    apply_theme()

    if 'token' not in app.storage.user:
        ui.navigate.to('/')
        return

    current_user_id = app.storage.user.get('user_id')
    user_email = app.storage.user.get('email', 'U')

    profile_res = await api_get(
        f'/users/profiles/{current_user_id}'
    )

    profile = (
        profile_res.json()
        if profile_res.status_code == 200
        else {}
    )

    user_name = (
        profile.get('full_name')
        or profile.get('name')
        or user_email
    )

    profile_picture = profile.get(
        'profile_picture_url'
    )

    ui.add_head_html('''
    <style>
        body {
            background: #f3f6fa;
        }

        .topbar {
            background: rgba(255,255,255,.98);
            border-bottom: 1px solid #e5eaf0;
            box-shadow: 0 4px 20px rgba(15,23,42,.05);
        }

        .nav-item:hover {
            transform: translateY(-2px);
        }

        .soft-card {
            background: #ffffff;
            border: 1px solid #e5eaf0;
            box-shadow: 0 8px 28px rgba(15,23,42,.055);
        }

        .post-card {
            transition:
                transform .18s ease,
                box-shadow .18s ease;
        }

        .post-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 35px rgba(15,23,42,.09);
        }

        .activity-item {
            transition: all .18s ease;
        }

        .activity-item:hover {
            transform: translateX(3px);
            background: #f3f6fa;
        }
    </style>
    ''')

    with ui.header().classes(
        'topbar w-full h-[82px] px-6 md:px-10 items-center sticky top-0 z-50'
    ):

        with ui.row().classes(
            'items-center gap-3 w-[250px] shrink-0'
        ):
            with ui.element('div').classes(
                'w-11 h-11 rounded-2xl '
                'bg-gradient-to-br from-blue-600 to-indigo-600 '
                'flex items-center justify-center shadow-lg'
            ):
                ui.icon('hub').classes(
                    'text-white text-[25px]'
                )

            with ui.column().classes('gap-0'):
                ui.label('Red Social').classes(
                    'text-[15px] font-extrabold text-gray-900'
                )

                ui.label('UNAL').classes(
                    'text-[10px] font-bold tracking-[3px] text-blue-600'
                )

        with ui.row().classes(
            'items-center gap-2 ml-auto mr-3 shrink-0'
        ):
            top_button(
                'home_rounded',
                'Inicio',
                '/feed',
                True
            )

            top_button(
                'group_rounded',
                'Amigos',
                '/friends'
            )

            top_button(
                'person_rounded',
                'Perfil',
                f'/profile/{current_user_id}'
            )

            top_button(
                'chat_bubble_rounded',
                'Chat',
                '/chat'
            )

            top_button(
                'notifications_rounded',
                'Avisos',
                '/notifications'
            )

            top_button(
                'settings_rounded',
                'Ajustes',
                '/settings'
            )

        with ui.row().classes(
            'items-center gap-1 shrink-0'
        ):
            ui.button(
                icon='dark_mode'
            ).props(
                'flat round'
            ).classes(
                'text-blue-600'
            ).tooltip(
                'Modo oscuro'
            )

            ui.button(
                icon='logout',
                on_click=lambda: ui.navigate.to('/')
            ).props(
                'flat round'
            ).classes(
                'text-blue-600'
            ).tooltip(
                'Cerrar sesión'
            )

    with ui.row().classes(
        'w-full max-w-[1280px] mx-auto px-4 md:px-6 py-7 items-start gap-6'
    ):

        with ui.column().classes(
            'w-[285px] shrink-0 gap-4'
        ):

            with ui.card().classes(
                'soft-card w-full rounded-2xl p-6'
            ):
                with ui.column().classes(
                    'items-center w-full'
                ):
                    avatar(
                        profile_picture,
                        user_name,
                        'w-20 h-20'
                    )

                    ui.label(
                        user_name
                    ).classes(
                        'mt-4 text-base font-extrabold text-gray-900 text-center'
                    )

                    ui.label(
                        'Comunidad UNAL'
                    ).classes(
                        'text-xs text-gray-500 mt-1'
                    )

                ui.separator().classes('my-6')

                ui.label(
                    'Tu actividad'
                ).classes(
                    'text-sm font-extrabold text-gray-900'
                )

                with ui.column().classes(
                    'w-full mt-3 gap-1'
                ):
                    activity_item(
                        'article',
                        'Mis publicaciones'
                    )

                    activity_item(
                        'photo_library',
                        'Mis fotos'
                    )

                    activity_item(
                        'bookmark',
                        'Guardados'
                    )

                ui.separator().classes('my-5')

                ui.button(
                    'Ver mi perfil',
                    icon='person',
                    on_click=lambda: ui.navigate.to(
                        f'/profile/{current_user_id}'
                    )
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'w-full rounded-xl bg-gray-100 text-gray-700 font-bold'
                )

            with ui.card().classes(
                'soft-card w-full rounded-2xl p-6'
            ):
                with ui.row().classes(
                    'items-center gap-3'
                ):
                    with ui.element('div').classes(
                        'w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center'
                    ):
                        ui.icon(
                            'auto_awesome'
                        ).classes(
                            'text-blue-600 text-[21px]'
                        )

                    ui.label(
                        'Tu espacio'
                    ).classes(
                        'text-sm font-extrabold text-gray-900'
                    )

                ui.label(
                    'Comparte momentos, fotos e ideas con tu comunidad.'
                ).classes(
                    'text-xs text-gray-500 mt-3 leading-5'
                )

                ui.button(
                    'Crear publicación',
                    icon='add',
                    on_click=lambda: new_post_text.set_focus()
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'w-full mt-5 rounded-xl bg-blue-600 text-white font-bold'
                )

        with ui.column().classes(
            'w-full max-w-[680px] mx-auto gap-5'
        ):

            with ui.card().classes(
                'soft-card w-full rounded-2xl p-5'
            ):
                with ui.row().classes(
                    'w-full items-center gap-3'
                ):
                    avatar(
                        profile_picture,
                        user_name
                    )

                    new_post_text = ui.input(
                        placeholder='¿Qué está pasando en la UNAL?'
                    ).props(
                        'borderless dense'
                    ).classes(
                        'flex-1 bg-gray-100 rounded-full px-4'
                    )

                preview_container = ui.column().classes(
                    'w-full mt-3 hidden'
                )

                uploaded_image = {
                    'url': None
                }

                async def handle_upload(e):
                    file_bytes = await e.file.read()

                    res = await api_post(
                        '/users/upload',
                        files={
                            'file': (
                                e.file.name,
                                file_bytes,
                                e.file.content_type
                            )
                        }
                    )

                    if res.status_code == 200:
                        uploaded_image['url'] = (
                            res.json()['image_url']
                        )

                        preview_container.clear()

                        preview_container.classes(
                            remove='hidden'
                        )

                        with preview_container:
                            ui.image(
                                media(
                                    uploaded_image['url']
                                )
                            ).classes(
                                'w-full max-h-72 object-cover rounded-xl'
                            )

                        ui.notify(
                            'Imagen lista para publicar',
                            color='positive'
                        )

                with ui.row().classes(
                    'w-full items-center justify-between mt-4 pt-4 border-t border-gray-100'
                ):
                    uploader = ui.upload(
                        on_upload=handle_upload,
                        auto_upload=True
                    ).props(
                        'accept=".jpg,.png,.jpeg"'
                    ).classes(
                        'hidden'
                    )

                    ui.button(
                        'Foto',
                        icon='add_photo_alternate',
                        on_click=lambda:
                        uploader.run_method('pickFiles')
                    ).props(
                        'flat no-caps'
                    ).classes(
                        'text-blue-600 font-bold'
                    )

                    async def publish():
                        if (
                            not new_post_text.value
                            and not uploaded_image['url']
                        ):
                            ui.notify(
                                'Escribe algo o sube una imagen',
                                color='warning'
                            )
                            return

                        res = await api_post(
                            '/users/posts',
                            json={
                                'author_id': current_user_id,
                                'author_name': user_email,
                                'content': new_post_text.value or '',
                                'image_url': uploaded_image['url']
                            }
                        )

                        if res.status_code == 200:
                            ui.navigate.to('/feed')

                    ui.button(
                        'Publicar',
                        icon='send',
                        on_click=publish
                    ).props(
                        'unelevated no-caps'
                    ).classes(
                        'rounded-full px-5 bg-blue-600 text-white font-bold'
                    )

            with ui.row().classes(
                'w-full items-center justify-between px-1'
            ):
                with ui.column().classes(
                    'gap-0'
                ):
                    ui.label(
                        'Inicio'
                    ).classes(
                        'text-2xl font-extrabold text-gray-900'
                    )

                    ui.label(
                        'Lo último de tu comunidad'
                    ).classes(
                        'text-sm text-gray-500'
                    )

                filter_switch = ui.switch(
                    'Solo amigos'
                ).props(
                    'color=primary'
                )

            posts_container = ui.column().classes(
                'w-full gap-5'
            )

            async def handle_reaction(
                post_id,
                reaction_type
            ):
                await api_post(
                    f'/users/posts/{post_id}/react'
                    f'?user_id={current_user_id}',
                    json={
                        'reaction_type': reaction_type
                    }
                )

                await load_posts()

            async def load_posts():
                posts_container.clear()

                res = await api_get(
                    '/users/posts',
                    params={
                        'user_id': current_user_id,
                        'only_friends': filter_switch.value
                    }
                )

                if res.status_code != 200:
                    ui.notify(
                        'No fue posible cargar las publicaciones',
                        color='negative'
                    )
                    return

                posts = res.json()

                if not posts:
                    with posts_container:
                        ui.label(
                            'No hay publicaciones para mostrar.'
                        ).classes(
                            'text-gray-500 text-center py-12 w-full'
                        )

                    return

                profile_results = await asyncio.gather(
                    *[
                        api_get(
                            f"/users/profiles/{post['author_id']}"
                        )
                        for post in posts
                    ]
                )

                profiles = {
                    post['author_id']: result.json()
                    for post, result in zip(
                        posts,
                        profile_results
                    )
                    if result.status_code == 200
                }

                with posts_container:
                    for post in posts:
                        author = profiles.get(
                            post['author_id'],
                            {}
                        )

                        author_name = (
                            author.get('full_name')
                            or author.get('name')
                            or post['author_name']
                        )

                        author_picture = author.get(
                            'profile_picture_url'
                        )

                        with ui.card().classes(
                            'post-card soft-card w-full rounded-2xl p-0 overflow-hidden'
                        ):
                            with ui.row().classes(
                                'w-full items-center px-5 py-4'
                            ):
                                avatar(
                                    author_picture,
                                    author_name
                                )

                                with ui.column().classes(
                                    'flex-1 gap-0 ml-3'
                                ):
                                    ui.link(
                                        author_name,
                                        f"/profile/{post['author_id']}"
                                    ).classes(
                                        'font-bold text-sm text-gray-900 no-underline hover:underline'
                                    )

                                    ui.label(
                                        post['created_at'][:16].replace(
                                            'T',
                                            ' '
                                        )
                                    ).classes(
                                        'text-xs text-gray-500'
                                    )

                                if (
                                    post['author_id']
                                    == current_user_id
                                ):

                                    async def delete_post(
                                        p_id=post['id']
                                    ):
                                        async with (
                                            httpx.AsyncClient()
                                        ) as client:
                                            await client.delete(
                                                f"http://gateway:8000/"
                                                f"users/posts/{p_id}"
                                                f"?user_id={current_user_id}",
                                                headers={
                                                    'Authorization':
                                                    f"Bearer {app.storage.user['token']}"
                                                }
                                            )

                                        ui.notify(
                                            'Publicación eliminada',
                                            color='warning'
                                        )

                                        await load_posts()

                                    ui.button(
                                        icon='delete',
                                        on_click=delete_post
                                    ).props(
                                        'flat round color=red'
                                    )

                            if post.get('content'):
                                ui.label(
                                    post['content']
                                ).classes(
                                    'px-5 pb-4 text-sm text-gray-800 whitespace-pre-wrap'
                                )

                            if post.get('image_url'):
                                ui.image(
                                    media(post['image_url'])
                                ).classes(
                                    'w-full max-h-[620px] object-cover'
                                )

                            with ui.row().classes(
                                'w-full px-4 py-3 border-t border-gray-100 items-center justify-between'
                            ):
                                with ui.row().classes(
                                    'gap-1'
                                ):
                                    like_color = (
                                        'red'
                                        if post['user_reaction'] == 'like'
                                        else 'gray'
                                    )

                                    ui.button(
                                        f"{post['likes_count']}",
                                        icon='favorite',
                                        on_click=lambda p=post:
                                        handle_reaction(
                                            p['id'],
                                            'like'
                                        )
                                    ).props(
                                        f'flat round color={like_color} no-caps'
                                    )

                                    dislike_color = (
                                        'blue'
                                        if post['user_reaction'] == 'dislike'
                                        else 'gray'
                                    )

                                    ui.button(
                                        f"{post['dislikes_count']}",
                                        icon='thumb_down',
                                        on_click=lambda p=post:
                                        handle_reaction(
                                            p['id'],
                                            'dislike'
                                        )
                                    ).props(
                                        f'flat round color={dislike_color} no-caps'
                                    )

                                    async def go_to_post(
                                        p_id=post['id']
                                    ):
                                        ui.navigate.to(
                                            f'/post/{p_id}'
                                        )

                                    ui.button(
                                        f"{post.get('comments_count', 0)}",
                                        icon='chat_bubble_outline',
                                        on_click=go_to_post
                                    ).props(
                                        'flat round color=gray no-caps'
                                    )

                                async def copy_link(
                                    p_id=post['id']
                                ):
                                    ui.clipboard.write(
                                        f"http://localhost:3000/feed#post-{p_id}"
                                    )

                                    ui.notify(
                                        '¡Enlace copiado!',
                                        color='positive'
                                    )

                                ui.button(
                                    'Compartir',
                                    icon='share',
                                    on_click=copy_link
                                ).props(
                                    'flat round color=gray no-caps'
                                )

            filter_switch.on_value_change(
                lambda e:
                asyncio.create_task(load_posts())
            )

            await load_posts()

        with ui.column().classes(
            'w-[250px] shrink-0 gap-4'
        ):

            with ui.card().classes(
                'soft-card w-full rounded-2xl p-5'
            ):
                with ui.row().classes(
                    'items-center gap-3'
                ):
                    with ui.element('div').classes(
                        'w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center'
                    ):
                        ui.icon(
                            'groups'
                        ).classes(
                            'text-blue-600 text-[22px]'
                        )

                    ui.label(
                        'Comunidad UNAL'
                    ).classes(
                        'text-sm font-extrabold text-gray-900'
                    )

                ui.label(
                    'Un espacio para conectar, compartir y descubrir.'
                ).classes(
                    'text-xs text-gray-500 mt-3 leading-5'
                )

                ui.separator().classes(
                    'my-4'
                )

                with ui.column().classes(
                    'gap-3'
                ):
                    with ui.row().classes(
                        'items-center gap-3'
                    ):
                        ui.icon(
                            'groups'
                        ).classes(
                            'text-blue-600 text-[21px]'
                        )

                        ui.label(
                            'Personas de la comunidad'
                        ).classes(
                            'text-sm font-semibold text-gray-700'
                        )

                    with ui.row().classes(
                        'items-center gap-3'
                    ):
                        ui.icon(
                            'photo_library'
                        ).classes(
                            'text-purple-600 text-[21px]'
                        )

                        ui.label(
                            'Momentos y fotografías'
                        ).classes(
                            'text-sm font-semibold text-gray-700'
                        )

                    with ui.row().classes(
                        'items-center gap-3'
                    ):
                        ui.icon(
                            'forum'
                        ).classes(
                            'text-green-600 text-[21px]'
                        )

                        ui.label(
                            'Conversaciones'
                        ).classes(
                            'text-sm font-semibold text-gray-700'
                        )

            with ui.card().classes(
                'soft-card w-full rounded-2xl p-5'
            ):
                ui.label(
                    'Accesos rápidos'
                ).classes(
                    'text-sm font-extrabold text-gray-900'
                )

                with ui.column().classes(
                    'mt-3 gap-1'
                ):
                    with ui.row().classes(
                        'items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-gray-100'
                    ):
                        ui.icon(
                            'help_outline'
                        ).classes(
                            'text-gray-500 text-[20px]'
                        )

                        ui.label(
                            'Ayuda y soporte'
                        ).classes(
                            'text-sm font-semibold text-gray-700'
                        )

                    with ui.row().classes(
                        'items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-gray-100'
                    ):
                        ui.icon(
                            'security'
                        ).classes(
                            'text-gray-500 text-[20px]'
                        )

                        ui.label(
                            'Privacidad'
                        ).classes(
                            'text-sm font-semibold text-gray-700'
                        )