use std::collections::{HashMap, HashSet};
use std::error::Error;
use std::fs::read_to_string;
use std::iter::Iterator;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_to_string("input/day2")?;
    let lines = input.lines().collect();

    println!("part 1: {}", solve_part1(&lines));
    println!("part 2: {}", solve_part2(&lines).ok_or("fail")?);

    Ok(())
}

fn solve_part1(lines: &Vec<&str>) -> isize {
    let mut two = 0;
    let mut three = 0;
    for line in lines {
        let values = get_values(line);
        if values.0 {
            two += 1;
        }
        if values.1 {
            three += 1;
        }
    }
    two * three
}

fn solve_part2(lines: &Vec<&str>) -> Option<String> {
    // one bucket per character index
    let mut s: Vec<HashSet<String>> = Vec::new();

    for line in lines {
        for (j, substring) in get_substrings(line).enumerate() {
            // does the bucket exist ?
            if s.len() <= j {
                s.push(HashSet::new());
            }

            // is this substring already in this char index bucket ?
            match s[j].get(&substring) {
                Some(_) => return Some(substring.clone()),
                None => (),
            }

            // insert it if not
            s[j].insert(substring);
        }
    }

    None
}

fn get_values(id: &str) -> (bool, bool) {
    let mut two = false;
    let mut three = false;
    for (_, value) in get_counts(id).iter() {
        match value {
            2 => two = true,
            3 => three = true,
            _ => (),
        }
    }
    return (two, three);
}

fn get_counts(id: &str) -> HashMap<char, i32> {
    let mut counts: HashMap<char, i32> = HashMap::new();
    for c in id.chars() {
        let count = match counts.get(&c) {
            Some(n) => *n + 1,
            None => 1,
        };
        counts.insert(c, count);
    }
    return counts;
}

struct Substrings {
    chars: Vec<char>,
    next: usize,
}

impl Iterator for Substrings {
    type Item = String;

    fn next(&mut self) -> Option<String> {
        if self.next >= self.chars.len() {
            return None;
        }
        let begin: String = self.chars[..self.next].iter().collect();
        let end: String = self.chars[self.next + 1..].iter().collect();
        self.next += 1;
        Some(begin + &end)
    }
}

fn get_substrings(id: &str) -> Box<dyn Iterator<Item = String>> {
    Box::new(Substrings {
        chars: id.chars().collect(),
        next: 0,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_counts() {
        let s = String::from("abcaba");
        let chars = vec!['a', 'b', 'c'];
        let counts = get_counts(&s);
        assert_eq!(*counts.get(&chars[0]).unwrap(), 3);
        assert_eq!(*counts.get(&chars[1]).unwrap(), 2);
        assert_eq!(*counts.get(&chars[2]).unwrap(), 1);
    }

    #[test]
    fn test_get_values() {
        {
            let s = String::from("abcaba");
            let values = get_values(&s);
            assert_eq!(values.0, true);
            assert_eq!(values.1, true);
        }

        {
            let s = String::from("aaaaaaa");
            let values = get_values(&s);
            assert_eq!(values.0, false);
            assert_eq!(values.1, false);
        }
    }

    #[test]
    fn test_get_substrings() {
        let s = String::from("abcde");
        assert_eq!(
            get_substrings(&s).collect::<Vec<String>>(),
            vec!["bcde", "acde", "abde", "abce", "abcd",]
        )
    }

    #[test]
    fn test_solve_part1() {
        {
            let s = vec![
                "abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab",
            ];
            assert_eq!(solve_part1(&s), 12);
        }
    }

    #[test]
    fn test_solve_part2() {
        let s = vec![
            "abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz",
        ];
        assert_eq!(solve_part2(&s).unwrap(), "fgij");
    }
}
