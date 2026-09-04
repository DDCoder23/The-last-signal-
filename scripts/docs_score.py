from documentation.score import generate_score

if __name__ == "__main__":
    score = generate_score()
    if score < 0:
        score = 0
    print(f"Documentation score : {score}/100")
