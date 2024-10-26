import inquirer from 'inquirer';
import chalk from 'chalk';

const colors: Record<string, (message: string) => string> = {
    info: chalk.blue,
    success: chalk.green,
    warning: chalk.yellow,
    error: chalk.red,
};

export async function confirmCommitMessage(commitMessage: string): Promise<boolean> {
    const answer = await inquirer.prompt({
        type: 'confirm',
        name: 'commit',
        message: `Do you want to commit with the following message?\n${commitMessage}`,
    });
    return answer.commit;
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

export function showHelpMenu(): void {
    print('info', 'Usage: ai-commit [options]');
    console.log('\nOptions:');
    console.log('  -m, --model <model>  Specify OpenAI model (default: gpt-4o)');
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
