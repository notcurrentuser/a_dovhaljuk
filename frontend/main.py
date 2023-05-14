import flet as ft

from pages import messages, get_pem, get_message, pem
from addons import window_prevent_close_event


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
    pem(page, password=password)


@page_manager
def get_pem_page(page, _):
    get_pem(page, redirect=pem_page)


@page_manager
def get_message_page(page, message_key):
    get_message(page, message_key=message_key)


@page_manager
def messages_page(page, _):
    messages(page, redirect=get_message_page)


def start_up(page):
    page.title = "HaltStore"
    window_prevent_close_event(page)
    messages_page(page, None)


ft.app(target=start_up)
