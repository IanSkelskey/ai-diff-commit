import { OpenAI } from 'openai';
import { print } from './promptUtils';
import { readFileSync } from 'fs';
import { join } from 'path';

let MODEL = 'gpt-4o';
const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const systemPromptPath = join(__dirname, '../../lib/rules/conventional_commits.md');
const systemPrompt = readFileSync(systemPromptPath, 'utf-8');

export function setModel(modelName: string): void {
	MODEL = modelName;
}

export async function generateCommitMessage(diffString: string): Promise<string | null> {
	if (!process.env.OPENAI_API_KEY) {
		print('error', 'OpenAI API key not found. Please set it in the OPENAI_API_KEY environment variable.');
		return null;
	}
	try {
		const completion = await client.chat.completions.create({
			model: MODEL,
			messages: [
				{
					role: 'system',
					content: systemPrompt,
				},
				{ role: 'user', content: diffString },
			],
		});
		return completion.choices[0]?.message?.content?.trim() || null;
	} catch (error: any) {
		print('error', `An error occurred while generating commit message: ${(error as Error).message}`);
		return null;
	}
}
