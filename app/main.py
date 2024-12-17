import sys

def main():
    valid_commands = []  # List for valid commands
    while True:
        # Print the prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Read and clean user input
        command = input().strip()

        # Exit cleanly if 'exit 0'
        if command == "exit 0":
            sys.exit(0)  # Terminate with exit code 0
        
        # Handle 'echo' command
        if command.startswith("echo "):
            print(command[len("echo "):])  # Print after 'echo '

        # Handle invalid commands
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
