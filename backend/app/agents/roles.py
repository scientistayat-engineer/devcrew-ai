"""Declarative definition of the 7 agents and their tasks."""

PIPELINE = ["analyst", "planner", "coder", "tester", "reviewer", "security", "reporter"]

ROLES = {
    "analyst": dict(
        role="Requirements Analyst", store_as="analysis",
        goal="Turn a vague request into precise, testable requirements.",
        backstory="A senior business analyst who spots missing details and edge cases.",
        task="Analyze this software requirement. List functional requirements, edge cases and assumptions.\n\nRequirement:\n{requirement}",
        output="A numbered list of requirements, edge cases and assumptions.",
    ),
    "planner": dict(
        role="Technical Planner", store_as="plan",
        goal="Create a clear, ordered implementation plan.",
        backstory="A staff engineer who breaks problems into small, buildable steps.",
        task="Create a step-by-step implementation plan for this Python project.\n\nRequirements:\n{analysis}",
        output="An ordered implementation plan with modules and functions.",
    ),
    "coder": dict(
        role="Python Developer", store_as="code",
        goal="Write clean, documented, working Python code.",
        backstory="A pragmatic Python developer who follows PEP 8 and writes docstrings.",
        task="Write complete, clean, documented Python code following this plan. Keep it compact: one file, at most about 120 lines, standard library only unless the requirement truly needs more. Return ONE fenced python code block.\n\nPlan:\n{plan}",
        output="One fenced python code block.",
    ),
    "tester": dict(
        role="QA Engineer", store_as="tests",
        goal="Write thorough pytest test cases.",
        backstory="A QA engineer who covers happy paths, edge cases and failures.",
        task="Write at most 8 focused pytest test cases for this code. Return ONE fenced python code block.\n\nCode:\n{code}",
        output="One fenced python code block with pytest tests.",
    ),
    "reviewer": dict(
        role="Code Reviewer", store_as="review",
        goal="Find bugs, risks and quality issues.",
        backstory="A meticulous reviewer who explains issues and suggests fixes.",
        task="Review the code and tests. List the issues as a numbered list (1., 2., ...), one short line each with a severity. Maximum 8 items.\n\nCode:\n{code}\n\nTests:\n{tests}",
        output="A prioritized list of issues with suggested fixes.",
    ),
    "security": dict(
        role="Security Auditor", store_as="security",
        goal="Find security weaknesses before they ship.",
        backstory="An application-security specialist focused on safe, defensive code.",
        task="Audit this code for security issues (input validation, file handling, injection, secrets). List the findings as a numbered list (1., 2., ...), one short line each with the fix. Maximum 6 items.\n\nCode:\n{code}",
        output="A list of security findings with recommended fixes.",
    ),
    "reporter": dict(
        role="Technical Writer", store_as="report",
        goal="Produce the final code and a clear development report.",
        backstory="A technical writer who summarizes engineering work for stakeholders.",
        task=("Produce the final deliverable in Markdown. Start with a SHORT report: Summary, Plan, test summary, issues found and fixed (brief lists, do not repeat long text). End with the FINAL improved Python code (apply the reviewer and security fixes) in ONE fenced python block as the very last part.\n\n"
              "Requirement:\n{requirement}\n\nPlan:\n{plan}\n\nCode:\n{code}\n\nTests:\n{tests}\n\n"
              "Review:\n{review}\n\nSecurity:\n{security}"),
        output="A Markdown development report containing the final code.",
    ),
}
