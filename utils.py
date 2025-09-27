WIDTH = 50
MARGIN = 5
input_char = ">"

def text_lines(text: list[str], space: str = " ", width: int = WIDTH, margin: int = MARGIN) -> list[str]: 
    max_len = width - margin * 2

    if len(text) <= max_len:
        return ["".join(text)]

    cut = None
    space_len = len(space)

    str = "".join(text[:max_len])
    idx = str.rfind(space) 

    if idx != -1:
        cut = idx

    if cut is not None:
        line = text[:cut]
        rest = text[cut + space_len :]
        return ["".join(line)] + text_lines(rest, space, width, margin)
    else:
        line = text[:max_len - 1] + ["-"]
        rest = text[max_len - 1 :]
        return ["".join(line)] + text_lines(rest, space, width, margin)

def title_style(input, width: int = WIDTH, margin: int = MARGIN) -> list[str]:
    text = "".join(map(lambda str: str + " ", input))
    return "\n".join(map(lambda str: str.center(width, " "), text_lines(text, space="  ")))

def default_text(input, width: int = WIDTH, margin: int = MARGIN) -> str:
    return "\n".join(map(lambda str: str.center(width, " "), text_lines(input)))

def separator(width: int = WIDTH) -> str:
    return "=" * width

def options(*options: str, center: bool = True) -> str:
    for i, option in enumerate(options):
        text = f"{i + 1}. {option}"
        print(text.center(WIDTH, " ") if center else text)
    return input(input_char + " ")