import json
import os
from datetime import datetime

# Makes the path for the json not dum
dir = os.path.dirname(__file__)
path = os.path.join(dir, "data.jsonl")
print(path)

# List of each levels xp requirement
xp_per_level = [
    0,
    2500,
    3000,
    3500,
    4000,
    5000,
    6000,
    7000,
    8000,
    9000,  # 1-10
    10000,
    12000,
    14000,
    16000,
    18000,
    21000,
    24500,
    28000,
    31500,
    35000,  # 11-20
    42000,
    49000,
    56000,
    63000,
    70000,
    83000,
    96000,
    109000,
    122000,
    135000,  # 21-30
    158000,
    181000,
    204000,
    227000,
    250000,
    290000,
    330000,
    370000,
    410000,
    450000,  # 31-40
    520000,
    590000,
    660000,
    730000,
    800000,
    900000,
    1000000,
    1100000,
    1200000,
    1300000,  # 41-50
    1440000,
    1580000,
    1720000,
    1860000,
    2000000,
    2200000,
    2400000,
    2600000,
    2800000,
    3000000,  # 51-60
    3350000,
    3700000,
    4050000,
    4400000,
    4750000,
    5250000,
    5750000,
    6250000,
    6750000,
    7250000,  # 61-70
    8000000,
    8750000,
    9500000,
    10250000,
    11000000,
    12000000,
    13000000,
    14000000,
    15000000, # 71-80
    16000000,  ]

# A class as a container for general use functions
class utils:
    @staticmethod
    # Clears console - currently unused, but handy
    def clear_console():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    # Just waits for an input, instead of typing input()
    def wait_for_enter():
        input("\nPress Enter to continue…")

    def yes_no_input(prompt):
        while True:
            user_input = input(prompt)

            if user_input == "yes":
                return True
            elif user_input == "no":
                return False
            else:
                continue

    @staticmethod
    # Special input function to guarantee that a input can be int()ed
    def int_input(prompt, min=None, max=None):
        while True:
            try:
                value = int(input(prompt))

                if min is not None and value < min:
                    print(f"Value can't be lower than {min}")
                    continue

                elif max is not None and value > max:
                    print(f"Value can't be higher than {max}")
                    continue

                return value

            except ValueError:
                print("Invalid number.")

# A class as a container for all things regarding the jsonl
class json_utils:
    @staticmethod
    # Dumps an entry (dict) and optionally you can input a path, but it defaults to data.jsonl, which is also called "path"
    def dump_entry(entry, path=path):
        with open(path, "a") as f:
            json.dump(entry, f)
            f.write("\n")

    @staticmethod
    # Opens the jsonL file and reads every line and exports each line. It also ignores empty lines for convenience
    def read_entries(path=path):
        entries = []

        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:  # skip empty lines
                    continue
                entry = json.loads(line)
                entries.append(entry)

        return entries

# A class as a container for xp printing and calculation related functions
class xp_utils:
    @staticmethod
    # Indexes xp_per_level based on user level and returns total - how much xp it takes for a level
    def total_through_level(level):
        return sum(xp_per_level[:level])

    @staticmethod
    # Gets the total xp of a trainer based on their current xp and their level. Returns a value, does not print
    def get_trainer_total(name):
        level = utils.int_input(f"Enter {name}'s level: ", 1, 80)
        xp = utils.int_input(f"Enter {name}'s xp: ", 0)
        return xp_utils.total_through_level(level) + xp

    @staticmethod
    # Users xp_utils.get_trainer_total to print out a value. This is used in case 1
    def print_single_trainer():
        # Gets level and xp
        level = utils.int_input("Enter your level: ")
        xp = utils.int_input("Enter your current xp: ")

        # Prints out total xp using xp_utils.total_through_level() function
        print("")
        print("Total xp: " + str(format(xp_utils.total_through_level(level) + xp, ",")))
        print("")

    @staticmethod
    # Enter two total xp values and saves them to a json with other information such as name and date. Used in case 2 and 3.
    def print_and_store_difference(trainer_1, trainer_2, wants_data_dumped = True):
        trainer_one_total = xp_utils.get_trainer_total(trainer_1)
        trainer_two_total = xp_utils.get_trainer_total(trainer_2)

        # Starts the entry that will dump into JSONL
        entry = {
            "p1": trainer_1,
            "p2": trainer_2,
        }

        # Prints out informations, then adds "difference" and "leading" (the person with more xp) to the entry, to be dumped.
        print("")

        if trainer_one_total > trainer_two_total:
            print(
                f"{trainer_1} has {str(format(trainer_one_total - trainer_two_total, ","))} more XP than {trainer_2}."
            )
            entry["difference"] = trainer_one_total - trainer_two_total
            entry["leading"] = entry["p1"]

        elif trainer_two_total > trainer_one_total:
            print(
                f"{trainer_2} has {str(format(trainer_two_total - trainer_one_total, ","))} more XP than {trainer_1}."
            )
            entry["difference"] = trainer_two_total - trainer_one_total
            entry["leading"] = entry["p2"]

        elif trainer_two_total == trainer_one_total:
            print(
                f"Both trainers have the same XP, noob. ({abs(trainer_one_total)})")
            entry["difference"] = 0
            entry["leading"] = "Tie"
        print("")

        # Adds date to the entry, to be dumped
        entry["date"] = str(datetime.now())

        # Adds p1 and p2 xp to the entry, to be dumped, for posterity
        entry["p1_xp"] = trainer_one_total
        entry["p2_xp"] = trainer_two_total

        # Dumps entry to a new line on data.jsonl
        if wants_data_dumped:
            json_utils.dump_entry(entry)

# A class as a container for log related functions, to keep things more organized
class log:
    @staticmethod
    def beautify_date(date):
        date_str = date.strftime("%Y-%m-%d")
        return date_str

    @staticmethod
    def get_entries_by_p2(p2_name):
        print("")
        kept_entries = []

        for entry in json_utils.read_entries():
            if entry["p2"] == p2_name:
                kept_entries.append(entry)

        return kept_entries

    @staticmethod
    def get_recent_entry_for_each_p2():
        entries = json_utils.read_entries()

        recent_entries = []
        found_names = []

        for entry in reversed(entries):
            if entry["p2"] not in found_names:
                recent_entries.append(entry)
                found_names.append(entry["p2"])

        return recent_entries

    def get_p1_recent_xp():
        entries = json_utils.read_entries()

        return entries[-1]["p1_xp"]

    ##########
    # Below are various ways to print the log
    ##########

    # Prints the entire log, raw
    @staticmethod
    def print_raw():
        print("")

        for entry in json_utils.read_entries():
            print(entry)

        utils.wait_for_enter()

    # Prints the last X entries, raw
    @staticmethod
    def print_last_raw(amount):
        print("")

        for entry in json_utils.read_entries()[-amount:]:
            print(entry)

        utils.wait_for_enter()

    # Prints minimal log information, very clean
    @staticmethod
    def print_concise():
        print("")

        for entry in json_utils.read_entries():
            print(
                f"{entry['p1']} {entry['p2']} - {entry['difference']:,} - {entry['leading']}")

        utils.wait_for_enter()

    # Prints last X entries, minimal information
    @staticmethod
    def print_last_concise(amount):
        print("")

        for entry in json_utils.read_entries()[-amount:]:
            print(
                f"{entry['p1']} {entry['p2']} - {entry['difference']:,} - {entry['leading']}")

        utils.wait_for_enter()

    @staticmethod
    def print_with_dates():
        print("")

        for entry in json_utils.read_entries():
            print(
                f"{entry['date']} - {entry['p1']} {entry['p2']} - {entry['difference']:,} - {entry['leading']}")

        utils.wait_for_enter()

    # Prints the log with the date, but without hours, minutes, or seconds
    @staticmethod
    def print_with_dates_clean(entries=json_utils.read_entries()):
        print("")

        for entry in entries:
            print(
                f"{log.beautify_date(date)} - {entry['p1']} {entry['p2']} - {entry['difference']:,} - {entry['leading']}")

        utils.wait_for_enter()

    # Prints all entries that have a specific p2, uses print_with_dates_clean
    @staticmethod
    def print_with_specific_p2():
        print("")

        p2_entries = get_entries_by_p2(input("Enter name of p2: "))

        print(log.print_with_dates_clean(p2_entries))

    # Prints the differences over time
    @staticmethod
    def print_differences_with_specific_p2():
        print("")

        p2_entries = get_entries_by_p2(input("Enter name of p2: "))

        differences_list = []

        for entry in p2_entries:
            differences_list.append(
                [entry['difference'], entry['p2'], entry['leading'], entry['date']])

        difference_total = 0

        for difference in differences_list:
            if difference[1] == difference[2]:
                difference_total -= difference[0]
            else:
                difference_total += difference[0]
            print(f"{difference_total} - f{log.beautify_date(difference[3])}")

    def print_current_rankings():
        recent_entries = log.get_recent_entry_for_each_p2()

        recent_entries.append({"p1": "Me", "p2": "Me", "difference": 0, "leading": "Me", "date": "null", "p1_xp": log.get_p1_recent_xp(), "p2_xp": log.get_p1_recent_xp()})

        sorted_entries = sorted(recent_entries, key=lambda x: x["p2_xp"], reverse=True)

        snapshot = ""

        for i, entry in enumerate(sorted_entries):
            snapshot = snapshot + "\n" + f"{i + 1}: {entry["p2"]} | {entry["p2_xp"]} XP | {entry["p2_xp"] - log.get_p1_recent_xp():,}"
        
        utils.clear_console()
        print(snapshot)

        should_save_snapshot = utils.yes_no_input("\nWould you like to save a snapshot of these results? (yes/no) : ")

        if should_save_snapshot == True:
            print("\nSnapshot saved to snapshots.jsonl\n")
            json_utils.dump_entry({"snapshot": snapshot, "date": str(datetime.now())}, os.path.join(dir, "snapshots.jsonl"))

# Prints log options and asks which one to run, then runs it from the log class
def xp_log():
    print("Log Options: ")
    print("1. Print raw log")
    print("2. Print last X entries raw")
    print("3. Print concise log")
    print("4. Print last X entries concise")
    print("5. Print log with dates")
    print("6. Print log with dates (clean)")
    print("7. Print with specific p2")
    print("8. Print all differences with specific p2")
    print("9. Print current rankings")

    opt = utils.int_input("Choose an option: ", 1)

    match opt:
        case 1:
            log.print_raw()
        case 2:
            amount = utils.int_input("How many entries to print: ", 1)
            log.print_last_raw(amount)
        case 3:
            log.print_concise()
        case 4:
            amount = utils.int_input("How many entries to print: ", 1)
            log.print_last_concise(amount)
        case 5:
            log.print_with_dates()
        case 6:
            log.print_with_dates_clean()
        case 7:
            log.print_with_specific_p2()
        case 8:
            log.print_differences_with_specific_p2()
        case 9:
            log.print_current_rankings()

# Program loop, repeatedly asks which function to run until program is quit with last option
while True:
    print("Pokemon Go Stuff: ")
    print("1. Total XP of single trainer")
    print("2. XP difference between me and other person (saved to JSONL)")
    print("3. ACTUAL XP difference between two trainer")
    print("4. Get XP log")
    print("5. Quit")
    print("")

    opt = utils.int_input("Choose an option: ", 1, 4)

    match opt:
        case 1:  # Total XP of single trainer
            xp_utils.print_single_trainer()

        case 2:  # XP difference between me and other person (saved to JSONL)
            xp_utils.print_and_store_difference(
                "Me", input("Who is the other person: ")
            )

        case 3:  # XP dif between two people of your choosing
            xp_utils.print_and_store_difference(
                input("Enter name of first person: "),
                input("Enter name of second person: "),
                False
            )

        case 4:
            xp_log()

        case 5:
            print("cya")
            exit()

