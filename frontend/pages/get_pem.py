import flet as ft


def get_pem(page, redirect):
    password_field = ft.TextField(label="Your password")

    def check_password(e):
        if not password_field.value:
            password_field.error_text = "Please enter your password"
            page.update()
        else:
            page.splash = ft.ProgressBar()
            page.update()
            redirect(page, password_field)

    page.add(password_field, ft.ElevatedButton("Generation keys", on_click=check_password))
