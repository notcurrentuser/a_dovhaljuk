import requests
import flet as ft

from pages import messages, get_pem, get_message, pem


def page_manager(page_func):
    def inner(*args, **kwargs):
        page, _ = args

        page.clean()
        page.add(ft.ResponsiveRow(
            [
                ft.ElevatedButton("Home", on_click=lambda _: messages_page(page, _), col={"md": 4}),
                ft.ElevatedButton("Registration", on_click=lambda _: get_pem_page(page, _), col={"md": 4}),
            ],
            run_spacing={"xs": 10}
        ))
        page_func(*args, **kwargs)

    return inner


@page_manager
def pem_page(page, password):
    pem.pem(page, password=password)


@page_manager
def get_pem_page(page, _):
    get_pem.get_pem(page, redirect=pem_page)


@page_manager
def get_message_page(page, message_key):
    get_message.get_message(page, message_key=message_key)


@page_manager
def messages_page(page, _):
    messages.messages(page, redirect=get_message_page)


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
    messages_page(page, None)


ft.app(target=start_up)
