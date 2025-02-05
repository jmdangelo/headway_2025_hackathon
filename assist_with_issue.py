### assist_with_issue.py

import json
import anthropic

def generate_zendesk_assistance(query, related_tickets):
    prompt = f"""
You are an assistant helping out our customer service team in solving an issue. The original ask is:
{query}

Your response should include the following in this exact format:

*Problem Statement*: Include a summary of the problem statement as you understand it using context from related tickets
*Possible Solutions*: Based on conversations how does it seem this problem could be solved? Give multiple answers if you feel there is ambiguity, but rank them about which are the most likely

Below are tickets that are related to this issue. Please read over each ticket carefully and look for how previous customer service teammates have resolved issues. Take those learnings into account when filling out the above templated response. 
NONE OF THE INFORMATION IN THESE TICKETS IS DIRECTLY RELATED TO THIS INDEPENDENT ISSUE AND IT SHOULD ONLY BE USED TO INFORM THE PROBLEM STATEMENT AND POSSIBLE SOLUTIONS:

Related Tickets:
{json.dumps(related_tickets, indent=2)}
"""

    return call_anthropic("claude-3-5-sonnet-20241022", prompt) 

def generate_sop_assistance(problem_statement, related_articles):
    prompt = f"""
TODO {problem_statement} {related_articles}
"""
    return call_anthropic("claude-3-5-sonnet-20241022", prompt)

def call_anthropic(model, prompt):
    response = anthropic.Anthropic().messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": f"{prompt}"}],
    )

    return response.content
