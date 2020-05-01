use std::collections::HashSet;
use std::error::Error;
use std::fs::read_to_string;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_to_string("input/day5")?;
    let line = input.lines().next().ok_or("bad input")?;

    println!("part 1: {}", solve_part1(line));
    println!("part 2: {}", solve_part2(line)?);

    Ok(())
}

fn solve_part1(s: &str) -> usize {
    react(s).len()
}

fn solve_part2(s: &str) -> Result<usize, Box<dyn Error>> {
    let chars: HashSet<char> = s.chars().collect();
    Ok(chars
        .iter()
        .map(|c| {
            let stripped: String = strip(s, c);
            (c, react(&stripped).len())
        })
        .min_by(|a, b| a.1.cmp(&(b.1)))
        .ok_or("fail")?
        .1)
}

fn strip(s: &str, c: &char) -> String {
    s.chars()
        .filter(|d| c.to_lowercase().next() != d.to_lowercase().next())
        .collect()
}

fn react(s: &str) -> String {
    let mut res: Vec<char> = Vec::with_capacity(s.len());
    for c in s.chars() {
        if res.len() == 0 {
            res.push(c);
            continue;
        }

        if reaction(res.last().unwrap(), &c) {
            res.pop();
            continue;
        }

        res.push(c);
    }
    res.iter().collect()
}

fn reaction(a: &char, b: &char) -> bool {
    *a != *b && a.to_lowercase().next() == b.to_lowercase().next()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_strip() {
        let cases = vec![
            (("dabAcCaCBAcCcaDA", 'A'), "dbcCCBcCcD"),
            (("dabAcCaCBAcCcaDA", 'a'), "dbcCCBcCcD"),
            (("dabAcCaCBAcCcaDA", 'B'), "daAcCaCAcCcaDA"),
            (("dabAcCaCBAcCcaDA", 'b'), "daAcCaCAcCcaDA"),
        ];
        for ((a, b), res) in cases {
            assert_eq!(strip(&a, &b), res);
        }
    }

    #[test]
    fn test_reaction() {
        let cases = vec![(('a', 'A'), true), (('a', 'a'), false), (('a', 'B'), false)];
        for ((a, b), res) in cases {
            assert_eq!(reaction(&a, &b), res);
        }
    }

    #[test]
    fn test_solve_part1() {
        assert_eq!(solve_part1("dabAcCaCBAcCcaDA"), 10)
    }

    #[test]
    fn test_solve_part2() {
        assert_eq!(solve_part2("dabAcCaCBAcCcaDA").unwrap(), 4)
    }
}
