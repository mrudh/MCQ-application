

import os
import json

from quiz_data import ALL_QUIZ_DATA, FILL_IN_QUIZ_DATA

LINKS_FILE = "answer_links.json"

DEFAULT_MCQ_LINKS = {
    1: ["https://en.wikipedia.org/wiki/Periodic_table"],
    2: ["https://en.wikipedia.org/wiki/Ostrich"],
    3: ["https://en.wikipedia.org/wiki/Atmosphere_of_Earth"],
    4: ["https://en.wikipedia.org/wiki/Human_skeleton"],
    5: ["https://solarsystem.nasa.gov/planets/venus/overview/"],
    6: ["https://en.wikipedia.org/wiki/Gold"],
    7: ["https://en.wikipedia.org/wiki/Heart"],
    8: ["https://en.wikipedia.org/wiki/Structure_of_the_Earth"],
    9: ["https://en.wikipedia.org/wiki/Cell_nucleus"],
    10: ["https://solarsystem.nasa.gov/planets/jupiter/overview/"],
    11: ["https://en.wikipedia.org/wiki/Mitochondrion"],
    12: ["https://en.wikipedia.org/wiki/Photosynthesis"],
    13: ["https://solarsystem.nasa.gov/planets/jupiter/overview/"],
    14: ["https://en.wikipedia.org/wiki/White_blood_cell"],
    15: ["https://en.wikipedia.org/wiki/Mercury_(element)"],
    16: ["https://en.wikipedia.org/wiki/Evaporation"],
    17: ["https://solarsystem.nasa.gov/planets/mars/overview/"],
    18: ["https://en.wikipedia.org/wiki/Diamond"],
    19: ["https://en.wikipedia.org/wiki/Heart"],
    20: ["https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion"],
    21: ["https://en.wikipedia.org/wiki/Cell_(biology)"],
    22: ["https://solarsystem.nasa.gov/planets/uranus/overview/"],
    23: ["https://en.wikipedia.org/wiki/Water#Boiling_point"],
    24: ["https://en.wikipedia.org/wiki/Vitamin_D"],
    25: ["https://en.wikipedia.org/wiki/Oxygen"],
    26: ["https://en.wikipedia.org/wiki/Milky_Way"],
    27: ["https://en.wikipedia.org/wiki/Oxygen"],
    28: ["https://en.wikipedia.org/wiki/Femur"],
    29: ["https://en.wikipedia.org/wiki/Rayleigh_scattering"],
    30: ["https://solarsystem.nasa.gov/planets/saturn/overview/"],
}

DEFAULT_FILL_LINKS = {
    1: ["https://en.wikipedia.org/wiki/Gold"],
    2: ["https://solarsystem.nasa.gov/planets/jupiter/overview/"],
    3: ["https://en.wikipedia.org/wiki/Mitochondrion"],
    4: ["https://en.wikipedia.org/wiki/Oxygen"],
    5: ["https://en.wikipedia.org/wiki/Diamond"],
}



def _load_links():
    
    if os.path.exists(LINKS_FILE):
        try:
            with open(LINKS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            
            return {}
    return {}


def _save_links(data):
    
    with open(LINKS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _key_for_mcq(index):
    
    return f"MCQ-{index}"


def _key_for_fill(index):
    
    return f"FILL-{index}"



def get_links_for_mcq(index):
    
    links_data = _load_links()
    key = _key_for_mcq(index)
    user_links = links_data.get(key, [])
    default_links = DEFAULT_MCQ_LINKS.get(index, [])

    merged = list(default_links)
    for link in user_links:
        if link not in merged:
            merged.append(link)
    return merged


def add_link_for_mcq(index, link):
    
    links_data = _load_links()
    key = _key_for_mcq(index)
    links_data.setdefault(key, [])
    if link not in links_data[key]:
        links_data[key].append(link)
    _save_links(links_data)


def get_links_for_fill(index):
   
    links_data = _load_links()
    key = _key_for_fill(index)
    user_links = links_data.get(key, [])
    default_links = DEFAULT_FILL_LINKS.get(index, [])

    merged = list(default_links)
    for link in user_links:
        if link not in merged:
            merged.append(link)
    return merged


def add_link_for_fill(index, link):
    
    links_data = _load_links()
    key = _key_for_fill(index)
    links_data.setdefault(key, [])
    if link not in links_data[key]:
        links_data[key].append(link)
    _save_links(links_data)



def _get_option_text(options, correct_letter):
    
    correct_letter = correct_letter.strip().upper()
    for opt in options:
        if opt.strip().upper().startswith(correct_letter + "."):
            return opt
    return f"{correct_letter} (option text not found)"


def show_mcq_with_links(index):
    
    if not (1 <= index <= len(ALL_QUIZ_DATA)):
        print("Invalid MCQ number.")
        return

    q = ALL_QUIZ_DATA[index - 1]
    question = q["question"]
    options = q["options"]
    ans_letter = q["answer"]

    print("\n===== MCQ ANSWER & LINKS =====")
    print(f"Q{index}. {question}")
    for opt in options:
        print("   " + opt)

    correct_text = _get_option_text(options, ans_letter)
    print(f"\nCorrect answer: {ans_letter} -> {correct_text}")

    links = get_links_for_mcq(index)
    if links:
        print("\nReference link(s):")
        for i, link in enumerate(links, start=1):
            print(f"  {i}. {link}")
    else:
        print("\nNo reference links stored yet.")
    print("================================\n")


def show_fill_with_links(index):
    
    if not (1 <= index <= len(FILL_IN_QUIZ_DATA)):
        print("Invalid fill-in question number.")
        return

    q = FILL_IN_QUIZ_DATA[index - 1]
    question = q["question"]
    raw_answer = q["answer"]
    variants = [a.strip() for a in raw_answer.split("|")]

    print("\n===== FILL-IN ANSWER & LINKS =====")
    print(f"Q{index}. {question}")
    print("Accepted answer(s): " + " / ".join(variants))

    links = get_links_for_fill(index)
    if links:
        print("\nReference link(s):")
        for i, link in enumerate(links, start=1):
            print(f"  {i}. {link}")
    else:
        print("\nNo reference links stored yet.")
    print("==================================\n")



def links_menu():
    while True:
        print("\n====== ANSWER REFERENCE LINKS ======")
        print("1. View MCQ answer + links")
        print("2. Add a link to an MCQ answer")
        print("3. View fill-in answer + links")
        print("4. Add a link to a fill-in answer")
        print("5. Delete a link from an MCQ answer")
        print("0. Back to main quiz menu")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            print("\n--- MCQ Questions ---")
            for i, q in enumerate(ALL_QUIZ_DATA, start=1):
                print(f"{i}. {q['question']}")
            try:
                idx = int(input("Enter MCQ number: "))
                show_mcq_with_links(idx)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "2":
            print("\n--- MCQ Questions ---")
            for i, q in enumerate(ALL_QUIZ_DATA, start=1):
                print(f"{i}. {q['question']}")
            try:
                idx = int(input("Enter MCQ number to add link for: "))
                link = input("Enter reference link (URL or note): ").strip()
                if link:
                    add_link_for_mcq(idx, link)
                    print("Link added.")
                else:
                    print("Empty link, nothing saved.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "3":
            print("\n--- FILL-IN Questions ---")
            for i, q in enumerate(FILL_IN_QUIZ_DATA, start=1):
                print(f"{i}. {q['question']}")
            try:
                idx = int(input("Enter fill-in question number: "))
                show_fill_with_links(idx)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "4":
            print("\n--- FILL-IN Questions ---")
            for i, q in enumerate(FILL_IN_QUIZ_DATA, start=1):
                print(f"{i}. {q['question']}")
            try:
                idx = int(input("Enter fill-in question number to add link for: "))
                link = input("Enter reference link (URL or note): ").strip()
                if link:
                    add_link_for_fill(idx, link)
                    print("Link added.")
                else:
                    print("Empty link, nothing saved.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "5":
            print("\n--- MCQ Questions ---")
            for i, q in enumerate(ALL_QUIZ_DATA, start=1):
                print(f"{i}. {q['question']}")
            try:
                idx = int(input("Enter MCQ number to delete a link from: "))
                show_mcq_with_links(idx)
                user_links = _show_user_links_for_mcq(idx)
                if not user_links:
                    continue
                raw = input("Enter link number to delete (or paste exact link text): ").strip()
                if not raw:
                    print("Nothing entered. Cancelled.")
                    continue
                try:
                    num = int(raw)
                    ok, msg = delete_link_for_mcq(idx, num)
                except ValueError:
                    ok, msg = delete_link_for_mcq(idx, raw)

                print(msg)

            except ValueError:
                print("Please enter a valid number.")
        elif choice == "0":
            print("Returning to main quiz menu.")
            break
        else:
            print("Invalid choice. Please try again.")


def delete_link_for_mcq(index, link_or_number):

    links_data = _load_links()
    key = _key_for_mcq(index)

    user_links = links_data.get(key, [])
    if not user_links:
        return False, "No user-added links to delete for this MCQ."


    if isinstance(link_or_number, int):
        pos = link_or_number
        if pos < 1 or pos > len(user_links):
            return False, f"Invalid number. Enter 1 to {len(user_links)}."
        removed = user_links.pop(pos - 1)

        if user_links:
            links_data[key] = user_links
        else:
            links_data.pop(key, None)

        _save_links(links_data)
        return True, f"Deleted: {removed}"


    target = str(link_or_number).strip()
    if target in user_links:
        user_links.remove(target)

        if user_links:
            links_data[key] = user_links
        else:
            links_data.pop(key, None)

        _save_links(links_data)
        return True, f"Deleted: {target}"

    return False, "That link was not found in user-added links (defaults can't be deleted)."


def _show_user_links_for_mcq(index):
 
    links_data = _load_links()
    key = _key_for_mcq(index)
    user_links = links_data.get(key, [])

    if not user_links:
        print("\nNo user-added links stored for this MCQ yet.")
        return []

    print("\nUser-added link(s) for this MCQ:")
    for i, link in enumerate(user_links, start=1):
        print(f"  {i}. {link}")
    return user_links





if __name__ == "__main__":
    links_menu()
