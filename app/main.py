import sys
import os

def main():
    while True:
        # Print the prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Read and clean user input
        command = input().strip()
        if not command:
            continue
        
        # Split the command into parts
        command_array = command.split()
        main_command = command_array[0]

        # Handle 'exit 0'
        if main_command == "exit" and len(command_array) == 2 and command_array[1] == "0":
            sys.exit(0)

        # Handle 'ls' command
        elif main_command == "ls":
            try:
                # Simulate 'ls' by listing current directory contents
                for item in os.listdir("."):
                    print(item)
            except Exception as e:
                print(f"ls: error listing files: {e}")

        # Handle 'echo' command
        elif main_command == "echo":
            # Join the remaining arguments and print
            echo = " ".join(command_array[1:])
            print(echo)
        
        # Handle 'type <command>' command
        elif main_command == "type" and len(command_array) > 1:
            word = command_array[1]
            print(f"{word} is /bin/{word}")
        elif main_command == "type":
            if len(command_array) > 1:
                evaled_command = command_array[1]
                if evaled_command in ["echo", "exit", "type"]:
                    print(f"{evaled_command} is a shell builtin")
            else:
                print("type: missing operand")

        
        # Handle invalid or unrecognized commands
        else:
            print(f"{main_command}: command not found")


if __name__ == "__main__":
    main()
