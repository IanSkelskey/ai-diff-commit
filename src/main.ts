import { setModel, generateCommitMessage } from "./utils/aiUtils";
import { isInGitRepo, hasGitChanges, getCurrentBranchName, getDiff, commitWithMessage } from "./utils/gitUtils";
import { confirmCommitMessage, print, showHelpMenu } from "./utils/promptUtils";
import { Command } from "commander";

const program = new Command();

program
	.option("-m, --model <model>", "Specify OpenAI model", "gpt-4o")
	.option("-p, --push", "Automatically push changes", false)
	.option("-a, --add", "Automatically add all changes", false)
	.option("-h, --help", "Display help for command");

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

	const branch = getCurrentBranchName();
	print("info", `Current branch: ${branch}`);

	const diffString = getDiff();
	const commitMessage = await generateCommitMessage(diffString);

	if (commitMessage && await confirmCommitMessage(commitMessage)) {
		commitWithMessage(sanitizeCommitMessage(commitMessage));
		print("success", "Commit successful.");
	} else {
		print("warning", "Commit aborted.");
	}
}

function validateWorkingDirectory(): boolean {
	if (!isInGitRepo()) {
		print("error", "Not in a git repository.");
		return false;
	}

	if (!hasGitChanges()) {
		print("warning", "No changes detected.");
		return false;
	}

	return true;
}

function sanitizeCommitMessage(commitMessage: string): string {
	return commitMessage.replace(/"/g, '\\"');
}

main().catch((err) => {
	console.error("An error occurred:", err);
});