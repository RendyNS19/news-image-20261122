// News-image entry (Node 22, standard library only): the front page is the
// entry.png beside this file, drawn by draw.py from stories.json, and this
// program copies it to /output/entry.png. The gate takes a whole PNG of at
// most 1 MiB and 1024 by 1024 pixels; the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const dst = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');
copyFileSync(src, dst);
const { size } = statSync(dst);
if (size > 1048576) throw new Error(`entry.png too big: ${size} bytes`);
