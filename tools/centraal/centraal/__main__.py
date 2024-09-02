import argparse
import master.init

parser = argparse.ArgumentParser(
    description="Centraal CLI to manage clusters and services."
)
parser.add_argument("tool", choices=["master"])
parser.add_argument("subtool")

if __name__ == "__main__":

    args, unknown = parser.parse_known_args()
    tool = args.tool
    subtool = args.subtool

    if tool == "master" and subtool == "init":
        master.init.main()
        exit(0)
    else:
        print("unknown subtool")
        exit(1)
