# Evergreen ILS Commit Message Guidelines

As a developer committing changes to Evergreen ILS, adhere to these guidelines to create clear, concise, and informative commit messages that meet project standards. Follow these rules to ensure your messages are consistent, easy to understand, and appropriately documented.

## Commit Message Structure

### Subject Line (mandatory)

- Start with the relevant Launchpad bug number if available, e.g., `LP#12345:`.
- Provide a concise description of the change, ideally no more than 60-70 characters.
- Use present tense verbs, like "Fix," "Add," "Update," etc.

### Body (optional but recommended)

- Separate the subject line from the body with a blank line.
- Describe the changes made, using bullet points or paragraphs.
- Specify affected files or components.
- Include relevant settings or permissions changes.
- If detailed explanation is needed, provide a testing plan or additional context.

### Release Note Tag

- If the change warrants a release note, include a line starting with `Release-Note:` followed by the description in present tense.

### Sign-offs (mandatory)

- Every commit must be signed off with your name and email using the `Signed-off-by:` format. Example: `Signed-off-by: John Doe <johndoe@example.com>`

## Example 1: Simple Fix

LP#12345: fix item renewal bug

Release-Note: Fixes an issue where auto-renewals fail for overdue items.

Signed-off-by: Jane Hacker jhacker@example.org


## Example 2: More Detailed Commit

LP#987: extend reporting feature

Add support for custom filters in the reporting module. Implements the following settings:

report.custom.filter
report.admin.view
Adds the following permissions:

VIEW_REPORTS
UPDATE_REPORTS
See LP bug report for testing plan.

Signed-off-by: Jane Hacker jhacker@example.org Signed-off-by: Chris Committer chris@example.net


## Additional Notes

- **Use present tense** for the `Release-Note` tag and commit messages.
- If further detail is needed, consider using the `docs/RELEASE_NOTES_NEXT/miscellaneous.adoc` file for long-form release notes.
- Each commit must include all sign-offs to confirm code quality and submission consent.

Follow these guidelines to create well-structured commit messages that meet the Evergreen ILS project's standards and facilitate smooth code review and release processes.
