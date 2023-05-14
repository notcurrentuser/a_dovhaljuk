import requests
import flet as ft


def pem(page, password):
    try:
        pems = requests.post('http://localhost:5465/private_key/generation/', {'password_phrase': password}).json()
        page.splash = None
        page.update()
        encrypted_private_key = pems['encrypted_pem_private_key']
        public_key = pems['pem_public_key']
        page.add(ft.Text('encrypted_private_key'))
        page.add(ft.Text(encrypted_private_key))
        page.add(ft.Text("pem_public_key"))
        page.add(ft.Text(public_key))
    except requests.exceptions.ConnectionError:
        page.splash = None
        page.update()
        page.add(ft.Text('Connection Error'))
