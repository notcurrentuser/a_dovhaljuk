from backend.common.text_tags import TextTags

text_tags = TextTags()


def test_stopword_create():
    assert ',' in text_tags._stopword_create()


def test_get_tags():
    result = text_tags.get_tags('''
    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley
     of type and scrambled it to make a type specimen book.
    ''')
    assert result[0][1] == 2
    assert len(result) == 10


def test_type_get_tags():
    assert type(text_tags.get_tags('''
    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley
     of type and scrambled it to make a type specimen book.
    ''')) is list
