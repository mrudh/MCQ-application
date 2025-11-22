from mcq import menu, take_quiz, print_results
from storage import load_scores, save_scores, check_high_score, load_custom_assessments, save_custom_assessments
from assessment import create_assessment

#Data
QUESTIONS = (
    "Which element has the chemical symbol 'O'? ",
    "Who developed the theory of relativity?: ",
    "What is the capital of France?: ",
    "Which organ in the human body is primarily responsible for pumping blood?: ",
    "How many continents are there on Earth?: ",
    "Which gas do plants absorb during photosynthesis?: ",
    "What is the hardest natural substance on Earth?: ",
    "Which planet is known as the Red Planet?: ",
    "What is the process by which a caterpillar becomes a butterfly called?: ",
    "Who painted the Mona Lisa?: ",
    "What is the boiling point of water at sea level (in °C)?: ",
    "Which metal is liquid at room temperature?: ",
    "Which is the smallest prime number?: ",
    "Who was the first person to step on the Moon?: ",
    "Which country is known as the Land of the Rising Sun?: ",
    "What is the largest mammal in the world?: ",
    "Which planet has the most moons?: ",
)

OPTIONS = (
    ("A. Gold", "B. Oxygen", "C. Osmium", "D. Ozone"),
    ("A. Isaac Newton", "B. Albert Einstein", "C. Galileo Galilei", "D. Stephen Hawking"),
    ("A. Rome", "B. Madrid", "C. Paris", "D. Berlin"),
    ("A. Brain", "B. Liver", "C. Heart", "D. Kidney"),
    ("A. 5", "B. 6", "C. 7", "D. 8"),
    ("A. Oxygen", "B. Carbon-Dioxide", "C. Nitrogen", "D. Helium"),
    ("A. Graphite", "B. Diamond", "C. Iron", "D. Quartz"),
    ("A. Earth", "B. Venus", "C. Mars", "D. Jupiter"),
    ("A. Hibernation", "B. Metamorphosis", "C. Photosynthesis", "D. Germination"),
    ("A. Leonardo da Vinci", "B. Michelangelo", "C. Pablo Picasso", "D. Vincent van Gogh"),
    ("A. 50°C", "B. 90°C", "C. 100°C", "D. 120°C"),
    ("A. Mercury", "B. Gallium", "C. Sodium", "D. Lead"),
    ("A. 0", "B. 1", "C. 2", "D. 3"),
    ("A. Yuri Gagarin", "B. Neil Armstrong", "C. Buzz Aldrin", "D. Alan Shepard"),
    ("A. Japan", "B. China", "C. Thailand", "D. Korea"),
    ("A. Elephant", "B. Blue Whale", "C. Giraffe", "D. Orca"),
    ("A. Earth", "B. Saturn", "C. Jupiter", "D. Neptune"),
)

ANSWERS = (
    "B", "B", "C", "C", "C", "B", "B",
    "C", "B", "A", "C", "A", "C", "B", "A", "B", "B"
)

DIFFICULTY_QUESTIONS = {
    "Easy": [
        ("What is the capital of France?: ",
         ("A. Rome", "B. Madrid", "C. Paris", "D. Berlin"), "C"),
        ("Which organ in the human body is primarily responsible for pumping blood?: ",
         ("A. Brain", "B. Liver", "C. Heart", "D. Kidney"), "C"),
        ("Which element has the chemical symbol 'O'?: ",
         ("A. Gold", "B. Oxygen", "C. Osmium", "D. Ozone"), "B"),
        ("How many continents are there on Earth?: ",
         ("A. 5", "B. 6", "C. 7", "D. 8"), "C"),
        ("What is the boiling point of water at sea level (in °C)?: ",
         ("A. 50°C", "B. 90°C", "C. 100°C", "D. 120°C"), "C"),
        ("What color are bananas when they are ripe?: ",
         ("A. Red", "B. Green", "C. Yellow", "D. Purple"), "C"),
        ("Which animal is known as man's best friend?: ",
         ("A. Cat", "B. Dog", "C. Horse", "D. Rabbit"), "B"),
        ("How many legs does a spider have?: ",
         ("A. 6", "B. 8", "C. 10", "D. 12"), "B"),
    ],
    "Medium": [
        ("What is the most abundant gas in Earth's atmosphere?: ",
         ("A. Nitrogen", "B. Oxygen", "C. Carbon-Dioxide", "D. Hydrogen"), "A"),
        ("Who painted the Mona Lisa?: ",
         ("A. Leonardo da Vinci", "B. Michelangelo", "C. Pablo Picasso", "D. Vincent van Gogh"), "A"),
        ("Which planet is known as the Red Planet?: ",
         ("A. Earth", "B. Venus", "C. Mars", "D. Jupiter"), "C"),
        ("Which planet has the most moons?: ",
         ("A. Earth", "B. Saturn", "C. Jupiter", "D. Neptune"), "C"),
        ("Which metal is liquid at room temperature?: ",
         ("A. Mercury", "B. Gallium", "C. Sodium", "D. Lead"), "A"),
        ("What is the chemical symbol for Gold?: ",
         ("A. Ag", "B. Au", "C. Go", "D. Gd"), "B"),
        ("Which planet is known for its rings?: ",
         ("A. Jupiter", "B. Saturn", "C. Neptune", "D. Uranus"), "B"),
        ("What is the powerhouse of the cell?: ",
         ("A. Nucleus", "B. Ribosome", "C. Mitochondria", "D. Cytoplasm"), "C"),
    ],
    "Hard": [
        ("Which planet in the solar system is the hottest?: ",
         ("A. Mercury", "B. Venus", "C. Earth", "D. Mars"), "B"),
        ("What is the largest ocean on Earth?: ",
         ("A. Atlantic Ocean", "B. Indian Ocean", "C. Arctic Ocean", "D. Pacific Ocean"), "D"),
        ("Who developed the theory of relativity?: ",
         ("A. Isaac Newton", "B. Albert Einstein", "C. Galileo Galilei", "D. Stephen Hawking"), "B"),
        ("Which gas do plants absorb during photosynthesis?: ",
         ("A. Oxygen", "B. Carbon-Dioxide", "C. Nitrogen", "D. Helium"), "B"),
        ("What is the hardest natural substance on Earth?: ",
         ("A. Graphite", "B. Diamond", "C. Iron", "D. Quartz"), "B"),
        ("What is the largest internal organ in the human body?: ",
         ("A. Heart", "B. Liver", "C. Lungs", "D. Kidney"), "B"),
        ("Which scientist proposed the three laws of motion?: ",
         ("A. Albert Einstein", "B. Isaac Newton", "C. Galileo Galilei", "D. Nikola Tesla"), "B"),
        ("What is the most abundant element in the universe?: ",
         ("A. Oxygen", "B. Carbon", "C. Hydrogen", "D. Helium"), "C"),
    ],
}

def main():
    while True:
        menu()
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
        if choice == 1:
            name = input("Enter your name: ")
            take_quiz(QUESTIONS, OPTIONS, ANSWERS, name)
        elif choice == 2:
            check_high_score()
        elif choice == 4:
            create_assessment()
        elif choice == 7:  
            quiz_by_difficulty(DIFFICULTY_QUESTIONS)
        elif choice == 8:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
