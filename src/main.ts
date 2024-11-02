#!/usr/bin/env node

import { setModel, createTextGeneration } from './utils/llm';
import {
    isInGitRepo,
    hasGitChanges,
    getCurrentBranchName,
    getDiffForStagedFiles,
    commitWithMessage,
    pushChanges,
    listChangedFiles,
    addAllChanges,
    stageFile,
    unstageAllFiles,
    getName,
    getEmail,
    setupUpstreamBranch,
} from './utils/git';
import {
    confirmCommitMessage,
    print,
    showHelpMenu,
    selectFilesToStage,
    selectCommitStandard,
    promptForAdditionalRequirement,
    requestFeedback,
} from './utils/prompt';
import { Command } from 'commander';
import * as fs from 'fs';
import * as path from 'path';

const program = new Command();

program
    .option('-m, --model <model>', 'Specify OpenAI model', 'gpt-4o')
    .option('-p, --push', 'Automatically push changes', false)
    .option('-a, --add', 'Automatically add all changes', false)
    .option('-h, --help', 'Display help for command');

program.parse(process.argv);
const options = program.opts();

async function main() {
    if (options.help) {
        showHelpMenu();
        return;
    }

    setModel(options.model);

    if (!validateWorkingDirectory()) {
        return;
    }

    try {
        const branch = getCurrentBranchName();
        print('info', `Current branch: ${branch}`);
    } catch (error: any) {
        print('error', error.message);
    }

    await handleStagingOptions();

    const diff = getDiffForStagedFiles();

    const { name, rules } = await selectCommitStandard();

    let systemPrompt: string = rules;

    const additionalRequirements = getRequiredFieldsFromStandard(name);

    if (additionalRequirements.length > 0) {
        systemPrompt += '\n\nAdditional information to include in commit: ';
    }

    for (const requirement of additionalRequirements) {
        let answer;
        if (requirement.name.toLowerCase() === 'name') {
            answer = getName();
        } else if (requirement.name.toLowerCase() === 'email') {
            answer = getEmail();
        } else {
            answer = await promptForAdditionalRequirement(requirement.name, requirement.description, requirement.type);
        }
        systemPrompt += `\n${requirement.name}: ${answer}`;
    }

    await executeCommitWorkflow(systemPrompt, diff);

    print('info', 'Exiting...');

    process.exit(0);
}

function getRequiredFieldsFromStandard(standardName: string): any[] {
    const rulesPath = path.join(__dirname, 'rules', 'rules.json');
    const rules = JSON.parse(fs.readFileSync(rulesPath, 'utf-8'));
    const standard = rules[standardName];
    if (!standard) {
        throw new Error(`Standard ${standardName} not found.`);
    }
    return standard.required;
}

async function executeCommitWorkflow(systemPrompt: string, diff: string) {
    let commitMessage = await createTextGeneration(systemPrompt, diff);

    if (!commitMessage) {
        print('error', 'Commit message generation is empty. Aborting commit.');
        process.exit(1);
    }

    let confirmed = false;
    while (!confirmed) {
        confirmed = await confirmCommitMessage(commitMessage);
        if (!confirmed) {
            const feedback = await requestFeedback();
            if (feedback === '') {
                unstageAllFiles();
                print('warning', 'Commit aborted.');
                return;
            }
            const feedbackMessage: string =
                'Standards:\n' + systemPrompt + 'Commit message:\n' + commitMessage + '\nFeedback:\n' + feedback;
            commitMessage = await createTextGeneration(
                'Please revise the commit message according to the feedback.',
                feedbackMessage,
            );
            if (!commitMessage) {
                print('error', 'Commit message generation is empty after feedback. Aborting commit.');
                process.exit(1);
            }
        }
    }

    commitWithMessage(commitMessage);
    print('success', 'Commit successful.');

    if (options.push) {
        try {
            pushChanges();
            print('success', 'Push successful.');
        } catch (error: any) {
            if (error.message.includes('The current branch has no upstream branch.')) {
                setupUpstreamBranch();
            }
        }

        print('success', 'Push successful.');
    }
}

async function handleStagingOptions() {
    if (options.add) {
        print('info', 'Adding all changes...');
        addAllChanges();
        print('success', 'Add successful.');
    } else {
        const changedFiles = listChangedFiles();
        const filesToStage = await selectFilesToStage(changedFiles);
        filesToStage.forEach(stageFile);
    }
}

function validateWorkingDirectory(): boolean {
    if (!isInGitRepo() || !hasGitChanges()) {
        print('error', !isInGitRepo() ? 'Not in a git repository.' : 'No changes detected.');
        return false;
    }
    return true;
}

main().catch((err) => {
    console.error('An error occurred:', err);
});
