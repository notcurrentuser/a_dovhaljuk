from datetime import datetime

import flet as ft
import requests


def get_message(page, message_key):
    message = requests.get(f'http://localhost:5465/message/get/?hash_id={message_key}').json()
    message_hash = requests.post(f'http://localhost:5465/message_hash/get/', data={
        'hash_id': message_key
    }).json()

    page.add(ft.Text(message['message']))
    page.add(ft.Row([ft.Text('Time Post:'), ft.Text(str(datetime.fromtimestamp(int(message['datetime']))))]))
    page.add(ft.Row([ft.Text('AI Short Description:'), ft.Text(message['message_description'])]))
    page.add(ft.Row([ft.Text('Sign Hash:'), ft.TextField(read_only=True, value=message_hash['message_hash_hash'])]))
