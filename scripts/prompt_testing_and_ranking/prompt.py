from typing import Optional

class Prompt:
    def __init__(self, text: str):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text must be a non-empty string.")
        self.text = text
        self.elo_rating = 1000  # Starting ELO rating
        self.metadata = {}  # Additional metadata storage

    def __repr__(self):
        return f"Prompt({self.text[:30]}... ELO: {self.elo_rating})"

    def update_elo(self, new_rating: float):
        if not isinstance(new_rating, (int, float)):
            raise ValueError("New rating must be a number.")
        self.elo_rating = new_rating

    def add_metadata(self, key: str, value: Optional[str]):
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Metadata key must be a non-empty string.")
        self.metadata[key] = value

    def get_metadata(self, key: str) -> Optional[str]:
        return self.metadata.get(key)

# Example usage
if __name__ == "__main__":
    prompt = Prompt("Generate a summary for the business need section.")
    prompt.add_metadata("category", "summary")
    print(prompt)
    print("Metadata:", prompt.get_metadata("category"))
    prompt.update_elo(1200)
    print("Updated Prompt:", prompt)
