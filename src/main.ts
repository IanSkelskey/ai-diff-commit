import { setModel, generateCommitMessage } from "./utils/aiUtils";
import { isInGitRepo, hasGitChanges, getCurrentBranchName, getDiffForStagedFiles, commitWithMessage, pushChanges, listChangedFiles, addAllChanges, stageFile, unstageAllFiles } from "./utils/gitUtils";
import { confirmCommitMessage, print, showHelpMenu, selectFilesToStage } from "./utils/promptUtils";
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

	await handleStagingOptions();

	const diff = getDiffForStagedFiles();

	const commitMessage = await generateCommitMessage(diff);

	await executeCommitWorkflow(commitMessage);
}

async function executeCommitWorkflow(commitMessage: string | null) {
	if (commitMessage && await confirmCommitMessage(commitMessage)) {
		commitWithMessage(commitMessage);
		print("success", "Commit successful.");
		if (options.push) {
			pushChanges();
			print("success", "Push successful.");
		}
	} else {
		unstageAllFiles();
		print("warning", "Commit aborted.");
	}
}

async function handleStagingOptions() {
	if (options.add) {
		print("info", "Adding all changes...");
		addAllChanges();
		print("success", "Add successful.");
	} else {
		const changedFiles = listChangedFiles();
		const filesToStage = await selectFilesToStage(changedFiles);
		filesToStage.forEach(stageFile);
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

main().catch((err) => {
	console.error("An error occurred:", err);
});