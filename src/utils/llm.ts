import { OpenAI } from 'openai';
import { print } from './prompt';

let MODEL = 'gpt-4o';
const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export function setModel(modelName: string): void {
	MODEL = modelName;
}

export async function createTextGeneration(system_prompt: string, user_prompt: string): Promise<string | null> {
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
					content: system_prompt,
				},
				{ role: 'user', content: user_prompt },
			],
		});
		return completion.choices[0]?.message?.content?.trim() || null;
	} catch (error: any) {
		print('error', `An error occurred while generating text: ${(error as Error).message}`);
		return null;
	}
}