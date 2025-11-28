from tools.code_generator import UniversalCodeGenerator


def test_generator():
    print("Initializing UniversalCodeGenerator...")
    generator = UniversalCodeGenerator()
    
    category = "business"
    use_case = "Project Budget Tracker"
    variables = {"project_name": "New HQ Build", "budget": "$50M"}
    
    print(f"\nTesting generation for: {use_case}")
    result = generator.generate(category, use_case, variables)
    
    print("\n--- Result ---")
    print(f"Draft: {result.draft}")
    print(f"Review Score: {result.review['score']}")
    print(f"Refined: {result.final}")
    
    assert result.review['score'] == 88
    assert "Refined content based on feedback" in result.final
    assert "Tip #4 is generic" in result.final or "Make Tip #4 specific" in str(result.final)
    print("\n✅ Test Passed!")


if __name__ == "__main__":
    test_generator()
