import sys

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

        # Handle 'echo' command
        elif main_command == "echo":
            echo = ""
            for word in command_array[1:]:
                echo += f"{word} "
            print(echo.rstrip())
        
        # Handle 'type <command>' command
        elif main_command == "type":
            if len(command_array) > 1:
                evaled_command = command_array[1]
                if evaled_command in ["echo", "exit", "type"]:
                    print(f"{evaled_command} is a shell builtin")
                else:
                    print(f"{evaled_command}: not found")
            else:
                print("type: missing operand")
        
        # Handle invalid or unrecognized commands
        else:
            print(f"{main_command}: command not found")


if __name__ == "__main__":
    main()
