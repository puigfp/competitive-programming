use std::collections::HashSet;
use std::error::Error;
use std::fs::read_to_string;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_to_string("input/day1")?;
    let numbers = input
        .lines()
        .map(|l| -> Result<isize, Box<dyn Error>> { l.parse::<isize>().map_err(|e| e.into()) })
        .collect::<Result<Vec<isize>, Box<dyn Error>>>()?;

    println!("part 1: {}", solve_part1(&numbers));
    println!("part 2: {}", solve_part2(&numbers));
    Ok(())
}

fn solve_part1(numbers: &Vec<isize>) -> isize {
    numbers.iter().map(|i| *i).sum()
}

fn solve_part2(numbers: &Vec<isize>) -> isize {
    let mut frequencies: HashSet<isize> = HashSet::new();
    let mut frequency = 0;
    loop {
        for n in numbers.iter() {
            if frequencies.contains(&frequency) {
                return frequency;
            }
            frequencies.insert(frequency);
            frequency += n;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solve_part1() {
        let cases: Vec<(Vec<isize>, isize)> = vec![
            (vec![], 0),
            (vec![1], 1),
            (vec![1, -2, 3], 2),
            (vec![1, 2], 3),
        ];

        for (input, output) in cases.iter() {
            assert_eq!(solve_part1(input), *output);
        }
    }

    #[test]
    fn test_solve_part2() {
        let cases: Vec<(Vec<isize>, isize)> = vec![
            (vec![0], 0),
            (vec![-1, 1, 5], 0),
            (vec![3, 3, 4, -2, -4], 10),
            (vec![-6, 3, 8, 5, -6], 5),
            (vec![7, 7, -2, -7, -4], 14),
        ];

        for case in cases.iter() {
            assert_eq!(solve_part2(&case.0), case.1);
        }
    }
}
