use std::error::Error;
use std::fs::read_to_string;

fn main() -> Result<(), Box<dyn Error>> {
    let input: usize = read_to_string("input/day11")?
        .lines()
        .next()
        .ok_or("bad input")?
        .parse()?;

    let (x, y) = solve_part1(&input);
    println!("part 1: {},{}", x, y);

    let (x, y, size) = solve_part2(&input);
    println!("part 2: {},{},{}", x, y, size);

    Ok(())
}

fn solve_part1(serial: &usize) -> (usize, usize) {
    let mut result = ((0, 0), get_grid_power_level(&0, &0, serial, &3));
    for x in 1..(301 - 3) {
        for y in 1..(301 - 3) {
            let level = get_grid_power_level(&x, &y, serial, &3);
            if level > result.1 {
                result = ((x, y), level);
            }
        }
    }
    result.0
}

fn solve_part2(serial: &usize) -> (usize, usize, usize) {
    let mut dynamic: Vec<Vec<isize>> = Vec::new();
    for x in 0..300 {
        dynamic.push(Vec::new());
        for y in 0..300 {
            let mut r = get_power_level(&x, &y, serial);
            if x > 0 && y > 0 {
                r += dynamic[x][y - 1] + dynamic[x - 1][y] - dynamic[x - 1][y - 1];
            } else if x > 0 {
                r += dynamic[x - 1][y];
            } else if y > 0 {
                r += dynamic[x][y - 1];
            }
            dynamic[x].push(r);
        }
    }

    let mut result = ((0, 0, 1), get_grid_power_level(&0, &0, serial, &1));
    for size in 1..301 {
        for x in 1..(301 - size) {
            for y in 1..(301 - size) {
                let level = dynamic[x - 1 + size][y - 1 + size] + dynamic[x - 1][y - 1]
                    - dynamic[x - 1][y - 1 + size]
                    - dynamic[x - 1 + size][y - 1];
                if level > result.1 {
                    result = ((x, y, size), level);
                }
            }
        }
    }
    result.0
}

fn get_grid_power_level(x: &usize, y: &usize, serial: &usize, size: &usize) -> isize {
    let mut result = 0;
    for x_ in 0..*size {
        for y_ in 0..*size {
            result += get_power_level(&(x + x_), &(y + y_), serial);
        }
    }
    result
}

fn get_power_level(x: &usize, y: &usize, serial: &usize) -> isize {
    (((x + 10) * y + serial) * (x + 10) / 100 % 10) as isize - 5
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solve_part1() {
        assert_eq!(solve_part1(&18), (33, 45));
        assert_eq!(solve_part1(&42), (21, 61));
    }

    #[test]
    fn test_solve_part2() {
        assert_eq!(solve_part2(&18), (90, 269, 16));
        assert_eq!(solve_part2(&42), (232, 251, 12));
    }

    #[test]
    fn test_power_level() {
        assert_eq!(get_power_level(&3, &5, &8), 4);
        assert_eq!(get_power_level(&122, &79, &57), -5);
        assert_eq!(get_power_level(&217, &196, &39), 0);
        assert_eq!(get_power_level(&101, &153, &71), 4);
        assert_eq!(get_grid_power_level(&33, &45, &18, &3), 29);
        assert_eq!(get_grid_power_level(&21, &61, &42, &3), 30);
    }
}
