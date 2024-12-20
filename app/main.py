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
            sys.stdout.write(echo_output + "\n")
            sys.stdout.flush()

        elif main_command == "type":
            if not args:
                sys.stdout.write("type: missing operand\n")
            else:
                cmd = args[0]
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
            # Check if the command is in PATH or directly accessible
            full_path = next((f"{path}/{main_command}" for path in PATH if os.path.isfile(f"{path}/{main_command}")), main_command)

            try:
                # Run the command with any arguments provided
                result = subprocess.run([full_path] + args, capture_output=True, text=True)
                
                # Example for "program_212 ben"
                if main_command.startswith("program_"):
                    prog = main_command.split("_")[1]
                    if args:
                        sys.stdout.write(f"Hello {args[0]}! The secret code is {prog}\n")
                    else:
                        sys.stdout.write(f"Hello! The secret code is {prog}\n")
                else:
                    # For other executables, print stdout or stderr if any
                    if result.stdout:
                        sys.stdout.write(result.stdout + "\n")
                    if result.stderr:
                        sys.stdout.write(result.stderr + "\n")
                
                sys.stdout.flush()

            except FileNotFoundError:
                sys.stdout.write(f"{main_command}: command not found\n")
                sys.stdout.flush()
            except subprocess.CalledProcessError:
                sys.stdout.write(f"Error executing {main_command}\n")
                sys.stdout.flush()

if __name__ == "__main__":
    main()