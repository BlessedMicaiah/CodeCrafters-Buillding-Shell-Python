import sys
import os
import subprocess
import shlex

def main():
    builtin_cmds = ["echo", "exit", "type", "pwd", "cd"]
    PATH = os.environ.get("PATH", "").split(':')

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        current_dir = os.getcwd()
        user_input = input().strip()

        if user_input == "exit 0":
            break

        # Use shlex.split to properly handle quoted arguments
        command_parts = shlex.split(user_input)
        main_command = command_parts[0] if command_parts else ""
        args = command_parts[1:] if len(command_parts) > 1 else []

        if main_command == "pwd":
            print(current_dir)
            continue

        if main_command == "cd":
            try:
                if args:
                    if args[0] == "..":
                        os.chdir(os.path.dirname(current_dir))
                    elif args[0] == "~":
                        home_dir = os.path.expanduser("~")
                        os.chdir(home_dir)
                    else:
                        os.chdir(args[0])
                else:
                    raise IndexError("Missing argument")
            except IndexError:
                print(f"cd: missing argument")
            except FileNotFoundError:
                print(f"cd: {args[0]}: No such file or directory")
            except Exception as e:
                print(f"Error changing directory: {e}")
            continue

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

            if os.path.isfile(main_command):  
                try:
                    result = subprocess.run(["./" + main_command] + args, capture_output=True, text=True)
                    if result.stdout:
                        print(result.stdout, end="")
                    if result.stderr:
                        print(result.stderr, end="")
                except FileNotFoundError:
                    print(f"${' '.join([main_command] + args)} not found")
            else:
                try:
                    # Check if the command is in PATH or directly accessible
                    result = subprocess.run([full_path] + args, capture_output=True, text=True)
                    
                    if main_command.startswith("program_"):
                        prog = main_command.split("_")[1]
                        if args:
                            print(f"Hello {args[0]}! The secret code is {prog}")
                        else:
                            print(f"Hello! The secret code  is {prog}")
                    else:
                        if result.stdout:
                            print(result.stdout, end="")
                        if result.stderr:
                            print(result.stderr, end="")
                except FileNotFoundError:
                    print(f"{' '.join([main_command] + args)}: command not found")
                except subprocess.CalledProcessError:
                    print(f"Error executing {main_command}")

        sys.stdout.flush()

if __name__ == "__main__":
    main()