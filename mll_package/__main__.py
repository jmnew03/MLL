import sys
from mll_package.run import MLL

def main():
    if len(sys.argv) != 2:
        print("Usage: mll <filename.yoon>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, "r", encoding="UTF-8") as file:
        code = file.read()

    interpreter = MLL()
    interpreter.compile(code)

if __name__ == "__main__":
    main()