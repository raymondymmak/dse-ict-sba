import json
import datetime
import os
import re

# INIT
DATA_FILE = "data.json"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"
TIME_SLOT_PATTERN = re.compile(
    r"^(\d{2}:\d{2})-(\d{2}:\d{2})$"
)  # thank you https://stackoverflow.com/questions/69806492/regex-d4-d2-d2
classrooms = []
bookings = []
users = []
currentUser = None


# DATA MANAGEMENT HELPERS
def load_data():
    global classrooms, bookings, users

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            classrooms = data.get("classrooms", [])
            bookings = data.get("bookings", [])
            users = data.get("users", [])
        print(f"Data loaded from {DATA_FILE}")

    else:
        # Initialize some default stuff if no file exists
        print(f"No data file found ({DATA_FILE}). Starting with empty data.")
        classrooms.extend(
            [
                {
                    "roomID": "C01",
                    "roomName": "Classroom 1A",
                    "roomCapacity": 35,
                    "hasProjector": True,
                    "hasWhiteboard": False,
                    "hasComputers": False,
                },
                {
                    "roomID": "C02",
                    "roomName": "Classroom 1B",
                    "roomCapacity": 35,
                    "hasProjector": True,
                    "hasWhiteboard": False,
                    "hasComputers": False,
                },
                {
                    "roomID": "C03",
                    "roomName": "Classroom 1C",
                    "roomCapacity": 35,
                    "hasProjector": True,
                    "hasWhiteboard": False,
                    "hasComputers": False,
                },
                {
                    "roomID": "C11",
                    "roomName": "Classroom 2A",
                    "roomCapacity": 35,
                    "hasProjector": False,
                    "hasWhiteboard": True,
                    "hasComputers": False,
                },
                {
                    "roomID": "C12",
                    "roomName": "Classroom 2B",
                    "roomCapacity": 35,
                    "hasProjector": False,
                    "hasWhiteboard": True,
                    "hasComputers": False,
                },
                {
                    "roomID": "C13",
                    "roomName": "Classroom 2C",
                    "roomCapacity": 35,
                    "hasProjector": False,
                    "hasWhiteboard": True,
                    "hasComputers": False,
                },
                {
                    "roomID": "D01",
                    "roomName": "Hall",
                    "roomCapacity": 1200,
                    "hasProjector": True,
                    "hasWhiteboard": False,
                    "hasComputers": False,
                },
                {
                    "roomID": "D02",
                    "roomName": "Covered Playground",
                    "roomCapacity": 100,
                    "hasProjector": False,
                    "hasWhiteboard": False,
                    "hasComputers": False,
                },
                {
                    "roomID": "E01",
                    "roomName": "InnoHub",
                    "roomCapacity": 40,
                    "hasProjector": True,
                    "hasWhiteboard": True,
                    "hasComputers": True,
                },
                {
                    "roomID": "E02",
                    "roomName": "Chem Lab",
                    "roomCapacity": 25,
                    "hasProjector": False,
                    "hasWhiteboard": True,
                    "hasComputers": True,
                },
                {
                    "roomID": "E03",
                    "roomName": "Bio Lab",
                    "roomCapacity": 25,
                    "hasProjector": False,
                    "hasWhiteboard": True,
                    "hasComputers": False,
                },
                {
                    "roomID": "E04",
                    "roomName": "Phy Lab",
                    "roomCapacity": 25,
                    "hasProjector": False,
                    "hasWhiteboard": True,
                    "hasComputers": False,
                },
            ]
        )
        bookings.extend(
            [
                {
                    "roomID": "D02",
                    "roomName": "Covered Playground",
                    "bookDate": "2025-10-15",
                    "bookTime": "10:00-20:00",
                    "bookUsername": "t_tyy",
                    "bookTeacher": "Ms Tse",
                    "bookSubject": "Singing Performance",
                    "bookClass": "5E",
                    "bookRemarks": "好好聽",
                },
            ]
        )
        users.extend(
            [
                {"username": "admin", "password": "admin123", "role": "admin"},
                {"username": "t_wkw", "password": "teacher123", "role": "teacher"},
                {"username": "t_tyy", "password": "teacher123", "role": "teacher"},
                {"username": "s20200073", "password": "student123", "role": "student"},
            ]
        )
        print("Default classrooms added. You can edit the list via the admin menu.")
        save_data()  # Save initial data


def save_data():
    data = {
        "classrooms": classrooms,
        "bookings": bookings,
        "users": users,
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {DATA_FILE}")


# MAIN
def login():
    print("Welcome to the CWY Booking System!")
    while True:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        global currentUser
        currentUser = next(
            (
                u
                for u in users
                if u["username"] == username and u["password"] == password
            ),
            None,
        )

        if currentUser:
            print(
                f"Login successful! Welcome, {currentUser['username']} ({currentUser['role']})"
            )
            if currentUser["role"] == "admin":
                admin_menu()
            elif currentUser["role"] == "teacher":
                teacher_menu()
            elif currentUser["role"] == "student":
                student_menu()
            break
        else:
            print("Invalid username or password. Please try again.")


# MENUS
def teacher_menu():
    while True:
        print("\n+==============================+")
        print("|      CWY Teacher Menu        |")
        print("+==============================+")
        print("| 1. Show Classrooms           |")
        print("| 2. Show Bookings             |")
        print("| 3. Book Classroom            |")
        print("| 4. Cancel Booking            |")
        print("| 5. Exit                      |")
        print("+==============================+")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_classrooms()
        elif choice == "2":
            show_bookings()
        elif choice == "3":
            book_classroom()
        elif choice == "4":
            cancel_booking()
        elif choice == "5":
            print("Exiting CWY Booking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")


def admin_menu():
    while True:
        print("\n+==============================+")
        print("|        CWY Admin Menu        |")
        print("+==============================+")
        print("| 1. Show Classrooms           |")
        print("| 2. Show Bookings             |")
        print("| 3. Book Classroom            |")
        print("| 4. Cancel Booking            |")
        print("| 5. Edit Classrooms           |")
        print("| 6. Exit                      |")
        print("+==============================+")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_classrooms()
        elif choice == "2":
            show_bookings()
        elif choice == "3":
            book_classroom()
        elif choice == "4":
            cancel_booking()
        elif choice == "5":
            edit_classrooms()
        elif choice == "6":
            print("Exiting CWY Admin Menu. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")


def student_menu():
    while True:
        print("\n+==============================+")
        print("|       CWY Student Menu       |")
        print("+==============================+")
        print("| 1. Show Classrooms           |")
        print("| 2. Show Bookings             |")
        print("| 3. Exit                      |")
        print("+==============================+")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_classrooms()
        elif choice == "2":
            show_bookings()
        elif choice == "3":
            print("Exiting CWY Student Menu. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")


# FUNCTIONS
def show_classrooms():
    print("\n--- Available Classrooms ---")
    print(
        f"{'ID':<10}{'Name':<25}{'Capacity':<10}{'Projector':<12}{'Whiteboard':<12}{'Computers':<12}"
    )
    print("-" * 80)
    for room in classrooms:
        print(
            f"{room['roomID']:<10}{room['roomName']:<25}{room['roomCapacity']:<10}"
            f"{'✔' if room['hasProjector'] else '':<12}"
            f"{'✔' if room['hasWhiteboard'] else '':<12}"
            f"{'✔' if room['hasComputers'] else '':<12}"
        )
    print("-" * 80)


def show_bookings():
    if not bookings:
        print("\nNo bookings yet.")
        return

    i = 0

    print("\n----- Current Bookings -----")
    for booking in bookings:
        i += 1
        print(
            f"  {i}. {_get_classroom_by_id(booking['roomID'])['roomName']} - {booking['roomID']}"
        )
        print(f"     Date: {booking['bookDate']}, Time: {booking['bookTime']}")
        print(
            f"     Booked by: {booking['bookTeacher']} for {booking['bookSubject']} (with class {booking['bookClass']})"
        )
        print(
            f"     Remarks: {booking.get('bookRemarks', 'N/A')}"
        )  # .get can handle missing keys
    print("----------------------------")


def book_classroom():
    show_classrooms()
    roomID = (
        input(
            "Enter Classroom ID to book, or type 'filter projector', 'filter whiteboard', or 'filter computers': "
        )
        .strip()
        .upper()
    )

    # Filtering logic
    filtered = False
    # If filtering, get bulk dates and time, and use for all logic
    if roomID.startswith("FILTER"):
        filter_type = roomID.split()
        if len(filter_type) == 2 and filter_type[1] in [
            "PROJECTOR",
            "WHITEBOARD",
            "COMPUTERS",
        ]:
            filter_key = {
                "PROJECTOR": "hasProjector",
                "WHITEBOARD": "hasWhiteboard",
                "COMPUTERS": "hasComputers",
            }[filter_type[1]]
            print(f"Filtering for classrooms with {filter_key[3:].capitalize()}...")
            date_str = input(
                "Enter dates separated by commas (YYYY-MM-DD,YYYY-MM-DD,...): "
            ).strip()
            date_list = [d.strip() for d in date_str.split(",") if d.strip()]
            bookDates = []
            for d in date_list:
                try:
                    bookingDate = datetime.datetime.strptime(d, DATE_FORMAT).date()
                    if bookingDate < datetime.date.today():
                        print(f"Error: {d} is in the past.")
                        return
                    bookDates.append(d)
                except ValueError:
                    print(f"Invalid date format: {d}. Please use YYYY-MM-DD.")
                    return
            bookTime = _get_valid_time_slot_input()
            # Only show rooms available for ALL dates
            available_rooms = [room for room in classrooms if room.get(filter_key)]
            available_rooms = [
                room
                for room in available_rooms
                if all(
                    _is_classroom_available(room["roomID"], d, bookTime)
                    for d in bookDates
                )
            ]
            if not available_rooms:
                print("No available classrooms match your filter, dates, and timeslot.")
                return
            print("\n--- Filtered Available Classrooms ---")
            for room in available_rooms:
                print(
                    f"{room['roomID']:<10}{room['roomName']:<25}{room['roomCapacity']:<10}"
                )
            print("-------------------------------------")
            roomID = (
                input("Enter Classroom ID to book from the filtered list: ")
                .strip()
                .upper()
            )
            filtered = True
        else:
            print(
                "Invalid filter. Try 'filter projector', 'filter whiteboard', or 'filter computers'."
            )
            return

    room = _get_classroom_by_id(roomID)
    if not room:
        print(f"Error: Classroom with ID '{roomID}' not found.")
        return

    print("You are booking for multiple dates (bulk booking).")
    if not filtered:
        date_str = input(
            "Enter dates separated by commas (YYYY-MM-DD,YYYY-MM-DD,...): "
        ).strip()
        date_list = [d.strip() for d in date_str.split(",") if d.strip()]
        bookDates = []
        for d in date_list:
            try:
                bookingDate = datetime.datetime.strptime(d, DATE_FORMAT).date()
                if bookingDate < datetime.date.today():
                    print(f"Error: {d} is in the past.")
                    return
                bookDates.append(d)
            except ValueError:
                print(f"Invalid date format: {d}. Please use YYYY-MM-DD.")
                return
        bookTime = _get_valid_time_slot_input()
    # else: bookDates, bookTime already set

    bookTeacher = input("Enter Teacher's Name: ").strip()
    bookSubject = input("Enter Subject Name: ").strip()
    bookClass = input("Enter Class Name (eg 5E): ").strip()
    bookRemarks = input("Enter Remarks (optional): ").strip()
    if not bookRemarks:
        bookRemarks = ""

    if not bookTeacher or not bookSubject or not bookClass:
        print("Teacher name, subject, and class name cannot be empty.")
        return

    print("\n")
    for bookDate in bookDates:
        if _is_classroom_available(roomID, bookDate, bookTime):
            new_booking = {
                "roomID": roomID,
                "bookDate": bookDate,
                "bookTime": bookTime,
                "bookUsername": currentUser["username"],
                "bookTeacher": bookTeacher,
                "bookSubject": bookSubject,
                "bookClass": bookClass,
                "bookRemarks": bookRemarks,
            }
            bookings.append(new_booking)
            print(f"Successfully booked {roomID} for {bookDate} at {bookTime}.")
        else:
            print(
                f"Error: {roomID} is already booked for {bookDate} during {bookTime} (overlap detected)."
            )
            continue
    save_data()


def cancel_booking():
    if not bookings:
        print("\nNo bookings to cancel.")
        return

    show_bookings()
    try:
        booking_index = int(input("Enter the number of the booking to cancel: ")) - 1
        if 0 <= booking_index < len(bookings):
            canceled_booking = bookings[booking_index]
            # Only allow if admin or teacher is the booker
            if currentUser["role"] == "admin" or (
                currentUser["role"] == "teacher"
                and canceled_booking["bookUsername"].lower()
                == currentUser["username"].lower()
            ):
                bookings.pop(booking_index)
                save_data()
                roomName = _get_classroom_by_id(canceled_booking["roomID"])["roomName"]
                print(
                    f"\nBooking for {roomName} on {canceled_booking['bookDate']} {canceled_booking['bookTime']} by {canceled_booking['bookTeacher']} has been cancelled."
                )
            else:
                print("You do not have permission to cancel this booking.")
        else:
            print("Invalid booking number.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def edit_classrooms():
    print("not implemented yet")


# HELPERS
def _get_classroom_by_id(roomID):
    for room in classrooms:
        if room["roomID"] == roomID:
            return room
    return None


def _get_valid_date_input(prompt="Enter date (YYYY-MM-DD): "):
    while True:
        date_str = input(prompt).strip()
        try:
            bookingDate = datetime.datetime.strptime(date_str, DATE_FORMAT).date()
            if bookingDate < datetime.date.today():
                print("Error: Cannot book for a past date.")
                continue
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def _get_valid_time_slot_input():
    while True:
        time_slot_str = input(
            "Enter time slot (HH:MM-HH:MM, e.g., 09:00-13:00): "
        ).strip()

        match = TIME_SLOT_PATTERN.match(time_slot_str)  # i learned regex for this smh
        if not match:
            print(
                "Invalid time slot format. Please use HH:MM-HH:MM (e.g., 08:00-09:00)."
            )
            continue
        start_time_str, end_time_str = match.groups()

        try:
            start_time = datetime.datetime.strptime(start_time_str, TIME_FORMAT).time()
            end_time = datetime.datetime.strptime(end_time_str, TIME_FORMAT).time()
            if start_time >= end_time:
                print("Error: End time must be after start time.")
                continue
        except ValueError:  # catch invalid time format
            print("Invalid time format within the slot (from 00:00 to 23:59).")
            continue

        # check if the time slot is within standard school hours
        if start_time < datetime.time(7, 0) or end_time > datetime.time(
            17, 0
        ):  # 07:00 to 17:00
            confirm = (
                input(
                    f"Warning: This time slot is outside standard school hours. Continue? (y/n): "
                )
                .strip()
                .lower()
            )
            if confirm != "yes" and confirm != "y":
                continue

        return time_slot_str


def _is_classroom_available(roomID, bookDate, bookTime):
    match = TIME_SLOT_PATTERN.match(bookTime)
    reqStart, reqEnd = match.groups()

    for booking in bookings:
        # Check if it's the same classroom and date
        if booking["roomID"] == roomID and booking["bookDate"] == bookDate:

            # Extract start and end times from the existing booking's bookTime
            existingMatch = TIME_SLOT_PATTERN.match(booking["bookTime"])
            existingStart, existingEnd = existingMatch.groups()

            # Check for overlap with the existing booking
            if _is_time_overlap(reqStart, reqEnd, existingStart, existingEnd):
                return False  # Not available (overlap found)

    return True  # Available


def _is_time_overlap(start1_str, end1_str, start2_str, end2_str):
    try:
        start1 = datetime.datetime.strptime(start1_str, TIME_FORMAT).time()
        end1 = datetime.datetime.strptime(end1_str, TIME_FORMAT).time()
        start2 = datetime.datetime.strptime(start2_str, TIME_FORMAT).time()
        end2 = datetime.datetime.strptime(end2_str, TIME_FORMAT).time()

        return (
            start1 < end2 and start2 < end1
        )  # covers all overlap, includes touching at endpoints

    except ValueError:
        # just in case
        print(
            "Error: Invalid time format encountered during overlap check. Problem on our side."
        )
        return False


# ENTRY
if __name__ == "__main__":
    load_data()
    login()
