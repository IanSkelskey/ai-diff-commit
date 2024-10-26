import { setModel, analyzeDiffWithChatGpt } from "./utils/aiUtils";
import { isInGitRepo, hasGitChanges, getCurrentBranchName, getDiff, commitWithMessage } from "./utils/gitUtils";
import { confirmCommitMessage, print } from "./utils/promptUtils";
import { Command } from "commander";

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
    print("error", "Not in a git repository.");
    process.exit(1);
  }

  if (!hasGitChanges()) {
    print("warning", "No changes detected.");
    return;
  }

  const branch = getCurrentBranchName();
  print("info", `Current branch: ${branch}`);

  const diffString = getDiff();
  const commitMessage = await analyzeDiffWithChatGpt(diffString);

  if (commitMessage && await confirmCommitMessage(commitMessage)) {
    commitWithMessage(sanitizeCommitMessage(commitMessage));
    print("success", "Commit successful.");
  } else {
    print("warning", "Commit aborted.");
  }
}

function sanitizeCommitMessage(commitMessage: string): string {
  return commitMessage.replace(/"/g, '\\"');
}

main().catch((err) => {
  console.error("An error occurred:", err);
});