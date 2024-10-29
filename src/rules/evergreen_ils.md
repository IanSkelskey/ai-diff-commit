# Evergreen ILS Commit Message Guidelines

As an AI, you are expected to generate commit messages for the Evergreen ILS project that adhere to the following structure and standards:

## Message Structure

1. **Subject Line**: A concise description of the change, ideally 60-70 characters, including a relevant Launchpad bug number if applicable (e.g., LP#1234).
2. **Blank Line**: Separate the subject line from the rest of the message.
3. **Detailed Description**: Optionally, provide additional context or details about the change, highlighting key modifications, new configurations, or added permissions.
4. **Release Note**: Begin a line with "Release-Note:" if a change merits mention in the release notes.
5. **Testing Plan**: Include steps for testers to validate the changes if necessary or reference the relevant Launchpad bug for more details.
6. **Sign-off(s)**: Conclude with one or more "Signed-off-by" lines, including the author and any reviewers.

## Commit Message Template

LP#bug_number: brief description of the change

Optional longer description of the change - Describe key changes made to code or configuration - Mention any relevant new configurations, permissions, or settings - Use a bulleted list for readability

Release-Note: present-tense summary of the fix or feature added

Signed-off-by: your name <your_email@example.com>

## Additional Rules

-   Use **present tense** for the Release-Note entry.
-   Ensure **testing steps** are clear if included.
-   Keep messages **brief and descriptive**, avoiding restating the code diff.
