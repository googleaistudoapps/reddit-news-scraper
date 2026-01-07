import os

def export_report(content, filename="reddit_news_report.txt"):
    try:
        with open(filename, "w") as f:
            f.write(content)
        print(f"Report exported successfully to {filename}")
    except Exception as e:
        print(f"Error exporting report: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # If content is passed as a string (handling potential size limits)
        content = " ".join(sys.argv[1:])
    else:
        # Fallback/Default test
        content = "No summary content provided."
    
    export_report(content)
