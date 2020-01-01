import { promises as fs } from "fs"

export async function readBin(path: string): Promise<Uint16Array> {
  const buf: Buffer = await fs.readFile(path)
  return bufferToUint16Array(buf)
}

export function bufferToUint16Array(buf: Buffer): Uint16Array {
  // note: Buffer ~= Uint8Array
  const bin = new Uint16Array(buf.length / 2)
  for (let i = 0; i < bin.length; i += 1) {
    bin[i] = buf.readUInt16LE(i * 2)
  }
  return bin
}
