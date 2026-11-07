import asyncio
from nicegui import ui, app
from core.api import api_get, api_post
from core.theme import apply_theme

API = "http://localhost:8000"


def url(path):
    return f"{API}{path}" if path else None


def initial(name):
    return (name or "U").strip()[0].upper()


def avatar(name, picture=None, size="w-12 h-12", text="text-lg"):
    if picture:
        ui.image(url(picture)).classes(
            f"{size} rounded-full object-cover border-4 border-white "
            f"dark:border-zinc-900 shadow-lg shrink-0"
        )
    else:
        ui.avatar(
            initial(name),
            color="primary",
            text_color="white"
        ).classes(
            f"{size} {text} shrink-0 shadow-lg"
        )


def card(classes=""):
    return ui.card().classes(
        "w-full bg-white dark:bg-zinc-900 "
        "rounded-2xl border border-slate-200 "
        "dark:border-zinc-800 shadow-sm " + classes
    )


def top_button(icon, label, route, active=False):
    color = "#2563eb" if active else "#374151"
    background = "#eff6ff" if active else "transparent"

    with ui.element("div").classes("profile-top-item").style(
        f"""
        width:82px;
        height:68px;
        min-width:82px;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        gap:5px;
        border-radius:22px;
        cursor:pointer;
        background:{background};
        box-sizing:border-box;
        transition:all .22s ease;
        """
    ).on(
        "click",
        lambda: ui.navigate.to(route)
    ):
        ui.icon(icon).style(
            f"""
            font-size:28px;
            line-height:28px;
            color:{color};
            display:block;
            margin:0;
            transition:transform .22s ease, color .22s ease;
            """
        )

        ui.label(label).style(
            f"""
            font-size:11px;
            line-height:14px;
            font-weight:700;
            color:{color};
            display:block;
            margin:0;
            white-space:nowrap;
            transition:color .22s ease;
            """
        )


def profile_nav(active):
    user_id = app.storage.user.get("user_id")

    with ui.element("div").classes(
        "w-full bg-white dark:bg-zinc-950 "
        "border-b border-slate-200 dark:border-zinc-800 "
        "sticky top-0 z-50"
    ):
        with ui.row().classes(
            "w-full items-center px-4 md:px-7 py-2"
        ):
            with ui.row().classes(
                "items-center gap-2 ml-auto mr-3 shrink-0"
            ):
                top_button(
                    "home_rounded",
                    "Inicio",
                    "/feed",
                    active == "home"
                )

                top_button(
                    "group_rounded",
                    "Amigos",
                    "/friends",
                    active == "friends"
                )

                top_button(
                    "person_rounded",
                    "Perfil",
                    f"/profile/{user_id}",
                    active == "profile"
                )

                top_button(
                    "chat_bubble_rounded",
                    "Chat",
                    "/chat",
                    active == "chat"
                )

                top_button(
                    "notifications_rounded",
                    "Avisos",
                    "/notifications",
                    active == "notifications"
                )

                top_button(
                    "settings_rounded",
                    "Ajustes",
                    "/settings",
                    active == "settings"
                )

            with ui.row().classes(
                "items-center gap-2 shrink-0"
            ):
                dark_mode = ui.button(
                    icon="dark_mode"
                ).props(
                    "flat round"
                ).classes(
                    "text-slate-600 dark:text-slate-300"
                )

                dark_mode.on(
                    "click",
                    lambda: ui.dark_mode.toggle()
                )

                ui.button(
                    icon="logout",
                    on_click=lambda: (
                        app.storage.user.clear(),
                        ui.navigate.to("/")
                    )
                ).props(
                    "flat round"
                ).classes(
                    "text-slate-600 dark:text-slate-300"
                )


def add_styles():
    ui.add_head_html("""
    <style>
        body {
            background: #f3f6fa !important;
        }

        .dark body {
            background: #090d12 !important;
        }

        .profile-top-item:hover {
            transform: translateY(-2px);
            background: #f1f5f9 !important;
        }

        .profile-top-item:hover .q-icon {
            transform: translateY(-2px) scale(1.08);
        }

        .dark .profile-top-item:hover {
            background: #172033 !important;
        }

        .profile-sidebar {
            min-height: calc(100vh - 105px);
        }

        .profile-menu {
            color: #64748b !important;
            border-radius: 14px !important;
            min-height: 46px !important;
            margin: 2px 8px !important;
        }

        .profile-menu:hover {
            background: #eef4ff !important;
            color: #2563eb !important;
        }

        .dark .profile-menu {
            color: #94a3b8 !important;
        }

        .dark .profile-menu:hover {
            background: #172338 !important;
            color: #60a5fa !important;
        }

        .profile-active {
            background: #e8f1ff !important;
            color: #2563eb !important;
            font-weight: 800 !important;
        }

        .dark .profile-active {
            background: #172b45 !important;
            color: #60a5fa !important;
        }

        .profile-tab {
            min-height: 55px;
            padding: 0 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #64748b;
            font-size: 13px;
            font-weight: 800;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            white-space: nowrap;
        }

        .profile-tab:hover {
            color: #2563eb;
        }

        .profile-tab-active {
            color: #2563eb !important;
            border-bottom-color: #2563eb !important;
        }

        .dark .profile-tab {
            color: #94a3b8;
        }

        .dark .profile-tab-active {
            color: #60a5fa !important;
            border-bottom-color: #60a5fa !important;
        }

        .profile-cover {
            height: 290px;
            background:
                linear-gradient(
                    135deg,
                    #0f766e 0%,
                    #2563eb 52%,
                    #4f46e5 100%
                );
        }

        .profile-stat {
            min-width: 90px;
        }

        .profile-photo {
            transition: transform .2s ease, box-shadow .2s ease;
        }

        .profile-photo:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(15, 23, 42, .12);
        }

        .profile-info-item {
            transition: background .2s ease;
        }

        .profile-info-item:hover {
            background: #f8fafc;
        }

        .dark .profile-info-item:hover {
            background: #111827;
        }

        @media(max-width: 768px) {
            .profile-top-item {
                width:58px !important;
                min-width:58px !important;
                height:60px !important;
            }

            .profile-top-item .q-icon {
                font-size:24px !important;
            }

            .profile-top-item .q-label {
                font-size:9px !important;
            }

            .profile-cover {
                height:220px;
            }

            .profile-tab {
                padding:0 14px;
                font-size:12px;
            }
        }
    </style>
    """)


def info_row(icon, title, value):
    with ui.row().classes("w-full items-start gap-4 py-4"):
        with ui.element("div").classes(
            "w-11 h-11 rounded-xl bg-blue-50 "
            "dark:bg-blue-950 flex items-center justify-center shrink-0"
        ):
            ui.icon(icon, size="21px").classes("text-primary")

        with ui.column().classes("gap-0 min-w-0"):
            ui.label(title).classes(
                "text-[10px] uppercase tracking-widest "
                "font-extrabold text-slate-400"
            )

            ui.label(
                str(value or "No especificado")
            ).classes(
                "mt-1 text-sm md:text-base font-semibold "
                "text-slate-800 dark:text-slate-200 "
                "leading-6 break-words"
            )


async def upload_image(endpoint, e, success):
    data = await e.file.read()

    response = await api_post(
        "/users/upload",
        files={
            "file": (
                e.file.name,
                data,
                e.file.content_type
            )
        }
    )

    if response.status_code == 200:
        image_url = response.json()["image_url"]

        await api_post(
            endpoint + image_url
        )

        ui.notify(
            success,
            color="positive"
        )

        ui.navigate.to("/myprofile")


async def get_posts(user_id):
    response = await api_get(
        "/users/posts",
        params={"user_id": user_id}
    )

    if response.status_code != 200:
        return []

    return [
        post
        for post in response.json()
        if post.get("author_id") == user_id
    ]


async def get_friends(user_id):
    response = await api_get(
        f"/friends/list/{user_id}"
    )

    if response.status_code != 200:
        return []

    return response.json()


def profile_header(
    profile,
    current_user_id,
    own,
    friends_count,
    posts_count,
    photos_count,
    reels_count
):
    full_name = profile.get(
        "full_name",
        "Usuario"
    )

    career = profile.get(
        "career",
        "Estudiante UNAL"
    )

    faculty = profile.get(
        "faculty",
        "Universidad Nacional de Colombia"
    )

    bio = profile.get(
        "bio",
        ""
    )

    cover = profile.get(
        "cover_picture_url"
    )

    picture = profile.get(
        "profile_picture_url"
    )

    with card("p-0 overflow-hidden"):
        if cover:
            ui.image(
                url(cover)
            ).classes(
                "w-full profile-cover object-cover"
            )
        else:
            with ui.element("div").classes(
                "w-full profile-cover relative overflow-hidden"
            ):
                with ui.column().classes(
                    "absolute inset-0 items-center justify-center"
                ):
                    ui.icon(
                        "school",
                        size="58px"
                    ).classes(
                        "text-white/70"
                    )

                    ui.label(
                        "Universidad Nacional de Colombia"
                    ).classes(
                        "text-white text-xl md:text-3xl "
                        "font-extrabold tracking-wide"
                    )

                    ui.label(
                        "Conecta · Comparte · Crece"
                    ).classes(
                        "text-white/70 text-sm mt-1"
                    )

        with ui.column().classes(
            "w-full px-5 md:px-9 pb-6"
        ):
            with ui.row().classes(
                "w-full items-end gap-5 "
                "-mt-16 md:-mt-20 relative"
            ):
                avatar(
                    full_name,
                    picture,
                    "w-32 h-32 md:w-40 md:h-40",
                    "text-5xl"
                )

                with ui.column().classes(
                    "flex-1 min-w-0 pb-2 gap-1"
                ):
                    with ui.row().classes(
                        "items-center gap-2 flex-wrap"
                    ):
                        ui.label(
                            full_name
                        ).classes(
                            "text-2xl md:text-4xl "
                            "font-extrabold text-slate-900 "
                            "dark:text-white"
                        )

                        with ui.element("div").classes(
                            "w-5 h-5 rounded-full bg-primary "
                            "flex items-center justify-center"
                        ):
                            ui.icon(
                                "check",
                                size="13px"
                            ).classes(
                                "text-white"
                            )

                    ui.label(
                        career
                    ).classes(
                        "text-sm md:text-base "
                        "font-bold text-primary"
                    )

                    with ui.row().classes(
                        "items-center gap-2"
                    ):
                        ui.icon(
                            "school",
                            size="16px"
                        ).classes(
                            "text-slate-400"
                        )

                        ui.label(
                            faculty
                        ).classes(
                            "text-xs md:text-sm "
                            "text-slate-500 "
                            "dark:text-slate-400"
                        )

                if own:
                    with ui.row().classes(
                        "gap-2 pb-2"
                    ):
                        async def cover_upload(e):
                            await upload_image(
                                f"/users/profiles/"
                                f"{current_user_id}/cover"
                                f"?image_url=",
                                e,
                                "Portada actualizada"
                            )

                        cover_picker = ui.upload(
                            on_upload=cover_upload,
                            auto_upload=True
                        ).classes("hidden")

                        ui.button(
                            "Portada",
                            icon="photo_camera",
                            on_click=lambda:
                                cover_picker.run_method(
                                    "pickFiles"
                                )
                        ).props(
                            "unelevated rounded "
                            "color=primary no-caps"
                        )

                        async def profile_upload(e):
                            await upload_image(
                                f"/users/profiles/"
                                f"{current_user_id}/picture"
                                f"?image_url=",
                                e,
                                "Foto actualizada"
                            )

                        profile_picker = ui.upload(
                            on_upload=profile_upload,
                            auto_upload=True
                        ).classes("hidden")

                        ui.button(
                            "Foto",
                            icon="account_circle",
                            on_click=lambda:
                                profile_picker.run_method(
                                    "pickFiles"
                                )
                        ).props(
                            "outline rounded "
                            "color=primary no-caps"
                        )

                elif current_user_id != profile.get("id"):
                    ui.button(
                        "Enviar mensaje",
                        icon="chat"
                    ).props(
                        "unelevated rounded "
                        "color=primary no-caps"
                    )

            if bio:
                with ui.row().classes(
                    "items-start gap-2 mt-4 max-w-3xl"
                ):
                    ui.icon(
                        "format_quote",
                        size="20px"
                    ).classes(
                        "text-primary"
                    )

                    ui.label(
                        bio
                    ).classes(
                        "text-sm text-slate-600 "
                        "dark:text-slate-300 "
                        "leading-6"
                    )

            with ui.row().classes(
                "w-full gap-8 mt-5 flex-wrap"
            ):
                stats = [
                    (posts_count, "Publicaciones"),
                    (friends_count, "Amigos"),
                    (photos_count, "Fotos"),
                    (reels_count, "Reels")
                ]

                for value, label in stats:
                    with ui.column().classes(
                        "profile-stat gap-0"
                    ):
                        ui.label(
                            str(value)
                        ).classes(
                            "text-xl font-extrabold "
                            "text-slate-900 "
                            "dark:text-white"
                        )

                        ui.label(
                            label
                        ).classes(
                            "text-xs font-medium "
                            "text-slate-400"
                        )


def sidebar(active):
    with ui.column().classes(
        "profile-sidebar hidden lg:flex "
        "w-64 shrink-0 bg-white dark:bg-zinc-900 "
        "rounded-2xl border border-slate-200 "
        "dark:border-zinc-800 shadow-sm "
        "sticky top-20 overflow-hidden"
    ):
        ui.label(
            "MENÚ"
        ).classes(
            "px-5 pt-5 pb-2 text-[10px] "
            "tracking-widest font-extrabold "
            "text-slate-400"
        )

        items = [
            ("home", "Inicio", "home"),
            ("people", "Amigos", "friends"),
            ("movie", "Videos", "videos"),
            ("bookmark", "Guardados", "saved"),
            ("edit_square", "Crear", "create"),
            ("account_circle", "Mi perfil", "profile")
        ]

        buttons = {}

        for icon, label, key in items:
            button = ui.button(
                label,
                icon=icon
            ).props(
                "flat no-caps align=left"
            ).classes(
                "profile-menu w-full"
            )

            if key == active:
                button.classes(
                    add="profile-active"
                )

            buttons[key] = button

        ui.label(
            "CUENTA"
        ).classes(
            "px-5 pt-5 pb-2 text-[10px] "
            "tracking-widest font-extrabold "
            "text-slate-400"
        )

        ui.button(
            "Ajustes",
            icon="settings"
        ).props(
            "flat no-caps align=left"
        ).classes(
            "profile-menu w-full"
        )

        ui.button(
            "Cerrar sesión",
            icon="logout",
            on_click=lambda: (
                app.storage.user.clear(),
                ui.navigate.to("/")
            )
        ).props(
            "flat no-caps align=left"
        ).classes(
            "profile-menu w-full mb-5"
        )


def tabs(active):
    result = {}

    with ui.row().classes(
        "w-full mt-4 bg-white dark:bg-zinc-900 "
        "rounded-2xl border border-slate-200 "
        "dark:border-zinc-800 shadow-sm px-2 "
        "overflow-x-auto"
    ):
        for key, label in [
            ("home", "Inicio"),
            ("info", "Información"),
            ("friends", "Amigos"),
            ("photos", "Fotos"),
            ("reels", "Reels")
        ]:
            button = ui.label(
                label
            ).classes(
                "profile-tab"
                + (
                    " profile-tab-active"
                    if key == active
                    else ""
                )
            )

            result[key] = button

    return result


async def render_information(container, profile):
    container.clear()

    with container:
        with ui.row().classes(
            "w-full gap-5 items-start"
        ):
            with ui.column().classes(
                "w-full lg:w-1/3"
            ):
                with card("p-3"):
                    ui.label(
                        "Información"
                    ).classes(
                        "text-xl font-extrabold "
                        "px-3 py-2 text-slate-900 "
                        "dark:text-white"
                    )

                    items = [
                        ("personal", "Datos personales", "person"),
                        ("education", "Formación académica", "school"),
                        ("interests", "Intereses", "favorite"),
                        ("travel", "Viajes", "flight_takeoff")
                    ]

                    active = {
                        "value": "personal"
                    }

                    panel = ui.column().classes(
                        "w-full"
                    )

                    buttons = {}

                    async def select(key):
                        active["value"] = key

                        for k, b in buttons.items():
                            if k == key:
                                b.classes(
                                    add="profile-active"
                                )
                            else:
                                b.classes(
                                    remove="profile-active"
                                )

                        await render_panel()

                    for key, label, icon in items:
                        b = ui.button(
                            label,
                            icon=icon,
                            on_click=lambda k=key:
                                asyncio.create_task(
                                    select(k)
                                )
                        ).props(
                            "flat no-caps align=left"
                        ).classes(
                            "profile-menu w-full"
                        )

                        if key == "personal":
                            b.classes(
                                add="profile-active"
                            )

                        buttons[key] = b

            with ui.column().classes(
                "w-full lg:w-2/3"
            ):
                panel = ui.column().classes(
                    "w-full"
                )

                async def render_panel():
                    panel.clear()

                    with panel:
                        with card("p-6 md:p-8"):
                            key = active["value"]

                            if key == "personal":
                                with ui.row().classes(
                                    "items-center gap-4 mb-5"
                                ):
                                    with ui.element("div").classes(
                                        "w-12 h-12 rounded-2xl "
                                        "bg-blue-50 dark:bg-blue-950 "
                                        "flex items-center justify-center"
                                    ):
                                        ui.icon(
                                            "person",
                                            size="25px"
                                        ).classes(
                                            "text-primary"
                                        )

                                    with ui.column().classes(
                                        "gap-0"
                                    ):
                                        ui.label(
                                            "Datos personales"
                                        ).classes(
                                            "text-2xl font-extrabold "
                                            "text-slate-900 "
                                            "dark:text-white"
                                        )

                                        ui.label(
                                            "Información básica de tu perfil"
                                        ).classes(
                                            "text-sm text-slate-400"
                                        )

                                info_row(
                                    "person_outline",
                                    "Nombre completo",
                                    profile.get("full_name")
                                )

                                ui.separator()

                                info_row(
                                    "school",
                                    "Carrera",
                                    profile.get("career")
                                )

                                ui.separator()

                                info_row(
                                    "account_balance",
                                    "Facultad",
                                    profile.get("faculty")
                                )

                                ui.separator()

                                info_row(
                                    "notes",
                                    "Biografía",
                                    profile.get(
                                        "bio",
                                        "Sin biografía"
                                    )
                                )

                            elif key == "education":
                                with ui.row().classes(
                                    "items-center gap-4 mb-5"
                                ):
                                    with ui.element("div").classes(
                                        "w-12 h-12 rounded-2xl "
                                        "bg-blue-50 dark:bg-blue-950 "
                                        "flex items-center justify-center"
                                    ):
                                        ui.icon(
                                            "school",
                                            size="25px"
                                        ).classes(
                                            "text-primary"
                                        )

                                    with ui.column().classes(
                                        "gap-0"
                                    ):
                                        ui.label(
                                            "Formación académica"
                                        ).classes(
                                            "text-2xl font-extrabold "
                                            "text-slate-900 "
                                            "dark:text-white"
                                        )

                                        ui.label(
                                            "Tu información universitaria"
                                        ).classes(
                                            "text-sm text-slate-400"
                                        )

                                info_row(
                                    "account_balance",
                                    "Institución",
                                    "Universidad Nacional de Colombia"
                                )

                                ui.separator()

                                info_row(
                                    "school",
                                    "Carrera",
                                    profile.get("career")
                                )

                                ui.separator()

                                info_row(
                                    "domain",
                                    "Facultad",
                                    profile.get("faculty")
                                )

                            elif key == "interests":
                                with ui.row().classes(
                                    "items-center gap-4 mb-5"
                                ):
                                    with ui.element("div").classes(
                                        "w-12 h-12 rounded-2xl "
                                        "bg-blue-50 dark:bg-blue-950 "
                                        "flex items-center justify-center"
                                    ):
                                        ui.icon(
                                            "favorite",
                                            size="25px"
                                        ).classes(
                                            "text-primary"
                                        )

                                    with ui.column().classes(
                                        "gap-0"
                                    ):
                                        ui.label(
                                            "Intereses"
                                        ).classes(
                                            "text-2xl font-extrabold "
                                            "text-slate-900 "
                                            "dark:text-white"
                                        )

                                        ui.label(
                                            "Lo que te gusta"
                                        ).classes(
                                            "text-sm text-slate-400"
                                        )

                                with ui.row().classes(
                                    "gap-3 flex-wrap mt-5"
                                ):
                                    for item in [
                                        "Tecnología",
                                        "Programación",
                                        "Deportes",
                                        "Universidad"
                                    ]:
                                        ui.label(
                                            item
                                        ).classes(
                                            "px-4 py-2 rounded-full "
                                            "bg-blue-50 dark:bg-blue-950 "
                                            "text-primary font-bold text-sm"
                                        )

                            else:
                                with ui.row().classes(
                                    "items-center gap-4 mb-5"
                                ):
                                    with ui.element("div").classes(
                                        "w-12 h-12 rounded-2xl "
                                        "bg-blue-50 dark:bg-blue-950 "
                                        "flex items-center justify-center"
                                    ):
                                        ui.icon(
                                            "flight_takeoff",
                                            size="25px"
                                        ).classes(
                                            "text-primary"
                                        )

                                    with ui.column().classes(
                                        "gap-0"
                                    ):
                                        ui.label(
                                            "Viajes"
                                        ).classes(
                                            "text-2xl font-extrabold "
                                            "text-slate-900 "
                                            "dark:text-white"
                                        )

                                        ui.label(
                                            "Tus lugares favoritos"
                                        ).classes(
                                            "text-sm text-slate-400"
                                        )

                                with ui.column().classes(
                                    "items-center py-10"
                                ):
                                    ui.icon(
                                        "flight",
                                        size="52px"
                                    ).classes(
                                        "text-slate-300"
                                    )

                                    ui.label(
                                        "Aún no has agregado viajes"
                                    ).classes(
                                        "text-slate-400 mt-3"
                                    )

                await render_panel()


async def render_home(
    container,
    user_id,
    email,
    profile,
    own
):
    container.clear()

    with container:
        with ui.row().classes(
            "w-full gap-5 items-start"
        ):
            with ui.column().classes(
                "w-full lg:w-1/3"
            ):
                with card("p-5"):
                    ui.label(
                        "Sobre mí"
                    ).classes(
                        "text-xl font-extrabold "
                        "text-slate-900 dark:text-white"
                    )

                    ui.label(
                        profile.get(
                            "bio",
                            "Sin biografía aún."
                        )
                    ).classes(
                        "text-sm text-slate-600 "
                        "dark:text-slate-400 "
                        "leading-6 mt-3"
                    )

                    ui.separator().classes("my-5")

                    info_row(
                        "school",
                        "Carrera",
                        profile.get("career")
                    )

                    info_row(
                        "account_balance",
                        "Facultad",
                        profile.get("faculty")
                    )

            with ui.column().classes(
                "w-full lg:w-2/3"
            ):
                if own:
                    with card("p-5 mb-5"):
                        with ui.row().classes(
                            "w-full items-center gap-3"
                        ):
                            avatar(
                                profile.get("full_name"),
                                profile.get(
                                    "profile_picture_url"
                                ),
                                "w-12 h-12"
                            )

                            post_input = ui.input(
                                placeholder="¿Qué estás pensando?"
                            ).props(
                                "outlined rounded"
                            ).classes(
                                "flex-grow"
                            )

                        uploaded = {
                            "url": None
                        }

                        async def upload_post(e):
                            data = await e.file.read()

                            response = await api_post(
                                "/users/upload",
                                files={
                                    "file": (
                                        e.file.name,
                                        data,
                                        e.file.content_type
                                    )
                                }
                            )

                            if response.status_code == 200:
                                uploaded["url"] = (
                                    response.json()["image_url"]
                                )

                                ui.notify(
                                    "Imagen lista para publicar",
                                    color="positive"
                                )

                        async def publish():
                            if (
                                not post_input.value
                                and not uploaded["url"]
                            ):
                                return

                            response = await api_post(
                                "/users/posts",
                                json={
                                    "author_id": user_id,
                                    "author_name": email,
                                    "content": post_input.value or "",
                                    "image_url": uploaded["url"]
                                }
                            )

                            if response.status_code == 200:
                                ui.notify(
                                    "Publicación creada",
                                    color="positive"
                                )

                                ui.navigate.to(
                                    "/myprofile"
                                )

                        uploader = ui.upload(
                            on_upload=upload_post,
                            auto_upload=True
                        ).props(
                            'accept=".jpg,.png,.jpeg"'
                        ).classes("hidden")

                        with ui.row().classes(
                            "w-full justify-between mt-4"
                        ):
                            ui.button(
                                "Foto",
                                icon="photo_camera",
                                on_click=lambda:
                                    uploader.run_method(
                                        "pickFiles"
                                    )
                            ).props(
                                "flat color=primary"
                            )

                            ui.button(
                                "Publicar",
                                icon="send",
                                on_click=publish
                            ).props(
                                "unelevated rounded color=primary"
                            )

                posts = await get_posts(user_id)

                ui.label(
                    "Publicaciones"
                ).classes(
                    "text-xl font-extrabold "
                    "text-slate-900 dark:text-white mb-3"
                )

                if not posts:
                    with card("p-10"):
                        with ui.column().classes(
                            "w-full items-center"
                        ):
                            ui.icon(
                                "post_add",
                                size="48px"
                            ).classes(
                                "text-slate-300"
                            )

                            ui.label(
                                "Aún no tienes publicaciones."
                                if own
                                else "Este usuario no tiene publicaciones."
                            ).classes(
                                "text-slate-400 mt-3"
                            )

                for post in posts:
                    with card(
                        "p-0 overflow-hidden mb-4"
                    ):
                        if post.get("content"):
                            ui.label(
                                post["content"]
                            ).classes(
                                "p-5 text-sm text-slate-800 "
                                "dark:text-slate-200 "
                                "whitespace-pre-wrap leading-6"
                            )

                        if post.get("image_url"):
                            ui.image(
                                url(post["image_url"])
                            ).classes(
                                "w-full max-h-[550px] object-cover"
                            )


async def render_friends(container, user_id):
    container.clear()

    with container:
        with card("p-6"):
            ui.label(
                "Amigos"
            ).classes(
                "text-2xl font-extrabold "
                "text-slate-900 dark:text-white mb-6"
            )

            friends = await get_friends(user_id)

            if not friends:
                with ui.column().classes(
                    "w-full items-center py-12"
                ):
                    ui.icon(
                        "group_off",
                        size="48px"
                    ).classes(
                        "text-slate-300"
                    )

                    ui.label(
                        "No tiene amigos aún."
                    ).classes(
                        "text-slate-400 mt-3"
                    )

            with ui.grid(columns=2).classes(
                "w-full gap-4"
            ):
                for friend in friends:
                    with ui.row().classes(
                        "items-center gap-3 p-4 "
                        "rounded-2xl border border-slate-100 "
                        "dark:border-zinc-800 "
                        "hover:bg-slate-50 "
                        "dark:hover:bg-zinc-800 "
                        "cursor-pointer transition"
                    ).on(
                        "click",
                        lambda f=friend:
                        ui.navigate.to(
                            f'/profile/{f["id"]}'
                        )
                    ):
                        avatar(
                            friend.get("full_name"),
                            friend.get(
                                "profile_picture_url"
                            ),
                            "w-12 h-12"
                        )

                        ui.label(
                            friend.get("full_name")
                        ).classes(
                            "font-bold text-slate-700 "
                            "dark:text-slate-200"
                        )


async def render_photos(container, user_id, own):
    container.clear()

    with container:
        with card("p-6"):
            with ui.row().classes(
                "w-full justify-between "
                "items-center mb-6"
            ):
                ui.label(
                    "Fotos"
                ).classes(
                    "text-2xl font-extrabold "
                    "text-slate-900 dark:text-white"
                )

                if own:
                    async def upload_photo(e):
                        data = await e.file.read()

                        response = await api_post(
                            "/users/upload",
                            files={
                                "file": (
                                    e.file.name,
                                    data,
                                    e.file.content_type
                                )
                            }
                        )

                        if response.status_code == 200:
                            await api_post(
                                "/users/posts",
                                json={
                                    "author_id": user_id,
                                    "author_name":
                                        app.storage.user.get(
                                            "email",
                                            "U"
                                        ),
                                    "content": "",
                                    "image_url":
                                        response.json()
                                        ["image_url"]
                                }
                            )

                            ui.notify(
                                "Foto subida correctamente",
                                color="positive"
                            )

                            await render_photos(
                                container,
                                user_id,
                                own
                            )

                    uploader = ui.upload(
                        on_upload=upload_photo,
                        auto_upload=True
                    ).props(
                        'accept="image/*"'
                    ).classes("hidden")

                    ui.button(
                        "Subir foto",
                        icon="add_a_photo",
                        on_click=lambda:
                            uploader.run_method(
                                "pickFiles"
                            )
                    ).props(
                        "unelevated rounded color=primary"
                    )

            posts = await get_posts(user_id)

            photos = [
                p
                for p in posts
                if p.get("image_url")
                and not p.get(
                    "image_url",
                    ""
                ).lower().endswith(
                    (".mp4", ".mov")
                )
            ]

            if not photos:
                with ui.column().classes(
                    "w-full items-center py-12"
                ):
                    ui.icon(
                        "photo_library",
                        size="48px"
                    ).classes(
                        "text-slate-300"
                    )

                    ui.label(
                        "No hay fotos aún."
                    ).classes(
                        "text-slate-400 mt-3"
                    )

            with ui.grid(columns=3).classes(
                "w-full gap-4"
            ):
                for photo in photos:
                    ui.image(
                        url(photo["image_url"])
                    ).classes(
                        "w-full aspect-square "
                        "object-cover rounded-2xl "
                        "profile-photo cursor-pointer"
                    )


async def render_reels(container, user_id, own):
    container.clear()

    with container:
        with card("p-6"):
            with ui.row().classes(
                "w-full justify-between "
                "items-center mb-6"
            ):
                ui.label(
                    "Reels"
                ).classes(
                    "text-2xl font-extrabold "
                    "text-slate-900 dark:text-white"
                )

                if own:
                    async def upload_reel(e):
                        data = await e.file.read()

                        response = await api_post(
                            "/users/upload",
                            files={
                                "file": (
                                    e.file.name,
                                    data,
                                    e.file.content_type
                                )
                            }
                        )

                        if response.status_code == 200:
                            result = response.json()

                            if result.get(
                                "file_type"
                            ) == "video":
                                await api_post(
                                    "/users/posts",
                                    json={
                                        "author_id": user_id,
                                        "author_name":
                                            app.storage.user.get(
                                                "email",
                                                "U"
                                            ),
                                        "content": "",
                                        "image_url":
                                            result["file_url"]
                                    }
                                )

                                ui.notify(
                                    "Reel subido correctamente",
                                    color="positive"
                                )

                                await render_reels(
                                    container,
                                    user_id,
                                    own
                                )

                    uploader = ui.upload(
                        on_upload=upload_reel,
                        auto_upload=True
                    ).props(
                        'accept="video/*"'
                    ).classes("hidden")

                    ui.button(
                        "Subir Reel",
                        icon="movie",
                        on_click=lambda:
                            uploader.run_method(
                                "pickFiles"
                            )
                    ).props(
                        "unelevated rounded color=primary"
                    )

            posts = await get_posts(user_id)

            reels = [
                p
                for p in posts
                if p.get("image_url")
                and p.get(
                    "image_url",
                    ""
                ).lower().endswith(
                    (".mp4", ".mov")
                )
            ]

            if not reels:
                with ui.column().classes(
                    "w-full items-center py-12"
                ):
                    ui.icon(
                        "movie",
                        size="48px"
                    ).classes(
                        "text-slate-300"
                    )

                    ui.label(
                        "No hay Reels aún."
                    ).classes(
                        "text-slate-400 mt-3"
                    )

            with ui.grid(columns=3).classes(
                "w-full gap-4"
            ):
                for reel in reels:
                    ui.video(
                        url(reel["image_url"])
                    ).classes(
                        "w-full aspect-[9/16] "
                        "rounded-2xl shadow-md"
                    )


@ui.page("/myprofile")
async def my_profile():
    apply_theme()
    add_styles()

    if "token" not in app.storage.user:
        ui.navigate.to("/")
        return

    user_id = app.storage.user.get("user_id")
    email = app.storage.user.get("email", "U")

    profile_nav("profile")

    response = await api_get(
        f"/users/profiles/{user_id}"
    )

    profile = (
        response.json()
        if response.status_code == 200
        else {}
    )

    posts = await get_posts(user_id)
    friends = await get_friends(user_id)

    photos = [
        p
        for p in posts
        if p.get("image_url")
        and not p.get(
            "image_url",
            ""
        ).lower().endswith(
            (".mp4", ".mov")
        )
    ]

    reels = [
        p
        for p in posts
        if p.get("image_url")
        and p.get(
            "image_url",
            ""
        ).lower().endswith(
            (".mp4", ".mov")
        )
    ]

    with ui.row().classes(
        "w-full max-w-[1480px] mx-auto "
        "px-3 md:px-5 pb-12 gap-5 items-start"
    ):
        sidebar("profile")

        with ui.column().classes(
            "w-full flex-1 min-w-0"
        ):
            profile_header(
                profile,
                user_id,
                True,
                len(friends),
                len(posts),
                len(photos),
                len(reels)
            )

            tabs_container = tabs("home")
            content = ui.column().classes(
                "w-full mt-5"
            )

            async def change_tab(name):
                for key, element in tabs_container.items():
                    if key == name:
                        element.classes(
                            add="profile-tab-active"
                        )
                    else:
                        element.classes(
                            remove="profile-tab-active"
                        )

                if name == "home":
                    await render_home(
                        content,
                        user_id,
                        email,
                        profile,
                        True
                    )

                elif name == "info":
                    await render_information(
                        content,
                        profile
                    )

                elif name == "friends":
                    await render_friends(
                        content,
                        user_id
                    )

                elif name == "photos":
                    await render_photos(
                        content,
                        user_id,
                        True
                    )

                elif name == "reels":
                    await render_reels(
                        content,
                        user_id,
                        True
                    )

            for key, element in tabs_container.items():
                element.on(
                    "click",
                    lambda k=key:
                    asyncio.create_task(
                        change_tab(k)
                    )
                )

            await render_home(
                content,
                user_id,
                email,
                profile,
                True
            )


@ui.page("/profile/{user_id}")
async def user_profile(user_id: int):
    apply_theme()
    add_styles()

    if "token" not in app.storage.user:
        ui.navigate.to("/")
        return

    current_user_id = app.storage.user.get(
        "user_id"
    )

    profile_nav("profile")

    response = await api_get(
        f"/users/profiles/{user_id}"
    )

    profile = (
        response.json()
        if response.status_code == 200
        else {
            "full_name": f"Usuario {user_id}"
        }
    )

    posts = await get_posts(user_id)
    friends = await get_friends(user_id)

    photos = [
        p
        for p in posts
        if p.get("image_url")
        and not p.get(
            "image_url",
            ""
        ).lower().endswith(
            (".mp4", ".mov")
        )
    ]

    reels = [
        p
        for p in posts
        if p.get("image_url")
        and p.get(
            "image_url",
            ""
        ).lower().endswith(
            (".mp4", ".mov")
        )
    ]

    with ui.row().classes(
        "w-full max-w-[1480px] mx-auto "
        "px-3 md:px-5 pb-12 gap-5 items-start"
    ):
        sidebar("")

        with ui.column().classes(
            "w-full flex-1 min-w-0"
        ):
            profile_header(
                profile,
                current_user_id,
                False,
                len(friends),
                len(posts),
                len(photos),
                len(reels)
            )

            tabs_container = tabs("home")
            content = ui.column().classes(
                "w-full mt-5"
            )

            async def change_tab(name):
                for key, element in tabs_container.items():
                    if key == name:
                        element.classes(
                            add="profile-tab-active"
                        )
                    else:
                        element.classes(
                            remove="profile-tab-active"
                        )

                if name == "home":
                    await render_home(
                        content,
                        user_id,
                        app.storage.user.get(
                            "email",
                            "U"
                        ),
                        profile,
                        False
                    )

                elif name == "info":
                    await render_information(
                        content,
                        profile
                    )

                elif name == "friends":
                    await render_friends(
                        content,
                        user_id
                    )

                elif name == "photos":
                    await render_photos(
                        content,
                        user_id,
                        False
                    )

                elif name == "reels":
                    await render_reels(
                        content,
                        user_id,
                        False
                    )

            for key, element in tabs_container.items():
                element.on(
                    "click",
                    lambda k=key:
                    asyncio.create_task(
                        change_tab(k)
                    )
                )

            await render_home(
                content,
                user_id,
                app.storage.user.get(
                    "email",
                    "U"
                ),
                profile,
                False
            )