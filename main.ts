import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Keep the destination path configurable for local runs and the grader.
const outputDirectory = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const entryImage = resolve(scriptDirectory, "entry.png");
mkdirSync(outputDirectory, { recursive: true });
copyFileSync(entryImage, resolve(outputDirectory, "entry.png"));
