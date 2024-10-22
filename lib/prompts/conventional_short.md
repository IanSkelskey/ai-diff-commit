# Conventional Commits Short Prompt

## Purpose
This prompt is designed to provide guidance on writing concise commit messages following the Conventional Commits specification. The focus is on brevity while still communicating the intent and nature of the changes.

## Structure of a Short Commit Message
- **Format**: `<type>[optional scope]: <brief description>`
- **Types**: Choose from `feat`, `fix`, `docs`, `chore`, `style`, `refactor`, `test`, `perf`, etc.
- **Scope (optional)**: A noun that describes the section of the codebase (e.g., parser, API).
- **Brief Description**: A concise statement, ideally under 50 characters, summarizing the change.

### Example Guidelines:
- Start with a type and a colon (`:`).
- Optionally add a scope in parentheses, followed by a colon (`:`).
- Use a brief, present-tense description.
- Avoid overly long descriptions or explanations in the commit message.

### Example Output

fix: resolve login error

feat(auth): add user validation

## Tips for Short Conventional Commits
- Keep the subject line under 50 characters if possible.
- Avoid using conjunctions to combine multiple changes into one message.
- Ensure the message concisely captures the essence of the change.

