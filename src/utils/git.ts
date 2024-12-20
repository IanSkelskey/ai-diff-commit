import { execSync } from 'child_process';

export enum GitFileStatus {
    'A' = 'Added',
    'M' = 'Modified',
    'D' = 'Deleted',
    'R' = 'Renamed',
    'C' = 'Copied',
    'U' = 'Unmerged',
    '?' = 'Untracked',
    '!' = 'Ignored',
}

export function isInGitRepo(): boolean {
    try {
        execSync('git rev-parse --is-inside-work-tree', { stdio: 'ignore' });
        return true;
    } catch {
        return false;
    }
}

export function pushChanges(): void {
    try {
        execSync('git push');
    } catch (error: any) {
        if (error.message.includes('fatal: The current branch')) {
            throw new Error('The current branch has no upstream branch.');
        }
    }
}

export function setupUpstreamBranch() {
    const branchName = getCurrentBranchName();
    execSync(`git push --set-upstream origin ${branchName}`);
}

export function addAllChanges(): void {
    execSync('git add .');
}

export function stageFile(filePath: string): void {
    execSync(`git add ${filePath}`);
}

export function unstageFile(filePath: string): void {
    execSync(`git restore --staged ${filePath}`);
}

export function unstageAllFiles(): void {
    execSync('git restore --staged .');
}

export function listChangedFiles(): string[] {
    const statusOutput = execSync('git status --porcelain').toString().trim();
    return statusOutput
        .split('\n')
        .map((line) => line.trim().slice(2))
        .filter(Boolean);
}

export function getStatusForFile(filePath: string): GitFileStatus {
    const status = execSync(`git status --porcelain "${filePath}"`).toString().trim();
    if (!status) {
        return GitFileStatus['!'];
    }
    return status.charAt(0) as GitFileStatus;
}

export function getDiffForAll(): string {
    return execSync('git diff').toString();
}

export function getDiffForStagedFiles(): string {
    return execSync('git diff --staged').toString();
}

export function commitWithMessage(message: string): void {
    const sanitizedMessage = sanitizeCommitMessage(message);
    execSync(`git commit -m "${sanitizedMessage}"`);
}

export function getCurrentBranchName(): string {
    return execSync('git rev-parse --abbrev-ref HEAD').toString().trim();
}

export function hasGitChanges(): boolean {
    const status = execSync('git status --porcelain').toString().trim();
    return status.length > 0;
}

export function getName(): string {
    return execSync('git config user.name').toString().trim();
}

export function getEmail(): string {
    return execSync('git config user.email').toString().trim();
}

export function sanitizeCommitMessage(message: string): string {
    return message.replace(/"/g, '\\"');
}
