from email_analyzer import EmailTicketAnalyzer

def test_categorization():
    """Test the email categorization logic"""
    analyzer = EmailTicketAnalyzer()
    
    # Test cases
    test_cases = [
        ("Urgent system issue", "The system is down", "High Priority"),
        ("API integration help", "Need help with API setup", "Medium Priority"),
        ("Pricing question", "What are your rates?", "Low Priority"),
        ("Critical bug", "This is an emergency", "High Priority"),
        ("Login verification", "Cannot access my account", "Medium Priority")
    ]
    
    print("Testing Email Categorization:")
    print("=" * 40)
    
    for subject, body, expected in test_cases:
        result = analyzer.categorize_email(subject, body)
        status = "✓" if result == expected else "✗"
        print(f"{status} Subject: '{subject}' → {result} (Expected: {expected})")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_categorization()
