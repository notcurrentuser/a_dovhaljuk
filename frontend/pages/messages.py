import requests
import flet as ft


def messages(page, redirect, edit_page):
    def get_message(e):
        redirect(page, e.control.key)

    def edit_message(e):
        print(e.control.key)
        edit_page(page, e.control.key)

    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    try:
        last_messages = requests.get('http://localhost:5465/message/get/?last=10').json()

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
                                [
                                    ft.TextButton("Edit", on_click=edit_message, key=message_key),
                                    ft.TextButton("Delete"),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    ),
                    width=400,
                    padding=10,
                )
            ))

        page.add(lv)

    except (ConnectionError, requests.JSONDecodeError):
        page.add(ft.Text('Connection error'))
