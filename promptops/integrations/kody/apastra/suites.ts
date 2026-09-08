import { call } from './client.ts'
import { suites } from './workflow.ts'
/**
 * List suites after confirming the expected workspace; use before starting a candidate.
 * @param input - Connected MCP server name and expected workspace identity.
 * @returns Available suites or a workspace/connector failure.
 * @example
 * import suites from 'kody:@your-scope/apastra/suites'
 * await suites({server: 'apastra', workspaceId: 'my-assistant'})
 */
export default async function listSuites(input: {
	server: string
	workspaceId: string
}) {
	return suites(call, input)
}
