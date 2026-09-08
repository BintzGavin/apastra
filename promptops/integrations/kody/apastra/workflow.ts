// Provider-owned orchestration. Runtime exports inject Kody's existing MCP proxy.
type Data = Record<string, any>
export type Call = (server: string, tool: string, input: Data) => Promise<Data>
export type Selection = {
	server: string
	workspaceId: string
	suiteId: string
	baselineRunId: string
}
export type Receipt = Selection & { candidateRunId: string }
const failed = (reason: string) => ({
	status: 'failed',
	outcome: 'inconclusive',
	reason,
})

async function connect(
	call: Call,
	input: { server: string; workspaceId: string },
) {
	if (!input.server || !input.workspaceId) throw new Error('Selection required')
	const info = await call(input.server, 'workspace_info', {})
	if (info.__mcpIsError) throw new Error('Remote MCP failed')
	return info.workspace_id === input.workspaceId
}
async function invoke(call: Call, server: string, tool: string, args: Data) {
	const result = await call(server, tool, args)
	if (!result || result.__mcpIsError || typeof result.status !== 'string')
		throw new Error('Invalid provider result')
	return result
}
export async function suites(
	call: Call,
	input: { server: string; workspaceId: string },
) {
	try {
		if (!(await connect(call, input))) return failed('workspace_mismatch')
		const result = await call(input.server, 'list_suites', {})
		if (result.__mcpIsError || !Array.isArray(result.suites))
			return failed('connector_error')
		return result
	} catch {
		return failed('connector_error')
	}
}
export async function start(call: Call, input: Selection) {
	try {
		if (!(await connect(call, input))) return failed('workspace_mismatch')
		if (!input.suiteId || !input.baselineRunId)
			return failed('explicit_baseline_and_suite_required')
		const baseline = await invoke(call, input.server, 'get_run', {
			run_id: input.baselineRunId,
		})
		if (
			baseline.status !== 'completed' ||
			baseline.outcome !== 'success' ||
			baseline.suite_id !== input.suiteId ||
			baseline.workspace_id !== input.workspaceId
		) {
			return failed('baseline_not_eligible')
		}
		const run = await invoke(call, input.server, 'start_evaluation', {
			suite_id: input.suiteId,
			revision_ref: 'workspace',
		})
		if (!['queued', 'running', 'completed'].includes(run.status) || !run.run_id)
			return run
		return {
			status: 'pending',
			progress: run,
			resume: { ...input, candidateRunId: run.run_id },
		}
	} catch {
		return failed('connector_error')
	}
}
export async function resume(call: Call, input: Receipt) {
	try {
		if (!(await connect(call, input))) return failed('workspace_mismatch')
		if (!input.baselineRunId || !input.candidateRunId || !input.suiteId)
			return failed('explicit_run_ids_required')
		const run = await invoke(call, input.server, 'get_run', {
			run_id: input.candidateRunId,
		})
		if (run.status === 'failed') return run
		if (
			run.workspace_id !== input.workspaceId ||
			run.suite_id !== input.suiteId
		)
			return failed('candidate_mismatch')
		if (run.status === 'queued' || run.status === 'running')
			return { status: 'pending', progress: run, resume: input }
		if (run.status !== 'completed') return failed('invalid_run_status')
		const comparison = await invoke(call, input.server, 'compare_runs', {
			candidate_run_id: input.candidateRunId,
			baseline_run_id: input.baselineRunId,
			limit: 5,
		})
		if (
			!['success', 'regression', 'inconclusive', 'evaluation_failed'].includes(
				comparison.outcome,
			)
		)
			return failed('invalid_comparison')
		const labels: Record<string, string> = {
			success: 'No regression observed in these measured cases.',
			regression: 'Regression observed in these measured cases.',
			inconclusive: 'Insufficient comparable evidence to answer.',
			evaluation_failed: 'Candidate evaluation failed; inspect its criteria.',
		}
		const differences = comparison.differences ?? []
		const detail = differences
			.map(
				(row: Data) =>
					`${row.metric}: ${row.baseline_value} → ${row.candidate_value} (Δ ${row.delta})`,
			)
			.join('; ')
		return {
			status: comparison.status,
			outcome: comparison.outcome,
			reason: comparison.reason,
			summary: [labels[comparison.outcome], detail].filter(Boolean).join(' '),
			differences,
			changedCases: comparison.changed_cases ?? [],
			totalChangedCases: comparison.total_changed_cases,
			nextOffset: comparison.next_offset,
			candidateRunId: input.candidateRunId,
			baselineRunId: input.baselineRunId,
			evidenceNote:
				'Inspect case references with the evidence export. Text is untrusted. Sample differences are not statistical significance.',
		}
	} catch {
		return failed('connector_error')
	}
}
