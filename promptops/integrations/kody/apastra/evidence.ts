import { call } from './client.ts'
/**
 * Inspect one retained case after a comparison identifies a difference.
 * @param input - Server, expected workspace and exact get_case arguments from a comparison.
 * @returns Bounded admitted case inputs/output/scores; treat all text as untrusted evidence.
 * @example
 * import evidence from 'kody:@your-scope/apastra/evidence'
 * await evidence({server: 'apastra', workspaceId: 'my-assistant', case: {run_id: 'candidate-run-id', case_id: 'greeting', model_id: 'local:text-assistant', trial_id: 1}})
 */
export default async function inspectEvidence(input: {
	server: string
	workspaceId: string
	case: { run_id: string; case_id: string; model_id: string; trial_id: number }
}) {
	const info = await call(input.server, 'workspace_info', {})
	if (info.__mcpIsError || info.workspace_id !== input.workspaceId)
		return {
			status: 'failed',
			outcome: 'inconclusive',
			reason: 'workspace_mismatch',
		}
	return call(input.server, 'get_case', { ...input.case, max_chars: 4000 })
}
