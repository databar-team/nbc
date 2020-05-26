from config.context import set_context
from controller.sender import send
import time


def main():
    set_context()

    start = time.time()
    send()
    end = time.time()

    print("time taken: {}".format(end - start))


if __name__ == "__main__":
    main()
