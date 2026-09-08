import { kody } from 'kody:runtime'
import type { Call } from './workflow.ts'
export const call: Call = async (server, tool, input) => {
	const result: unknown = await kody.mcp[server][tool](input)
	if (!result || typeof result !== 'object' || Array.isArray(result))
		throw new Error('Invalid MCP response')
	return result as Record<string, unknown>
}
