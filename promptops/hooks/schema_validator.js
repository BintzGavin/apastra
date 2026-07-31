"use strict";

const fs = require("fs");
const path = require("path");
const AjvDraft7 = require("ajv").default;
const Ajv2020 = require("ajv/dist/2020").default;
const addFormats = require("ajv-formats");
const yaml = require("js-yaml");

function emit(payload, status) {
  process.stdout.write(`${JSON.stringify(payload)}\n`);
  process.exit(status);
}

if (process.argv[2] === "--probe") {
  emit({ status: "ready" }, 0);
}

const [schemaDir, schemaName, dataFile, mode] = process.argv.slice(2);
if (!schemaDir || !schemaName || !dataFile || !mode) {
  emit({ status: "unavailable" }, 2);
}

function safeValidationErrors(errors, lineNumber) {
  return (errors || []).map((error) => {
    const line = lineNumber ? `line ${lineNumber} ` : "";
    const location = error.instancePath || "/";
    const message = error.message || error.keyword || "schema validation failed";
    return `${line}${location}: ${message}`;
  });
}

function parseDocument(source, filename) {
  const extension = path.extname(filename).toLowerCase();
  if (extension === ".json") {
    return JSON.parse(source);
  }
  return yaml.load(source);
}

try {
  const schemaFiles = fs
    .readdirSync(schemaDir)
    .filter((name) => name.endsWith(".schema.json"))
    .sort();
  const schemas = new Map();
  for (const filename of schemaFiles) {
    const schema = JSON.parse(fs.readFileSync(path.join(schemaDir, filename), "utf8"));
    schemas.set(filename, schema);
  }

  const targetSchema = schemas.get(schemaName);
  if (!targetSchema) {
    emit({ status: "unavailable" }, 2);
  }
  const targetDialect = targetSchema.$schema || "";
  const usesDraft2020 = targetDialect.includes("2020-12");
  const ajv = usesDraft2020
    ? new Ajv2020({ allErrors: true, strict: false, validateFormats: true })
    : new AjvDraft7({ allErrors: true, strict: false, validateFormats: true });
  addFormats(ajv);
  for (const [filename, schema] of schemas.entries()) {
    const schemaDialect = schema.$schema || "";
    if (schemaDialect.includes("2020-12") !== usesDraft2020) {
      continue;
    }
    ajv.addSchema(schema, schema.$id || filename);
  }
  const validate =
    (targetSchema.$id && ajv.getSchema(targetSchema.$id)) ||
    ajv.getSchema(schemaName) ||
    ajv.compile(targetSchema);

  const source = fs.readFileSync(dataFile, "utf8");
  const failures = [];
  if (mode === "jsonl") {
    source.split(/\r?\n/).forEach((line, index) => {
      if (!line.trim()) {
        return;
      }
      try {
        const data = JSON.parse(line);
        if (!validate(data)) {
          failures.push(...safeValidationErrors(validate.errors, index + 1));
        }
      } catch (error) {
        failures.push(`line ${index + 1}: invalid JSON`);
      }
    });
  } else {
    try {
      const data = parseDocument(source, dataFile);
      if (!validate(data)) {
        failures.push(...safeValidationErrors(validate.errors));
      }
    } catch (error) {
      failures.push("/: document could not be parsed");
    }
  }

  if (failures.length) {
    emit({ status: "fail", errors: failures }, 1);
  }
  emit({ status: "pass" }, 0);
} catch (error) {
  emit({ status: "unavailable" }, 2);
}
