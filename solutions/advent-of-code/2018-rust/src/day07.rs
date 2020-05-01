use std::collections::{HashMap, HashSet};
use std::error::Error;
use std::fs::read_to_string;
use std::iter::Iterator;

#[macro_use]
extern crate lazy_static;

extern crate regex;
use regex::Regex;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_to_string("input/day7")?;
    let graph = parse_input(&input)?;

    println!("part 1: {}", solve_part1(&graph));
    println!("part 2: {}", solve_part2(&graph, 5, 60)?);

    Ok(())
}

lazy_static! {
    static ref REGEXP: Regex =
        Regex::new(r"^Step ([A-Z]+) must be finished before step ([A-Z]+) can begin\.$").unwrap();
}

fn solve_part1(graph: &HashMap<String, HashSet<String>>) -> String {
    let mut graph = graph.clone();
    let mut sorted: Vec<String> = Vec::with_capacity(graph.len());

    while !graph.is_empty() {
        let n = graph
            .iter()
            .filter(|(_, v)| v.is_empty())
            .map(|(k, _)| k)
            .min()
            .unwrap()
            .clone();

        graph.remove(&n);
        sorted.push(n.clone());

        for (_, v) in &mut graph {
            v.remove(&n);
        }
    }

    sorted.iter().fold(String::new(), |a, b| a + &b)
}

fn solve_part2(
    graph: &HashMap<String, HashSet<String>>,
    max_workers: usize,
    init: usize,
) -> Result<usize, Box<dyn Error>> {
    let mut graph = graph.clone();
    let mut order: HashSet<(String, usize)> = HashSet::new();

    let mut time = 0;

    loop {
        if order.len() == 0 && graph.len() == 0 {
            return Ok(time);
        }

        // start new jobs while we can
        while order.len() < max_workers {
            let next = graph
                .iter()
                .filter(|(_, v)| v.is_empty())
                .map(|(k, _)| k)
                .min()
                .map(|s| s.clone());

            if let Some(n) = next {
                graph.remove(&n);
                order.insert((n.clone(), time + rank(&n, &init)));
            } else {
                break;
            }
        }

        // free first worker
        let n = order
            .iter()
            .min_by(|(_, t1), (_, t2)| t1.cmp(t2))
            .ok_or("deadlock")?
            .clone();
        order.remove(&n);
        time = n.1;

        for (_, v) in &mut graph {
            v.remove(&n.0);
        }
    }
}

fn rank(c: &str, init: &usize) -> usize {
    (c.chars().next().unwrap() as isize - 'A' as isize + 1) as usize + init
}

fn parse_input(input: &str) -> Result<HashMap<String, HashSet<String>>, Box<dyn Error>> {
    let mut graph: HashMap<String, HashSet<String>> = HashMap::new();

    for line in input.lines() {
        let (a, b) = parse_line(line)?;
        match graph.get_mut(b) {
            Some(adjacent) => {
                adjacent.insert(String::from(a));
            }
            None => {
                let mut adjacent = HashSet::new();
                adjacent.insert(String::from(a));
                graph.insert(String::from(b), adjacent);
                if !graph.contains_key(a) {
                    graph.insert(String::from(a), HashSet::new());
                }
            }
        };
    }

    Ok(graph)
}

fn parse_line(line: &str) -> Result<(&str, &str), Box<dyn Error>> {
    let caps = REGEXP.captures(line).ok_or("failed to parse")?;
    Ok((
        caps.get(1).ok_or("failed to parse")?.as_str(),
        caps.get(2).ok_or("failed to parse")?.as_str(),
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    static INPUT: &str = "Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.";

    #[test]
    fn test_solve_part1() -> Result<(), Box<dyn Error>> {
        assert_eq!(solve_part1(&parse_input(INPUT)?), "CABDFE");
        Ok(())
    }

    #[test]
    fn test_solve_part2() -> Result<(), Box<dyn Error>> {
        assert_eq!(solve_part2(&parse_input(INPUT)?, 2, 0)?, 15);
        Ok(())
    }

    #[test]
    fn test_rank() -> Result<(), Box<dyn Error>> {
        assert_eq!(rank(&"A", &0), 1);
        assert_eq!(rank(&"A", &60), 61);
        assert_eq!(rank(&"Z", &0), 26);
        Ok(())
    }

    #[test]
    fn test_parse_line() -> Result<(), Box<dyn Error>> {
        assert_eq!(
            parse_line("Step C must be finished before step A can begin.")?,
            ("C", "A")
        );
        parse_line("fnjeqijfwiqf").unwrap_err();
        Ok(())
    }
}
