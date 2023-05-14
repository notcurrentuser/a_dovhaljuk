import flet as ft
import requests


def get_message(page, message_key):
    message = requests.get(f'http://localhost:5465/message/get/?hash_id={message_key}').json()
    page.add(ft.Text(message['datetime']), ft.Text(message['message']), ft.Text(message['message_description']))