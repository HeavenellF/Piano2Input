KEY_LAYOUT = "Z1X2CV3B4N5MA6S7DF8G9H0JQIWOERPT[Y]U"
START_NOTE = 48


def build_note_mapping():
    return {
        START_NOTE + i: key.lower()
        for i, key in enumerate(KEY_LAYOUT)
    }