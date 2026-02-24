import os
from rich import print


def main() -> None:
    """The main of program"""

    os.system(command="cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        pass

    except Exception as error:
        print(f"[-] {error}!")

    print()