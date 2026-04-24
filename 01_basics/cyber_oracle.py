# cyber_oracle.py
import random
import time

def ask_the_oracle():
    print("--- 🔮 Cyber Oracle ---")
    input("Enter your question for the universe: ")
    
    # Simulating a quantum calculation delay for cyberpunk effect
    print("Consulting the quantum realm", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("\n")
    
    # Geek-exclusive answer database
    answers = [
        "42. (The answer to life, the universe, and everything)", 
        "The compiler says YES.", 
        "Segmentation Fault. Try again.", 
        "Trust the math, go for it.",
        "Warning: Infinite loop ahead, reconsider.",
        "Git commit and push it immediately!"
    ]
    
    print(f"Oracle says: {random.choice(answers)}")

if __name__ == "__main__":
    ask_the_oracle()