import sys

def style(text, style):
    if not sys.stdout.isatty():
        return text
    
    if style == "bold":
        return f"\033[1m{text}\033[0m"
    
    if style == "italic":
        return f"\033[3m{text}\033[0m"
    
    return text

def format_menu_entry(raw_text, includes_title=False):
    
    formatted = ""
    filtered = [line for line in raw_text.splitlines() if line.strip() != ""]
    is_not_empty = len(filtered) > 0

    if includes_title and is_not_empty:
        title = filtered.pop(0)
        formatted += "\n-------\n"
        formatted += style(title, "bold")
        formatted += "\n-------\n"

    lines = []
    if len(filtered) > 0:
        lines.append(style(filtered[0], "bold") + "\n")    
    if len(filtered) > 1:
        lines.append(style(filtered[1], "normal") + "\n")
    if len(filtered) > 2:
        lines.append(style(filtered[2], "italic") + "\n")

    formatted += "".join(lines)
    
    return formatted 