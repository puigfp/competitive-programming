export class Queue<T> {
  in: Array<T> = []
  out: Array<T> = []

  length(): number {
    return this.in.length + this.out.length
  }

  push(elem: T) {
    this.in.push(elem)
  }

  extend(arr: T[]) {
    this.in = this.in.concat(arr)
  }

  pop(): T {
    if (this.out.length === 0) {
      this.in.reverse()
      this.out = this.in
      this.in = []
    }

    return this.out.pop()
  }

  popAll(): T[] {
    this.out.reverse()
    const out: T[] = [].concat(this.out, this.in)
    this.in = []
    this.out = []
    return out
  }
}
