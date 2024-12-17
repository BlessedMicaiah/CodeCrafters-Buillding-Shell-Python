import sys

def main():
    valid_commands = []
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_command = input()
        if user_command == "exit 0":
            print("$ exit 0")
        elif user_command not in valid_commands:
            print(user_command)
            print(f"{user_command}: command not found")
    sys.exit(0)

# main check
if __name__ == "__main__":
    main()
