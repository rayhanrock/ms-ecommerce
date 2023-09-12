import subprocess

compose_files = [
    "./services/account/docker-compose.yml",
    "./services/product/docker-compose.yml",
    "./services/cart/docker-compose.yml",
    "./services/order_payment/docker-compose.yml"
    # Add more compose file paths as needed
]


def get_input():
    while True:
        try:
            input_choice = int(input("Enter your choice: "))
            if 0 <= input_choice <= len(compose_files):
                return input_choice
            else:
                print("Invalid choice. Please enter a valid option.")
        except ValueError:
            print("Invalid input. Please enter a valid option.")


def run_containers():
    print("Select a container to run:")
    for index, compose_file in enumerate(compose_files):
        print(f"{index + 1}. Run {compose_file}")
    print("0. Run all containers")

    input_choice = get_input()

    if input_choice == 0:
        for compose_file in compose_files:
            print(f"Running containers from {compose_file}...")
            subprocess.run(["docker-compose", "-f", compose_file, "up", "-d"])
        print("All containers started.")
    else:
        selected_file = compose_files[input_choice - 1]
        print(f"Running containers from {selected_file}...")
        subprocess.run(["docker-compose", "-f", selected_file, "up", "-d"])
        print("Containers started.")


def view_logs():
    for index, compose_file in enumerate(compose_files):
        print(f"{index}. Log {compose_file}")

    input_index = get_input()

    selected_file = compose_files[input_index]
    print(f"You selected: {selected_file}")
    subprocess.run(["docker-compose", "-f", selected_file, "logs", "-f"])


def stop_containers():
    for compose_file in compose_files:
        print(f"Stopping and removing containers from {compose_file}...")
        subprocess.run(["docker-compose", "-f", compose_file, "down"])
    print("All containers stopped and removed.")


while True:
    print("\nSelect an option:")
    print("1. Run Containers")
    print("2. View Logs")
    print("3. Stop Containers")
    print("0. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":
        run_containers()
    elif choice == "2":
        view_logs()
    elif choice == "3":
        stop_containers()
    elif choice == "0":
        break
    else:
        print("Invalid choice. Please select a valid option.")
