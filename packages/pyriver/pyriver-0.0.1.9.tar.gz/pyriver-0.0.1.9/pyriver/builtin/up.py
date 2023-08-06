import subprocess


def execute(args):
    if not args.detach:
        subprocess.call(["river-server"])
        return
    subprocess.Popen(["river-server"])
    print("River server started successfully.")

