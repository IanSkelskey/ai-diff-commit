import { OpenAI } from "openai";

let MODEL = "gpt-4o";
const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY || "" });

export function setModel(modelName: string): void {
  MODEL = modelName;
}

export async function generateCommitMessage(diffString: string): Promise<string | null> {
  try {
    const completion = await client.chat.completions.create({
      model: MODEL,
      messages: [
        { role: "system", content: "Provide a concise commit message based on the following diff:" },
        { role: "user", content: diffString }
      ]
    });
    return completion.choices[0]?.message?.content?.trim() || null;
  } catch (error) {
    console.error("Error generating commit message:", error);
    return null;
  }
}
