import { call } from './client.ts'
import { start, type Selection } from './workflow.ts'
/**
 * Start a candidate evaluation against an explicit passing baseline; use after choosing a suite.
 * @param input - Server, expected workspace, suite and baseline run identity.
 * @returns A resume receipt, or the provider's unsupported/failure reason.
 * @example
 * import start from 'kody:@your-scope/apastra/start'
 * await start({server: 'apastra', workspaceId: 'my-assistant', suiteId: 'assistant-smoke', baselineRunId: 'saved-run-id'})
 */
export default async function evaluateCandidate(input: Selection) {
	return start(call, input)
}
