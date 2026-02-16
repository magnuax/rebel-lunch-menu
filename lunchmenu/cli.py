from lunchmenu.parse import menu_of_the_day, menu_of_the_week
import datetime
import sys

def arg_parser():
    
    parsed = {}
    parsed["weekly"] = False
    parsed["today"] = False
    parsed["weekday"] = None

    help_message = "Usage: python3 -m lunchmenu.cli [--weekly] [--today] [--weekday=<day>]"

    if len(sys.argv) > 1:
        for argument in sys.argv[1:]:
            
            if argument == "--weekly":
                parsed["weekly"] = True
                
            elif argument == "--today":
                parsed["today"] = True
                
            elif argument.startswith("--weekday="):
                parsed["weekday"] = argument.split("=")[1]

            elif argument == "--help":
                print(help_message)
                sys.exit(0)
    else:
        print(help_message)
        sys.exit(0)
    
    return parsed

def main():
    parser = arg_parser()
    
    if parser["weekly"]:
        print(menu_of_the_week())
        
    elif parser["today"]:
        today = datetime.date.today()
        weekday = today.strftime("%A").lower()
        print(menu_of_the_day(weekday))
    
    elif parser["weekday"]:
        weekday = parser["weekday"].lower()
        print(menu_of_the_day(weekday))
        
    return 0

if __name__ == "__main__":
    raise SystemExit(main())