import { setModel, analyzeDiffWithChatGpt } from "./utils/aiUtils";
import { isInGitRepo, hasGitChanges, getCurrentBranchName, getDiff, commitWithMessage } from "./utils/gitUtils";
import { confirmCommitMessage } from "./utils/promptUtils";
import { Command } from "commander";
import chalk from "chalk";

const program = new Command();

program
  .option("-m, --model <model>", "Specify OpenAI model", "gpt-4o")
  .option("-p, --push", "Automatically push changes", false)
  .option("-a, --add", "Automatically add all changes", false);

program.parse(process.argv);
const options = program.opts();

async function main() {
  setModel(options.model);

  if (!isInGitRepo()) {
    console.error(chalk.red("Error: This program must be run inside a Git repository."));
    process.exit(1);
  }

  if (!hasGitChanges()) {
    console.log(chalk.green("No changes to commit. Your working directory is clean."));
    return;
  }

  const branch = getCurrentBranchName();
  console.log(chalk.blue(`Current branch: ${branch}`));

  const diffString = getDiff();
  const commitMessage = await analyzeDiffWithChatGpt(diffString);

  if (commitMessage && await confirmCommitMessage(commitMessage)) {
    commitWithMessage(sanitizeCommitMessage(commitMessage));
    console.log(chalk.green("Changes committed successfully."));
  } else {
    console.log(chalk.yellow("Commit aborted."));
  }
}

function sanitizeCommitMessage(commitMessage: string): string {
  return commitMessage.replace(/"/g, '\\"');
}

main().catch((err) => {
  console.error("An error occurred:", err);
});