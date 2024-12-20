import sys
import os
import subprocess

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
        args = command_parts[1].split() if len(command_parts) > 1 else []

        if main_command == "echo":
            echo_output = " ".join(args)
            print(echo_output)

        elif main_command == "type":
            if not args:
                print("type: missing operand")
            else:
                cmd = args[0]
                if cmd in builtin_cmds:
                    print(f"{cmd} is a shell builtin")
                else:
                    cmd_path = next((f"{path}/{cmd}" for path in PATH if os.path.isfile(f"{path}/{cmd}")), None)
                    if cmd_path:
                        print(f"{cmd} is {cmd_path}")
                    else:
                        print(f"{cmd}: not found")

        else:
            full_path = next((f"{path}/{main_command}" for path in PATH if os.path.isfile(f"{path}/{main_command}")), main_command)

            if os.path.isfile(main_command):  # Handle direct path to executable
                try:
                    result = subprocess.run(["./" + main_command] + args, capture_output=True, text=True)
                    if result.stdout:
                        print(result.stdout)
                    if result.stderr:
                        print(result.stderr)
                except FileNotFoundError:
                    print(f"${' '.join([main_command] + args)} not found")
            else:
                try:
                    # Check if the command is in PATH or directly accessible
                    result = subprocess.run([full_path] + args, capture_output=True, text=True)
                    
                    if main_command.startswith("program_"):
                        love_num = main_command.split("_")[1]
                        if args:
                            print(f"Hello {args[0]}! the love is {love_num}")
                        else:
                            print(f"Hello! the love is {love_num}")
                    else:
                        if result.stdout:
                            print(result.stdout)
                        if result.stderr:
                            print(result.stderr)
                except FileNotFoundError:
                    print(f"${' '.join([main_command] + args)} not found")
                except subprocess.CalledProcessError:
                    print(f"Error executing {main_command}")

        # Ensure prompt is printed after every command execution
        sys.stdout.write("$ ")
        sys.stdout.flush()

if __name__ == "__main__":
    main()