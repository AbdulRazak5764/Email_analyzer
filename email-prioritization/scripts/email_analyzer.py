import re
from collections import Counter
from typing import Dict, List, Tuple

class EmailTicketAnalyzer:
    def __init__(self):
        # Define priority keywords
        self.high_priority_keywords = ['urgent', 'critical', 'immediate', 'emergency', 'blocked', 'down', 'outage']
        self.medium_priority_keywords = ['verification', 'login', 'api', 'integration', 'access', 'authentication', 'account']
        
    def categorize_email(self, subject: str, body: str) -> str:
        """Categorize email based on subject and body content"""
        text = (subject + " " + body).lower()
        
        # Check for high priority keywords
        for keyword in self.high_priority_keywords:
            if keyword in text:
                return "High Priority"
        
        # Check for medium priority keywords
        for keyword in self.medium_priority_keywords:
            if keyword in text:
                return "Medium Priority"
        
        # Default to low priority
        return "Low Priority"
    
    def parse_email_data(self, data: str) -> List[Dict]:
        """Parse email data from text format"""
        emails = []
        lines = data.strip().split('\n')
        
        current_email = {}
        current_field = None
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_email:
                    emails.append(current_email)
                    current_email = {}
                continue
            
            if line.startswith('From:'):
                current_email['sender'] = line.replace('From:', '').strip()
                current_field = 'sender'
            elif line.startswith('Subject:'):
                current_email['subject'] = line.replace('Subject:', '').strip()
                current_field = 'subject'
            elif line.startswith('Body:'):
                current_email['body'] = line.replace('Body:', '').strip()
                current_field = 'body'
            else:
                # Continue previous field if it's multi-line
                if current_field and current_field in current_email:
                    current_email[current_field] += " " + line
        
        # Add the last email if exists
        if current_email:
            emails.append(current_email)
        
        return emails
    
    def analyze_tickets(self, email_data: str) -> Dict:
        """Analyze email tickets and return priority counts and frequent sender"""
        emails = self.parse_email_data(email_data)
        
        priority_counts = {"High Priority": 0, "Medium Priority": 0, "Low Priority": 0}
        sender_counts = Counter()
        
        for email in emails:
            if 'subject' in email and 'body' in email and 'sender' in email:
                priority = self.categorize_email(email['subject'], email['body'])
                priority_counts[priority] += 1
                sender_counts[email['sender']] += 1
        
        # Find most frequent sender
        most_frequent_sender = sender_counts.most_common(1)[0] if sender_counts else ("None", 0)
        
        return {
            "priority_counts": priority_counts,
            "most_frequent_sender": most_frequent_sender,
            "total_emails": len(emails)
        }
    
    def generate_report(self, analysis_results: Dict) -> str:
        """Generate formatted report"""
        priority_counts = analysis_results["priority_counts"]
        sender, count = analysis_results["most_frequent_sender"]
        
        report = f"""Email Support Ticket Analysis Report
==========================================
High Priority Tickets: {priority_counts['High Priority']}
Medium Priority Tickets: {priority_counts['Medium Priority']}
Low Priority Tickets: {priority_counts['Low Priority']}
Most Frequent Sender: {sender} ({count} tickets)
Total Emails Processed: {analysis_results['total_emails']}
"""
        return report

# Example usage and test
def main():
    analyzer = EmailTicketAnalyzer()
    
    # Sample email data for testing
    sample_data = """
From: user1@example.com
Subject: Urgent: System is down
Body: Our entire system is not accessible. This is critical for our business operations.

From: user2@example.com
Subject: API Integration Question
Body: I need help with integrating your API into our application. Can you provide documentation?

From: user1@example.com
Subject: Pricing inquiry
Body: What are your subscription plans and pricing options?

From: user3@example.com
Subject: Login verification issue
Body: I cannot verify my account and login to the system. Please help.

From: user2@example.com
Subject: Immediate assistance needed
Body: We are experiencing critical issues with our account access.
"""
    
    print("Analyzing sample email data...")
    results = analyzer.analyze_tickets(sample_data)
    report = analyzer.generate_report(results)
    print(report)
    
    # To use with your actual data file, uncomment and modify:
    # with open('path_to_your_email_data.txt', 'r') as file:
    #     email_data = file.read()
    #     results = analyzer.analyze_tickets(email_data)
    #     report = analyzer.generate_report(results)
    #     print(report)

if __name__ == "__main__":
    main()
