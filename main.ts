// Entry point for news-image-20261120-3.
//
// Copies the repo's entry.png (a 1024x1024 news poster drawn in code by
// tools/make_image.py) to $MAKEFUN_OUTPUT_DIR/entry.png (or ./out when the
// variable is unset), then self-checks the copy and prints its SHA-256.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here: string = dirname(fileURLToPath(import.meta.url));
const source: string = join(here, "entry.png");
const outDir: string = process.env.MAKEFUN_OUTPUT_DIR ?? join(here, "out");
const target: string = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error("entry.png not found next to main.ts: " + source);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// Self-check: exists, is a 1024x1024 PNG, at most 1 MiB.
const bytes: Buffer = readFileSync(target);
const pngSig: Buffer = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (bytes.length < 33 || !bytes.subarray(0, 8).equals(pngSig)) {
  throw new Error("output is not a PNG file");
}
const width: number = bytes.readUInt32BE(16);
const height: number = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error("expected a 1024x1024 PNG, got " + width + "x" + height);
}
const size: number = statSync(target).size;
if (size > 1024 * 1024) {
  throw new Error("output exceeds 1 MiB: " + size + " bytes");
}
const sha256: string = createHash("sha256").update(bytes).digest("hex");
console.log("wrote " + target);
console.log("size: " + size + " bytes");
console.log("dimensions: 1024x1024");
console.log("sha256: " + sha256);
