import sys

def arg_parser():
    
    parsed = {}
    
    parsed["full"] = False
    parsed["today"] = False
    parsed["weekday"] = None

    if len(sys.argv) > 1:
        for argument in sys.argv[1:]:
            
            if argument == "--full":
                parsed["full"] = True
                
            elif argument == "--today":
                parsed["today"] = True
                
            elif argument.startswith("--weekday="):
                parsed["weekday"] = argument.split("=")[1]

            elif argument == "--help":
                print("Usage: menu.py [--full] [--today] [--weekday=<day>]")
                sys.exit(0)
    
    return parsed

def style(text, style):
    if not sys.stdout.isatty():
        return text
    
    if style == "bold":
        return f"\033[1m{text}\033[0m"
    
    if style == "italic":
        return f"\033[3m{text}\033[0m"
    
    return text
