package main

import (
	"fmt"
)

type fenwick []int

func initFenwick(l []int) fenwick {
	f := fenwick(make([]int, len(l)+1))
	for i, x := range l {
		f.add(i, x)
	}
	return f
}

func (f *fenwick) add(i int, x int) {
	i++
	for i < len(*f) {
		(*f)[i] ^= x
		i += i & -i
	}
}

func (f fenwick) sum(i int) int {
	s := 0
	for i > 0 {
		s ^= f[i]
		i -= i & -i
	}
	return s
}

func (f fenwick) sumRange(i, j int) int {
	a := f.sum(i)
	b := f.sum(j)
	return a ^ b
}

func flattenTree(adj [][]int) ([]int, []int) {
	beg := make([]int, len(adj))
	for i := range beg {
		beg[i] = -1
	}
	end := make([]int, len(adj))
	for i := range end {
		end[i] = -1
	}

	i := 0

	q := []int{0}

	for len(q) > 0 {
		current := q[len(q)-1]
		q = q[:len(q)-1]

		if beg[current] == -1 {
			beg[current] = i
			i++
			q = append(q, current)
			for _, neighbor := range adj[current] {
				if beg[neighbor] == -1 {
					q = append(q, neighbor)
				}
			}
		}
		end[current] = i
	}

	return beg, end
}

func main() {
	var N int
	fmt.Scan(&N)

	adj := make([][]int, N)
	for i := 0; i < N-1; i++ {
		var x, y int
		fmt.Scan(&x)
		fmt.Scan(&y)
		adj[x-1] = append(adj[x-1], y-1)
		adj[y-1] = append(adj[y-1], x-1)
	}

	beg, end := flattenTree(adj)

	var letters string
	fmt.Scanln(&letters)

	l := make([]int, N)
	for i, letter := range letters {
		l[beg[i]] = 1 << uint(int(letter)-int('a'))
	}

	f := initFenwick(l)

	var M int
	fmt.Scan(&M)

	for i := 0; i < M; i++ {
		var t int
		fmt.Scan(&t)

		if t == 0 {
			var (
				i          int
				nextLetter int
			)
			fmt.Scanf("%d %c", &i, &nextLetter)
			i--
			nextLetter = 1 << uint(nextLetter-int('a'))
			prevLetter := f.sumRange(beg[i], beg[i]+1)
			if nextLetter != prevLetter {
				f.add(beg[i], nextLetter^prevLetter)
			}
		} else {
			var i int
			fmt.Scan(&i)
			i--
			s := f.sumRange(beg[i], end[i])
			if s == 0 || s-(s&-s) == 0 {
				fmt.Println("YES")
			} else {
				fmt.Println("NO")
			}
		}
	}
}
