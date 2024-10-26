import { execSync } from "child_process";

export function isInGitRepo(): boolean {
  try {
    execSync("git rev-parse --is-inside-work-tree", { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

export function getCurrentBranchName(): string {
  return execSync("git rev-parse --abbrev-ref HEAD").toString().trim();
}

export function hasGitChanges(): boolean {
  const status = execSync("git status --porcelain").toString().trim();
  return status.length > 0;
}
