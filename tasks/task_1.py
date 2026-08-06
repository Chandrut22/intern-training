def greet(name):
    message = f"Hello, {name}!"
    return message


def main():
    print("Program started")

    name = "Alice"

    # breakpoint()  # Execution will pause here

    greeting = greet(name)
    print(greeting)

    print("Program finished")


if __name__ == "__main__":
    main()
