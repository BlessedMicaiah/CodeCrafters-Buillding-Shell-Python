import sys

def main():
    valid_commands = [{
        "echo": "echo is a shell builtin",
        "exit": "exit is a shell builtin"
    }]  # List for valid commands
    while True:
        # Print the prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Read and clean user input
        command = input().strip()

        # Exit cleanly if 'exit 0'
        if command == "exit 0":
            sys.exit(0)  # Terminate with exit code 0

        if command.startswith("type "):
            cmd = command[len("type "):]
            if cmd in valid_commands:
                print(valid_commands[cmd])
            else:
                print(f"{cmd}: not found")
        
        # Handle invalid commands
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
