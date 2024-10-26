import { setModel, analyzeDiffWithChatGpt } from "./utils/aiUtils";
import { isInGitRepo, hasGitChanges, getCurrentBranchName } from "./utils/gitUtils";
import { confirmCommitMessage } from "./utils/promptUtils";
import { Command } from "commander";
import chalk from "chalk";
import { execSync } from "child_process";

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

  // Assuming this function is for getting a string representation of changes
  const diffString = execSync("git diff").toString();
  const commitMessage = await analyzeDiffWithChatGpt(diffString);

  if (commitMessage && await confirmCommitMessage(commitMessage)) {
    execSync(`git commit -am "${commitMessage}"`);
    console.log(chalk.green("Changes committed successfully."));
  } else {
    console.log(chalk.yellow("Commit aborted."));
  }
}

main().catch((err) => {
  console.error("An error occurred:", err);
});