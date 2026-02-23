from services.render_service import render_topic_html

def test_render_escapes_html():
    s = render_topic_html("t", "<b>x</b>")
    assert "&lt;b&gt;" in s 