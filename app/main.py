import sys

def main():
    valid_builtin_commands = {
        "echo": "echo is a shell builtin",
        "exit": "exit is a shell builtin"
    }

    while True:
        # Print the prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Read and clean user input
        command = input().strip()

        # Exit cleanly if 'exit 0'
        if command == "exit 0":
            sys.exit(0)  # Terminate with exit code 0
        
        # Handle 'type <command>' input
        if command.startswith("type "):
            cmd_name = command[len("type "):]  # Extract command after 'type '
            if cmd_name in valid_builtin_commands:
                print(valid_builtin_commands[cmd_name])  # Print description
            else:
                print(f"{cmd_name}: not found")  # Command not found
        
        # General unrecognized commands
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
