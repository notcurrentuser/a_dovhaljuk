import requests
import flet as ft


def page_manager(page_func):
    def inner(*args, **kwargs):
        page, _ = args

        page.clean()

        page.add(ft.ResponsiveRow(
            [
                ft.ElevatedButton("Home", on_click=lambda _: home_page(page, _), col={"md": 4}),
                ft.ElevatedButton("Registration", on_click=lambda _: get_pem_page(page, _), col={"md": 4}),
            ],
            run_spacing={"xs": 10}
        ))
        page_func(*args, **kwargs)

    return inner


@page_manager
def pem_page(page, password):
    pem = requests.post('http://localhost:5465/private_key/generation/', {'password_phrase': password}).json()
    encrypted_private_key = pem['encrypted_pem_private_key']
    public_key = pem['pem_public_key']
    page.add(ft.Text('encrypted_private_key'))
    page.add(ft.Text(encrypted_private_key))
    page.add(ft.Text("pem_public_key"))
    page.add(ft.Text(public_key))


@page_manager
def get_pem_page(page, _):
    password_field = ft.TextField(label="Your password")

    def check_password(e):
        if not password_field.value:
            password_field.error_text = "Please enter your password"
            page.update()
        else:
            pem_page(page, password_field)

    page.add(password_field, ft.ElevatedButton("Generation keys", on_click=check_password))


@page_manager
def home_page(page, _):
    pass
    # page.clean()
    # page.add(ft.ElevatedButton("Registration", on_click=lambda _: get_pem_page(page, 'None')))


def start_up(page):
    home_page(page, None)


ft.app(target=start_up)
