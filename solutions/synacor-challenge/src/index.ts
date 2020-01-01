import readline from "readline"

import { readBin } from "./misc"
import { VM } from "./vm"

function input(): Promise<string> {
  const rl = readline.createInterface({
    input: process.stdin,
  })

  return new Promise(resolve => {
    rl.question("", s => {
      rl.close()
      resolve(s)
    })
  })
}

;(async () => {
  const bin = await readBin("challenge.bin")
  const vm = new VM(bin)

  const initial = [
    "doorway",
    "morth",
    "north",
    "north",
    "bridge",
    "continue",
    "down",
    "east",
    "take empty lantern",
    "west",
    "west",
    "passage",
    "ladder",
    "west",
    "south",
    "north",
    "take can",
    "use can",
    "use lantern",
    "west",
    "ladder",
    "darkness",
    "continue",
    "east",
    "continue",
    "east",
    "continue",
    "west",
    "west",
    "west",
    "west",
    "north",
    "take red coin",
    "north",
    "east",
    "down",
    "take corroded coin",
    "up",
    "west",
    "west",
    "up",
    "take shiny coin",
    "down",
    "take blue coin",
    "east",
    "east",
    "take concave coin",
    "west",
    "use blue coin",
    "use red coin",
    "use shiny coin",
    "use concave coin",
    "use corroded coin",
    "north",
    "take teleporter",
    "use teleporter"
  ]

  vm.stdin.extend(Array.from(Buffer.from(initial.join("\n") + "\n")))

  const commands: string[] = []
  vm.run()
  while (true) {
    console.log(Buffer.from(vm.stdout.popAll()).toString())
    const s = await input()
    if (s == "show") {
      console.log(commands)
    } else {
      if (s === "use teleporter") {
        vm.debug = true
      }
      commands.push(s)
      vm.stdin.extend(Array.from(Buffer.from(s + "\n")))
      vm.run()
      vm.debug = false
    }
  }
})()
