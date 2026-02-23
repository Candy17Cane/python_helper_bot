from handlers.content import parse_cb

def test_parse_v1():
    action, ver, section, topic = parse_cb("topic:v1:oop:class")
    assert action == "topic"
    assert section == "oop"
    assert topic == "class"

def test_parse_legacy():
    action, ver, section, topic = parse_cb("topic:oop:class")
    assert section == "oop"
    assert topic == "class"

