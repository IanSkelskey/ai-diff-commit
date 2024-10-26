import inquirer from "inquirer";

export async function confirmCommitMessage(commitMessage: string): Promise<boolean> {
  const answer = await inquirer.prompt({
    type: "confirm",
    name: "commit",
    message: `Do you want to commit with the following message?\n${commitMessage}`
  });
  return answer.commit;
}
