import test from 'node:test'
import assert from 'node:assert/strict'
import {
	start,
	resume,
	suites,
} from '../../promptops/integrations/kody/apastra/workflow.ts'

const selection = {
	server: 'apastra',
	workspaceId: 'mine',
	suiteId: 'smoke',
	baselineRunId: 'baseline',
}
function provider(overrides = {}) {
	const calls = []
	const methods = {
		workspace_info: () => ({ workspace_id: 'mine' }),
		list_suites: () => ({
			workspace_id: 'mine',
			suites: [{ id: 'smoke' }],
			invalid_suites: [],
		}),
		get_run: ({ run_id }) => ({
			status: 'completed',
			outcome: 'success',
			suite_id: 'smoke',
			workspace_id: 'mine',
			run_id,
		}),
		start_evaluation: () => ({
			status: 'queued',
			run_id: 'candidate',
			workspace_id: 'mine',
			suite_id: 'smoke',
		}),
		compare_runs: () => ({
			status: 'completed',
			outcome: 'regression',
			candidate_run_id: 'candidate',
			baseline_run_id: 'baseline',
			differences: [
				{
					metric: 'quality',
					candidate_value: 0.5,
					baseline_value: 1,
					delta: -0.5,
				},
			],
			changed_cases: [
				{
					case_id: 'one',
					candidate_evidence: {
						tool: 'get_case',
						arguments: { run_id: 'candidate', case_id: 'one' },
					},
				},
			],
			total_changed_cases: 1,
			next_offset: null,
		}),
		...overrides,
	}
	return {
		calls,
		call: async (server, tool, input) => {
			calls.push({ server, tool, input })
			return methods[tool](input)
		},
	}
}

test('start verifies workspace and baseline before executing and returns a resume receipt', async () => {
	const api = provider()
	const result = await start(api.call, selection)
	assert.equal(result.status, 'pending')
	assert.deepEqual(result.resume, { ...selection, candidateRunId: 'candidate' })
	assert.equal(
		api.calls.filter((call) => call.tool === 'start_evaluation').length,
		1,
	)
})
test('select suites verifies the expected workspace', async () => {
	const api = provider()
	assert.equal((await suites(api.call, selection)).suites[0].id, 'smoke')
	const wrong = provider({
		workspace_info: () => ({ workspace_id: 'someone-else' }),
	})
	assert.equal(
		(await start(wrong.call, selection)).reason,
		'workspace_mismatch',
	)
	assert.equal(wrong.calls.length, 1)
})
test('no failed baseline or unavailable adapter becomes a successful evaluation', async () => {
	const bad = provider({
		get_run: () => ({ status: 'failed', outcome: 'evaluation_failed' }),
	})
	assert.equal(
		(await start(bad.call, selection)).reason,
		'baseline_not_eligible',
	)
	assert.equal(
		bad.calls.some((call) => call.tool === 'start_evaluation'),
		false,
	)
	const absent = provider({
		start_evaluation: () => ({
			status: 'failed',
			outcome: 'unsupported',
			reason: 'adapter_required',
		}),
	})
	assert.equal((await start(absent.call, selection)).outcome, 'unsupported')
})
test('resume returns progress promptly and does not compare unfinished evidence', async () => {
	const api = provider({
		get_run: () => ({
			status: 'running',
			elapsed_seconds: 10,
			stage: 'harness_execution',
			suite_id: 'smoke',
			workspace_id: 'mine',
		}),
	})
	const result = await resume(api.call, {
		...selection,
		candidateRunId: 'candidate',
	})
	assert.equal(result.status, 'pending')
	assert.equal(result.progress.elapsed_seconds, 10)
	assert.equal(
		api.calls.some((call) => call.tool === 'compare_runs'),
		false,
	)
})
test('completed threshold failure still compares and returns regression with inspectable case references', async () => {
	const api = provider({
		get_run: () => ({
			status: 'completed',
			outcome: 'evaluation_failed',
			suite_id: 'smoke',
			workspace_id: 'mine',
		}),
	})
	const result = await resume(api.call, {
		...selection,
		candidateRunId: 'candidate',
	})
	assert.equal(result.outcome, 'regression')
	assert.match(result.summary, /quality: 1 → 0.5/)
	assert.equal(result.changedCases[0].candidate_evidence.tool, 'get_case')
})
test('inconclusive and provider failures survive unchanged; wire errors fail closed', async () => {
	for (const outcome of ['inconclusive', 'evaluation_failed', 'success']) {
		const api = provider({
			compare_runs: () => ({
				status: 'completed',
				outcome,
				differences: [],
				changed_cases: [],
			}),
		})
		assert.equal(
			(await resume(api.call, { ...selection, candidateRunId: 'candidate' }))
				.outcome,
			outcome,
		)
	}
	const broken = provider({ workspace_info: () => ({ __mcpIsError: true }) })
	assert.equal((await start(broken.call, selection)).reason, 'connector_error')
	const legacy = provider({
		workspace_info: () => ({ content: [{ type: 'text', text: '{}' }] }),
	})
	assert.equal(
		(await start(legacy.call, selection)).reason,
		'workspace_mismatch',
	)
})
test('resume rejects a candidate from another suite before comparison', async () => {
	const api = provider({
		get_run: () => ({
			status: 'completed',
			outcome: 'success',
			suite_id: 'other',
			workspace_id: 'mine',
		}),
	})
	assert.equal(
		(await resume(api.call, { ...selection, candidateRunId: 'candidate' }))
			.reason,
		'candidate_mismatch',
	)
	assert.equal(
		api.calls.some((call) => call.tool === 'compare_runs'),
		false,
	)
})
