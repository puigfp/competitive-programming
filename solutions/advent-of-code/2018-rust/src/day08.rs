use std::error::Error;
use std::fs::read_to_string;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_to_string("input/day8")?;
    let numbers = parse_input(&input)?;

    println!("part 1: {}", solve_part1(&numbers));
    println!("part 2: {}", solve_part2(&numbers));

    Ok(())
}

fn solve_part1(numbers: &Vec<usize>) -> usize {
    solve_part1_rec(numbers, 0).0
}

fn solve_part1_rec(numbers: &Vec<usize>, i: usize) -> (usize, usize) {
    let childs = numbers[i];
    let metadata = numbers[i + 1];
    let mut sum = 0;
    let mut end = i + 2;

    for _ in 0..childs {
        let (sum_, end_) = solve_part1_rec(numbers, end);
        sum += sum_;
        end = end_;
    }

    for i in end..end + metadata {
        sum += numbers[i];
    }

    (sum, end + metadata)
}

fn solve_part2(numbers: &Vec<usize>) -> usize {
    solve_part2_rec(&(get_node(numbers, 0).0))
}

fn solve_part2_rec(node: &Node) -> usize {
    if node.childs.len() == 0 {
        return node.metadata.iter().sum();
    }
    node.metadata
        .iter()
        .map(|m| node.childs.get(*m - 1))
        .filter(|e| e.is_some())
        .map(|e| e.unwrap())
        .map(solve_part2_rec)
        .sum()
}

#[derive(Debug)]
struct Node {
    childs: Vec<Node>,
    metadata: Vec<usize>,
}

fn get_node(numbers: &Vec<usize>, i: usize) -> (Node, usize) {
    let childs = numbers[i];
    let metadata = numbers[i + 1];

    let mut node = Node {
        childs: Vec::with_capacity(childs),
        metadata: Vec::with_capacity(metadata),
    };

    let mut end = i + 2;

    for _ in 0..childs {
        let (node_, end_) = get_node(numbers, end);
        node.childs.push(node_);
        end = end_;
    }

    for i in end..end + metadata {
        node.metadata.push(numbers[i]);
    }

    (node, end + metadata)
}

fn parse_input(input: &str) -> Result<Vec<usize>, Box<dyn Error>> {
    let line = input.lines().next().ok_or("empty input")?;
    line.split(" ")
        .map(|n| n.parse::<usize>().map_err(|e| e.into()))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solve_part1() -> Result<(), Box<dyn Error>> {
        assert_eq!(
            solve_part1(&parse_input("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2")?),
            138,
        );
        parse_input("feijfw").unwrap_err();
        Ok(())
    }

    #[test]
    fn test_solve_part2() -> Result<(), Box<dyn Error>> {
        assert_eq!(
            solve_part2(&parse_input("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2")?),
            66,
        );
        parse_input("feijfw").unwrap_err();
        Ok(())
    }

    #[test]
    fn test_parse_input() -> Result<(), Box<dyn Error>> {
        assert_eq!(
            parse_input("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2")?,
            vec![2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]
        );
        parse_input("feijfw").unwrap_err();
        Ok(())
    }
}
