
import json
from pathlib import Path
from datetime import datetime

from agent import run_agent
from semantic_grader import semantic_grade


# Project paths
BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "dataset.jsonl"
RESULTS_DIR = BASE_DIR / "results"

# Similarity threshold
SIMILARITY_THRESHOLD = 0.75


def run_evaluation():

    print("\nStarting Agent Evaluation...\n")

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    results = []

    # Read dataset
    with open(DATASET_PATH, "r", encoding="utf-8") as file:

        for index, line in enumerate(file, start=1):

            # Skip empty lines
            if not line.strip():
                continue

            try:
                test = json.loads(line)

            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON at line {index}: {error}"
                )

            if "input" not in test or "expected" not in test:
                raise ValueError(
                    f"Missing input or expected at line {index}"
                )

            question = test["input"]
            expected = test["expected"]

            print(f"\nRunning test case {index}...")

            # Generate actual response
            actual = run_agent(question)

            # Perform semantic grading
            grading = semantic_grade(
                expected=expected,
                actual=actual,
                threshold=SIMILARITY_THRESHOLD
            )

            status = grading["status"]

            print("Question:", question)
            print("Expected:", expected)
            print("Actual:", actual)
            print("Similarity:", grading["similarity_score"])
            print("Status:", status)

            # Store results
            results.append({
                "test_case": index,
                "question": question,
                "expected": expected,
                "actual": actual,
                "similarity_score": grading["similarity_score"],
                "threshold": grading["threshold"],
                "status": status
            })

    # Calculate evaluation metrics
    total_tests = len(results)

    passed_tests = sum(
        1 for result in results
        if result["status"] == "PASS"
    )

    failed_tests = total_tests - passed_tests

    accuracy = (
        (passed_tests / total_tests) * 100
        if total_tests > 0 else 0
    )

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    filename = datetime.now().strftime(
        "evaluation_%Y%m%d_%H%M%S.json"
    )

    output_path = RESULTS_DIR / filename

    report = {
        "total_tests": total_tests,
        "passed": passed_tests,
        "failed": failed_tests,
        "accuracy": round(accuracy, 2),
        "similarity_threshold": SIMILARITY_THRESHOLD,
        "results": results
    }

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    # Print summary
    print("\n========== EVALUATION SUMMARY ==========")

    print("Total tests:", total_tests)
    print("Passed:", passed_tests)
    print("Failed:", failed_tests)
    print(f"Accuracy: {accuracy:.2f}%")

    print("\nResults saved to:", output_path)


if __name__ == "__main__":
    run_evaluation()
