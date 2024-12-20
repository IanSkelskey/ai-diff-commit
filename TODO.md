# TODO

This document outlines the upcoming features and improvements for the `ai_diff_commit` script. Once entire features are implemented, I will move them to the [Completed Features](#completed-features) section. If the document becomes bloated, the oldest complete features will be removed from the list. The purpose of this document is to keep track of the progress and provide a roadmap for future development. This document is informal and may contain incomplete information.

## Upcoming Features:

-   [ ] Allow manual editing of commit messages before committing the changes.
-   [ ] If push is blocked due to branch protection rules, notify the user.
    -   Currently, the script just fails silently and displays a success message which is misleading.
-   [ ] Add option to select all files within a directory.
-   [ ] Option to generate a short commit message without a description. (One-liner)
-   [ ] If the remote branch does not exist, create it.
    -   i.e. set upstream to the remote branch. maybe just pass the actual git message from this to the user.
    -   Currently, the script fails silently if the remote branch does not exist and displays a success message which is misleading.
-   [ ] Add optional organization instructions.
    -   [ ] Project specific scope definitions and descriptions. e.g. `(backend)`: for backend changes, `(frontend)`: for frontend changes, etc.
    -   [ ] Any organization-specific instructions.
-   [ ] Add an easy way to quit the script.
-   [ ] OpenAI Assistant for generating commit messages.
-   [ ] Make a way to update the OpenAI API key.
    -   [x] If the key is invalid, prompt the user to update it.
    -   [ ] Add a flag to update/remove the key.
-   [x] Decide on a distribution method for the script: NPM
    -   [x] Publish the script to NPM.
    -   [ ] Create a release on GitHub?
-   [ ] Release the script to the public as an open-source project.
-   [ ] Accept donations for the project.
-   [ ] Add contribution guidelines.
-   [ ] Add branch protection rules.
-   [ ] Spaces in file names throw errors.
-   [ ] Reference [AICommits](https://github.com/Nutlope/aicommits) for inspiration.
    -   Study the release strategy.
    -   Study the documentation.
    -   Compare the features.

## Completed Features:

-   [x] Come up with a better name for the script.
    -   `ai_diff_commit` is too long.
        -   comgen
-   [x] Test branch protection rules.
-   [x] Create dev branch.
-   [x] Meet with Nate about collaboration.
-   [x] Add documentation for the script.
    -   [x] Write a README.md file.
    -   [x] Generate documentation using Sphinx or similar tool.
    -   [x] Deploy documentation to a website. (Probably GitHub Pages)
    -   [x] `-h` or `--help` flag to display help information for `ai_diff_commit`.
-   [x] Create a logo for the script.
-   [x] Add terminal arguments for customization.
    -   [x] Add argument for specifying the openai API language model.
    -   [x] Add argument for automatically pushing changes.
    -   [x] Add argument to automatically add all changes.
    -   [x] Add argument for help information.
-   [x] Make automated push optional.
-   [x] Allow the user to specify the files to include in the commit.
-   [x] Automate installation and setup process.
-   [x] Improve interface while still utilizing the command line for simplicity.
-   [x] Clear the terminal before each run.
-   [x] Notify the user of what branch they are on.
