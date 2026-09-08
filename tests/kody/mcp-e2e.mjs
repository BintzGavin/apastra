/** Run with Node 26: mcp-e2e.mjs <Apastra venv python> <SDK package directory>. */
import assert from 'node:assert/strict'
import { cp, mkdtemp, readFile, writeFile, rm } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { resolve, join } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import {
	start,
	resume,
	suites,
} from '../../promptops/integrations/kody/apastra/workflow.ts'

const [python, sdk] = process.argv.slice(2)
if (!python || !sdk)
	throw new Error(
		'Pass the venv interpreter and installed @modelcontextprotocol/sdk directory',
	)
const { Client } = await import(
	pathToFileURL(resolve(sdk, 'dist/esm/client/index.js'))
)
const { StdioClientTransport } = await import(
	pathToFileURL(resolve(sdk, 'dist/esm/client/stdio.js'))
)
const root = fileURLToPath(new URL('../..', import.meta.url))
const workspace = await mkdtemp(join(tmpdir(), 'apastra-package-e2e-'))
await cp(
	join(root, 'promptops/examples/kody-regression/workspace'),
	workspace,
	{ recursive: true },
)
const client = new Client({
	name: 'apastra-package-acceptance',
	version: '1.0.0',
})
const transport = new StdioClientTransport({
	command: python,
	args: [
		join(root, 'bin/apastra'),
		'mcp',
		'--workspace',
		workspace,
		'--workspace-id',
		'package-demo',
		'--adapter',
		'promptops/harnesses/local.json',
	],
	stderr: 'ignore',
})
try {
	await client.connect(transport)
	const call = async (server, name, args) => {
		assert.equal(server, 'apastra')
		const response = await client.callTool({ name, arguments: args })
		assert.equal(response.isError, false)
		assert.ok(response.structuredContent)
		// Kody exposes downstream structuredContent as a plain object to package code.
		return response.structuredContent
	}
	const selected = {
		server: 'apastra',
		workspaceId: 'package-demo',
		suiteId: 'assistant-smoke',
	}
	assert.equal((await suites(call, selected)).suites[0].id, selected.suiteId)
	const baseline = await call('apastra', 'start_evaluation', {
		suite_id: selected.suiteId,
	})
	async function complete(runId) {
		for (let attempt = 0; attempt < 200; attempt++) {
			const result = await call('apastra', 'get_run', { run_id: runId })
			if (!['running', 'queued'].includes(result.status)) return result
			await new Promise((resolve) => setTimeout(resolve, 30))
		}
		throw new Error('Local run exceeded acceptance deadline')
	}
	assert.equal((await complete(baseline.run_id)).outcome, 'success')
	const prompt = join(workspace, 'promptops/prompts/assistant.json')
	const original = await readFile(prompt, 'utf8')
	for (const [template, outcome] of [
		[original.replace('Uppercase', 'Lowercase'), 'regression'],
		[original, 'success'],
	]) {
		await writeFile(prompt, template)
		const receipt = await start(call, {
			...selected,
			baselineRunId: baseline.run_id,
		})
		assert.equal(receipt.status, 'pending')
		await complete(receipt.resume.candidateRunId)
		const report = await resume(call, receipt.resume)
		assert.equal(report.outcome, outcome)
		if (outcome === 'regression') {
			const reference = report.changedCases[0].candidate_evidence
			const evidence = await call(
				'apastra',
				reference.tool,
				reference.arguments,
			)
			assert.notEqual(evidence.case.output, evidence.case.expected_outputs.text)
		}
		console.log(report.summary)
	}
} finally {
	await client.close()
	await rm(workspace, { recursive: true, force: true })
}
