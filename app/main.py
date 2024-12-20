import sys
import os

def main():
    builtin_cmds = ["echo", "exit", "type"]
    PATH = os.environ.get("PATH", "").split(':')

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = input().strip()

        if user_input == "exit 0":
            break

        command_parts = user_input.split(" ", 1)
        main_command = command_parts[0]

        if main_command == "echo":
            echo_output = command_parts[1] if len(command_parts) > 1 else ""
            sys.stdout.write(echo_output + "\n")
            sys.stdout.flush()

        elif main_command == "type":
            if len(command_parts) < 2:
                sys.stdout.write("type: missing operand\n")
            else:
                cmd = command_parts[1]
                if cmd in builtin_cmds:
                    sys.stdout.write(f"{cmd} is a shell builtin\n")
                else:
                    cmd_path = next((f"{path}/{cmd}" for path in PATH if os.path.isfile(f"{path}/{cmd}")), None)
                    if cmd_path:
                        sys.stdout.write(f"{cmd} is {cmd_path}\n")
                    else:
                        sys.stdout.write(f"{cmd}: not found\n")
            sys.stdout.flush()

        else:
            sys.stdout.write(f"{main_command}: command not found\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()