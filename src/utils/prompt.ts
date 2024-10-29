import inquirer from 'inquirer';
import chalk from 'chalk';
import fs from 'fs';
import path from 'path';

const colors: Record<string, (message: string) => string> = {
    info: chalk.blue,
    success: chalk.green,
    warning: chalk.yellow,
    error: chalk.red,
    content: chalk.grey
};

export async function confirmCommitMessage(commitMessage: string): Promise<boolean> {
    print('info', 'Commit message:');
    print('content', commitMessage);
    const answer = await inquirer.prompt({
        type: 'confirm',
        name: 'commit',
        message: `Do you want to commit with this message?`,
    });
    return answer.commit;
}

export async function requestFeedback(): Promise<string> {
    const answer = await inquirer.prompt({
        type: 'confirm',
        name: 'tryAgain',
        message: 'Would you like to provide feedback on the commit message and try again?',
    });
    if (!answer.tryAgain) {
        return '';
    }

    const feedbackAnswer = await inquirer.prompt({
        type: 'input',
        name: 'feedback',
        message: 'Please provide feedback:',
    });
    return feedbackAnswer.feedback;

}

export async function selectFilesToStage(files: string[]): Promise<string[]> {
    const answer = await inquirer.prompt({
        type: 'checkbox',
        name: 'files',
        message: 'Select files to stage:',
        choices: files,
    });
    return answer.files;
}

export async function selectCommitStandard(): Promise<{ name: string, rules: string }> {
    const rulesDir = path.resolve(__dirname, '../rules');
    const files = fs.readdirSync(rulesDir).filter(file => file.endsWith('.md'));
    const choices = files.map(file => file);

    const answer = await inquirer.prompt({
        type: 'list',
        name: 'standard',
        message: 'Select commit standard:',
        choices: choices,
    });

    const filename: string = answer.standard;
    const selectedFilePath = path.join(rulesDir, filename);
    const fileContents = fs.readFileSync(selectedFilePath, 'utf-8');
    return { name: filename, rules: fileContents };
}

export async function promptForAdditionalRequirement(name: string, description: string, datatype: string): Promise<string> {
    let answer: any;
    if (datatype === 'number') {
        answer = await inquirer.prompt({
            type: 'input',
            name: name,
            message: description,
        });
    } else if (datatype === 'string') {
        answer = await inquirer.prompt({
            type: 'input',
            name: name,
            message: description,
        });
    } else if (datatype === 'boolean') {
        answer = await inquirer.prompt({
            type: 'confirm',
            name: name,
            message: description,
        });
    } else {
        throw new Error(`Invalid datatype: ${datatype}`);
    }
    return answer[name];
}


export function showHelpMenu(): void {
    print('info', 'Usage: ai-diff-commit [options]');
    console.log('\nOptions:');
    console.log('  -m, --model <model>  Specify OpenAI model (default: gpt-4o)');
    console.log('                       Available models can be found at https://platform.openai.com/docs/models/');
    console.log('  -p, --push           Automatically push changes (default: false)');
    console.log('  -a, --add            Automatically add all changes (default: false)');
    console.log('  -h, --help           Display help for command');
}

export function print(type: string, message: string): void {
    if (type === 'error') {
        console.error(colors[type](message));
        return;
    } else if (type === 'warning') {
        console.warn(colors[type](message));
        return;
    } else if (!colors[type]) {
        throw new Error(`Invalid message type: ${type}`);
    }

    console.log(colors[type](message));
}
