import assert from "assert"

import { Queue } from "./queue"

enum PType {
  Value,
  Ptr
}

export class VM {
  instrPtr: number = 0
  stdin = new Queue<number>()
  stdout = new Queue<number>()
  memory = new Uint16Array(1 << 15) // 15-bit address space / 16-bit values
  registers = new Uint16Array(1 << 3) // 3-bit address space / 16-bit values
  stack: Array<number> = []
  debug: boolean = false

  opcodes: {
    [code: number]: {
      name: string
      params: PType[]
      exec: (params: Uint16Array) => number
    }
  } = {
    0: {
      name: "halt",
      params: [],
      exec: () => null
    },
    1: {
      name: "set",
      params: [PType.Ptr, PType.Value],
      exec: p => {
        this.registers[p[0]] = p[1]
        return this.instrPtr + 1 + p.length
      }
    },
    2: {
      name: "push",
      params: [PType.Value],
      exec: p => {
        this.stack.push(p[0])
        return this.instrPtr + 1 + p.length
      }
    },
    3: {
      name: "pop",
      params: [PType.Ptr],
      exec: p => {
        this.registers[p[0]] = this.stack.pop()
        return this.instrPtr + 1 + p.length
      }
    },
    4: {
      name: "eq",
      params: [PType.Ptr, PType.Value, PType.Value],
      exec: p => {
        this.registers[p[0]] = p[1] === p[2] ? 1 : 0
        return this.instrPtr + 1 + p.length
      }
    },
    5: {
      name: "gt",
      params: [PType.Ptr, PType.Value, PType.Value],
      exec: p => {
        this.registers[p[0]] = p[1] > p[2] ? 1 : 0
        return this.instrPtr + 1 + p.length
      }
    },
    6: {
      name: "jump",
      params: [PType.Value],
      exec: p => p[0]
    },
    7: {
      name: "jt",
      params: [PType.Value, PType.Value],
      exec: p => (p[0] !== 0 ? p[1] : this.instrPtr + 1 + p.length)
    },
    8: {
      name: "jf",
      params: [PType.Value, PType.Value],
      exec: p => (p[0] === 0 ? p[1] : this.instrPtr + 1 + p.length)
    },
    9: {
      name: "add",
      params: [PType.Ptr, PType.Value, PType.Value],
      exec: p => {
        this.registers[p[0]] = (p[1] + p[2]) % 32768
        return this.instrPtr + 1 + p.length
      }
    },
    10: {
      name: "mult",
      params: [PType.Ptr, PType.Value, PType.Value],
      exec: p => {
        this.registers[p[0]] = (p[1] * p[2]) % 32768
        return this.instrPtr + 1 + p.length
      }
    },
    11: {
      name: "mod",
      params: [PType.Ptr, PType.Value, PType.Value],
      exec: p => {
        this.registers[p[0]] = p[1] % p[2]
        return this.instrPtr + 1 + p.length
      }
    },
    12: {
      name: "and",
      params: [PType.Ptr, PType.Value, PType.Value],
      exec: p => {
        this.registers[p[0]] = p[1] & p[2]
        return this.instrPtr + 1 + p.length
      }
    },
    13: {
      name: "or",
      params: [PType.Ptr, PType.Value, PType.Value],
      exec: p => {
        this.registers[p[0]] = p[1] | p[2]
        return this.instrPtr + 1 + p.length
      }
    },
    14: {
      name: "not",
      params: [PType.Ptr, PType.Value],
      exec: p => {
        this.registers[p[0]] = p[1] ^ ((1 << 15) - 1)
        return this.instrPtr + 1 + p.length
      }
    },
    15: {
      name: "rmem",
      params: [PType.Ptr, PType.Value],
      exec: p => {
        this.registers[p[0]] = this.memory[p[1]]
        return this.instrPtr + 1 + p.length
      }
    },
    16: {
      name: "wmem",
      params: [PType.Value, PType.Value],
      exec: p => {
        this.memory[p[0]] = p[1]
        return this.instrPtr + 1 + p.length
      }
    },
    17: {
      name: "call",
      params: [PType.Value],
      exec: p => {
        this.stack.push(this.instrPtr + 1 + p.length)
        return p[0]
      }
    },
    18: {
      name: "ret",
      params: [],
      exec: () => {
        if (this.stack.length === 0) {
          return null
        }
        return this.stack.pop()
      }
    },
    19: {
      name: "out",
      params: [PType.Value],
      exec: p => {
        this.stdout.push(p[0])
        return this.instrPtr + 1 + p.length
      }
    },
    20: {
      name: "in",
      params: [PType.Ptr],
      exec: p => {
        if (this.stdin.length() === 0) {
          return null
        }

        this.registers[p[0]] = this.stdin.pop()
        return this.instrPtr + 1 + p.length
      }
    },
    21: {
      name: "noop",
      params: [],
      exec: () => this.instrPtr + 1
    }
  }

  constructor(bin: Uint16Array) {
    // load program in memory
    this.memory.set(bin, 0)
  }

  read(addr: number): number {
    assert(0 <= addr && addr < 32776, `invalid address ${addr}`)
    if (addr <= 32767) {
      return addr
    } else {
      return this.registers[addr - 32768]
    }
  }

  write(addr: number, val: number) {
    assert(0 <= addr && addr <= 7, `invalid address ${addr}`)
    this.registers[addr] = val
  }

  run() {
    while (true) {
      assert(0 <= this.instrPtr && this.instrPtr < this.memory.length)

      const opcode = this.memory[this.instrPtr]
      assert(this.opcodes[opcode] !== undefined, `unknown opcode: ${opcode}`)

      if (
        this.debug &&
        opcode === 8 &&
        this.memory[this.instrPtr + 1] === 32775
      ) {
        console.log("OVERRIDE")
        this.registers[7] = 1
      }

      // retrieve params for current opcode
      const params = new Uint16Array(this.opcodes[opcode].params.length)
      for (let i = 0; i < params.length; i++) {
        switch (this.opcodes[opcode].params[i]) {
          case PType.Value:
            params[i] = this.read(this.memory[this.instrPtr + 1 + i])
            break
          case PType.Ptr:
            params[i] = this.memory[this.instrPtr + 1 + i] - 32768
            break
          default:
            assert(false, `bad param type: ${this.opcodes[opcode].params[i]}`)
        }
      }

      if (this.debug) {
        console.log(
          this.instrPtr,
          this.opcodes[opcode].name,
          this.memory.slice(
            this.instrPtr + 1,
            this.instrPtr + 1 + this.opcodes[opcode].params.length
          ),
          params
        )
      }

      // run next op
      const nextInstrPtr = this.opcodes[opcode].exec(params)
      if (nextInstrPtr === null) {
        return
      }
      this.instrPtr = nextInstrPtr
    }
  }
}
