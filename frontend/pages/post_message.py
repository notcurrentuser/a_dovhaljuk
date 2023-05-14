import flet as ft
import requests


def post_message(page, default_message_key=None):
    try:
        print(requests.get(f'http://localhost:5465/message/get/?hash_id={default_message_key}'))
        default_message = requests.get(f'http://localhost:5465/message/get/?hash_id={default_message_key}').json()['message']
    except Exception as e:
        default_message = None
        print(e)
    message_field = ft.TextField(label="Your message", value=default_message)
    password_field = ft.TextField(label="Your password")

    def post(e):
        if not message_field.value:
            message_field.error_text = "Please enter your message"
            page.update()

        if not password_field.value:
            password_field.error_text = "Please enter your password"
            page.update()

        if message_field.value and password_field.value:
            try:
                message_hash = requests.post('http://localhost:5465/message/send/',
                                             data={
                                                 'message': message_field.value,
                                             }).json()['message_hash']

                message_hash_sign = requests.post('http://localhost:5465/private_key/sign/',
                                                  data={
                                                      'password_phrase': password_field.value,
                                                      'data_hash': message_hash,
                                                      'encrypted_pem_private_key': page.session.get(
                                                          'encrypted_private_key'),
                                                  }).json()['signature']

                requests.post('http://localhost:5465/message_hash/send/',
                              data={
                                  'message_hash': message_hash,
                                  'message_hash_hash': message_hash_sign,
                              })

            except ConnectionError:
                ft.Text('Error post message')

    page.add(message_field, password_field, ft.ElevatedButton("Post", on_click=post))
