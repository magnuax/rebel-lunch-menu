from lunchmenu.parse import menu_of_the_day, menu_of_the_week
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


if __name__ == "__main__":
    import datetime

    parser = arg_parser()
    
    if parser["full"]:
        print(menu_of_the_week())
        
    elif parser["today"]:
        today = datetime.date.today()
        weekday = today.strftime("%A").lower()
        print(menu_of_the_day(weekday))
    
    elif parser["weekday"]:
        weekday = parser["weekday"].lower()
        print(menu_of_the_day(weekday))
        