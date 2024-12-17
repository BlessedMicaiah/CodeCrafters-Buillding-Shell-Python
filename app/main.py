import sys

def main():
    valid_commands = []
    while True:
        # Print the prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Read user input
        user_command = input()

        # Echo 'exit 0' and exit cleanly
        if user_command == "exit 0":
            print(user_command)  # Echo the exit command exactly
            sys.exit(0)  # Terminate with exit code 0
        
        # Handle invalid commands
        if user_command not in valid_commands:
            print(user_command)  # Echo the user command
            print(f"{user_command}: command not found")

if __name__ == "__main__":
    main()
