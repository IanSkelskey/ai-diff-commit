import inquirer from "inquirer";
import chalk from "chalk";

// Create a map of chalk colors for different types of messages
const colors: Record<string, (message: string) => string> = {
	"info": chalk.blue,
	"success": chalk.green,
	"warning": chalk.yellow,
	"error": chalk.red
};

export async function confirmCommitMessage(commitMessage: string): Promise<boolean> {
	const answer = await inquirer.prompt({
		type: "confirm",
		name: "commit",
		message: `Do you want to commit with the following message?\n${commitMessage}`
	});
	return answer.commit;
}

export function print(type: string, message: string): void {
	if (type === "error") {
		console.error(colors[type](message));
		return;
	} else if (type === "warning") {
		console.warn(colors[type](message));
		return;
	} else if (!colors[type]) {
		throw new Error(`Invalid message type: ${type}`);
	}

	console.log(colors[type](message));
}