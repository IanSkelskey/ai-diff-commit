# TODO

This document outlines the upcoming features and improvements for the `ai_diff_commit` script. Once entire features are implemented, I will move them to the [Completed Features](#completed-features) section. If the document becomes bloated, the oldest complete features will be removed from the list. The purpose of this document is to keep track of the progress and provide a roadmap for future development. This document is informal and may contain incomplete information.

## Upcoming Features:

- [ ] Allow manual editing of commit messages before committing the changes.
- [ ] Add support for Linux and macOS.
- [ ] Add terminal arguments for customization.
  - [ ] Add argument for specifying the openai API language model.
  - [x] Add argument for automatically pushing changes.
  - [x] Add argument to automatically add all changes.
  - [ ] Add argument for help information.
- [ ] Add documentation for the script.
  - [x] Write a README.md file.
  - [ ] Generate documentation using Sphinx or similar tool.
  - [ ] Deploy documentation to a website. (Probably GitHub Pages)
  - [ ] `-h` or `--help` flag to display help information for `ai_diff_commit`.
- [ ] Add option to select all files within a directory.
- [ ] If the remote branch does not exist, create it.
  - i.e. set upstream to the remote branch. maybe just pass the actual git message from this to the user.
- [ ] Add optional organization instructions.
  - [ ] Project specific scope definitions and descriptions. e.g. `(backend)`: for backend changes, `(frontend)`: for frontend changes, etc.
  - [ ] Any organization-specific instructions.

## Completed Features:

- [x] Make automated push optional.
- [x] Allow the user to specify the files to include in the commit.
- [x] Automate installation and setup process.
- [x] Improve interface while still utilizing the command line for simplicity.
- [x] Clear the terminal before each run.
- [x] Notify the user of what branch they are on.