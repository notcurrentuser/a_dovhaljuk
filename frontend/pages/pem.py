import requests
import flet as ft


def pem(page):
    page.add(ft.TextField(label='Private Key', read_only=True, value=page.session.get('encrypted_private_key')))
