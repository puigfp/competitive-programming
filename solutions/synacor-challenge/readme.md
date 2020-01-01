This is a partial solution to the [Synacor Challenge](https://challenge.synacor.com/).

I wrote the code in TypeScript because I wanted to experiment with this language and see how the dev experience was.

---

About the Synacor Challenge itself:

I've only found 6 codes (out of 8).

- code 1: in arch-spec
- code 2: hello world interpreter
- code 3: working interpreter
- code 4: read tablet
- code 5: find light (manual trial error... but should be with using a proper BFS)
- code 6: solve coin equations (one-liner solution in `coins.py`, because lodash doesn't have a `_.permutations` function)
- code 7: ???
- code 8: ???

---

About the TypeScript dev experience:

Overall, once everything was set up, it was very fun to write code:

- the types allow the editor to make proper suggestions (and most third-party packages have TypeScript type declarations)
- the compiler did catch mistakes (and overall, I felt more confident that the code I was writing would work)
- Prettier integrates really well with TypeScript and VS Code, it was easy to have the code be auto-formatted on every file save


But there was a few downsides:

- `ts-node`'s startup-time felt too long
- it took me more time than I expected to get everything working (the TypeScript compiler, Jest, Prettier, etc):
    - I found than a lot of things have too many configuration options compared to what I was used to (the documentations for Prettier and TypeScript's documentation are very very long)
    - writing those configuration files often requires some context on the JavaScript world (for instance, I needed to set 3 different config options to make the TS compiler translate correctly the `import`-related statements)
- TypeScript compiles to Node.js-compatible code, so a lot functionality comes from Node's standard library:
    - I've found the documentation abound consuming streams or implementing custom streams very confusing, so I ended up giving up on using the `Writable` and `Readable` interfaces for my VM's `stdin` and `stdout`, and implemented using a very basic homemade `Queue<int>` data structure
    - most IO/async-related APIs are using callback style or event-driven patterns instead of async/await. this made writing a simple `input()` function that returns the next line coming through `stdin` not very intuitive (see [src/index.ts](src/index.ts))

