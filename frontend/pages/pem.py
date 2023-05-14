import requests
import flet as ft


def pem(page):
    page.add(ft.Text('encrypted_private_key'))
    page.add(ft.Text(page.session.get('encrypted_private_key')))
    page.add(ft.Text("pem_public_key"))
    page.add(ft.Text(page.session.get('public_key')))
