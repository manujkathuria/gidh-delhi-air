/** Copy only deliberately published aggregate artifacts into the web build. */
import { cp, mkdir, readdir, rename, rm } from 'node:fs/promises'
import { dirname, extname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = dirname(dirname(fileURLToPath(import.meta.url)))
const source = join(root, 'data/published')
const destination = join(root, 'apps/web/public/research')
const staging = join(root, 'apps/web/public/.research-staging')
const allowed = new Set(['.json', '.csv'])

async function collect(directory, relative = '') {
  const files = []
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (entry.isSymbolicLink()) throw new Error(`Published exports must not contain symlinks: ${entry.name}`)
    const path = join(relative, entry.name)
    if (entry.isDirectory()) files.push(...await collect(join(directory, entry.name), path))
    else if (entry.isFile() && allowed.has(extname(entry.name))) files.push(path)
  }
  return files
}

const files = await collect(source)
await rm(staging, { recursive: true, force: true })
await mkdir(staging, { recursive: true })
for (const path of files) {
  await mkdir(dirname(join(staging, path)), { recursive: true })
  await cp(join(source, path), join(staging, path))
}
// Replace only this script's generated destination; never modify source exports.
await rm(destination, { recursive: true, force: true })
await rename(staging, destination)
console.log(`Synced ${files.length} reviewed research export(s).`)
