// import { VM } from "./vm"
// import { Writable } from "stream"

// class StringWritable extends Writable {
//   data = ""

//   _write(chunk: Buffer, _: string, callback: () => void) {
//     this.data += chunk.toString()
//     callback()
//   }
// }

// test("example", async () => {
//   const bin = Uint16Array.from([9, 32768, 32769, 4, 19, 32768])
//   const stdout = new StringWritable()
//   const vm = new VM(bin, stdout)
//   vm.registers[1] = 2
//   await vm.run()

//   expect(vm.registers[0]).toBe(4 + 2)
//   expect(stdout.data).toBe(String.fromCharCode(4 + 2))
// })
