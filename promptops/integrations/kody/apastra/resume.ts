import { call } from './client.ts'
import { resume, type Receipt } from './workflow.ts'
/**
 * Poll once and compare a finished candidate; use the receipt returned by start.
 * @param input - Original selection and candidate run identity; keep the baseline explicit.
 * @returns Pending progress or concise metric differences and case evidence references.
 * @example
 * import resume from 'kody:@your-scope/apastra/resume'
 * await resume({server: 'apastra', workspaceId: 'my-assistant', suiteId: 'assistant-smoke', baselineRunId: 'saved-run-id', candidateRunId: 'candidate-run-id'})
 */
export default async function resumeEvaluation(input: Receipt) {
	return resume(call, input)
}
