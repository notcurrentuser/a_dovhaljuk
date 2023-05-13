import time

import requests
import flet as ft


def page_manager(page_func):
    def inner(*args, **kwargs):
        page, _ = args

        page.clean()
        page.add(ft.ResponsiveRow(
            [
                ft.ElevatedButton("Home", on_click=lambda _: message_page(page, _), col={"md": 4}),
                ft.ElevatedButton("Registration", on_click=lambda _: get_pem_page(page, _), col={"md": 4}),
            ],
            run_spacing={"xs": 10}
        ))
        page_func(*args, **kwargs)

    return inner


@page_manager
def pem_page(page, password):
    try:
        pem = requests.post('http://localhost:5465/private_key/generation/', {'password_phrase': password}).json()
        page.splash = None
        page.update()
        encrypted_private_key = pem['encrypted_pem_private_key']
        public_key = pem['pem_public_key']
        page.add(ft.Text('encrypted_private_key'))
        page.add(ft.Text(encrypted_private_key))
        page.add(ft.Text("pem_public_key"))
        page.add(ft.Text(public_key))
    except requests.exceptions.ConnectionError:
        page.splash = None
        page.update()
        page.add(ft.Text('Connection Error'))


@page_manager
def get_pem_page(page, _):
    password_field = ft.TextField(label="Your password")

    def check_password(e):
        if not password_field.value:
            password_field.error_text = "Please enter your password"
            page.update()
        else:
            page.splash = ft.ProgressBar()
            page.update()
            pem_page(page, password_field)

    page.add(password_field, ft.ElevatedButton("Generation keys", on_click=check_password)) \



@page_manager
def get_message_page(page, message_key):
    message = requests.get(f'http://localhost:5465/message/get/?hash_id={message_key}').json()
    page.add(ft.Text(message['datetime']), ft.Text(message['message']), ft.Text(message['message_description']))


@page_manager
def message_page(page, _):
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    last_messages = requests.get('http://localhost:5465/message/get/?last=10').json()
    message_key = ''

    def get_message(e):
        get_message_page(page, e.control.key)

    for message_key in last_messages.keys():
        lv.controls.append(ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            key=message_key,
                            leading=ft.Icon(ft.icons.ALBUM),
                            title=ft.Text(last_messages[message_key]['message_description']),
                            subtitle=ft.Text(last_messages[message_key]['message']),
                            on_click=get_message
                        ),
                        ft.Row(
                            [ft.TextButton("Delete"),
                             ft.TextButton("Edit")],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                width=400,
                padding=10,
            )
        ))

    page.add(lv)

    while True:
        last_db_message = requests.get('http://localhost:5465/message/get/?last=1').json()
        last_db_key = list(last_db_message.keys())[0]
        if message_key != last_db_key:
            message_key = last_db_key
            lv.controls.append(ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                key=message_key,
                                leading=ft.Icon(ft.icons.ALBUM),
                                title=ft.Text(last_db_message[message_key]['message_description']),
                                subtitle=ft.Text(last_db_message[message_key]['message']),
                                on_click=get_message
                            ),
                            ft.Row(
                                [ft.TextButton("Delete"),
                                 ft.TextButton("Edit")],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    ),
                    width=400,
                    padding=10,
                )
            ))
        page.update()
        time.sleep(10)


def start_up(page):
    page.title = "HaltStore"

    def window_event(e):
        if e.data == "close":
            page.dialog = confirm_dialog
            confirm_dialog.open = True
            page.update()

    page.window_prevent_close = True
    page.on_window_event = window_event

    def yes_click(_):
        page.window_destroy()

    def no_click(_):
        confirm_dialog.open = False
        page.update()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to exit this app?"),
        actions=[
            ft.ElevatedButton("Yes", on_click=yes_click),
            ft.OutlinedButton("No", on_click=no_click),
        ],
        actions_alignment="end",
    )
    message_page(page, None)


ft.app(target=start_up)
