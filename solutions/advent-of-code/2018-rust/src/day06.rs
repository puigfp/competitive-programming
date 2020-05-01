use std::cmp::{max, min};
use std::collections::{HashMap, HashSet};
use std::error::Error;
use std::fs::read_to_string;
use std::iter::Iterator;

#[macro_use]
extern crate lazy_static;

extern crate regex;
use regex::Regex;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_to_string("input/day6")?;
    let points: Vec<Point> = input
        .lines()
        .map(|s| parse_line(s))
        .collect::<Result<Vec<Point>, Box<dyn Error>>>()?;

    println!("part 1: {}", solve_part1(&points)?);
    println!("part 2: {}", solve_part2(&points, &10000)?);
    Ok(())
}

type Point = (isize, isize);

fn solve_part1(points: &[Point]) -> Result<usize, Box<dyn Error>> {
    let ((x_min, x_max), (y_min, y_max)) = get_limits(points.iter()).ok_or("empty input")?;

    let mut ownerships: HashMap<Point, usize> = HashMap::new();
    let mut blacklist: HashSet<Point> = HashSet::new();
    for x in x_min..=x_max {
        for y in y_min..=y_max {
            let closest = get_closest(&(x, y), points.iter());
            if let Some(c) = closest {
                if x == x_min || x == x_max || y == y_min || y == y_max {
                    blacklist.insert(c);
                } else {
                    ownerships.insert(c, 1 + ownerships.get(&c).unwrap_or_else(|| &0));
                }
            }
        }
    }

    Ok(*ownerships
        .iter()
        .filter(|(k, _)| blacklist.get(&k) == None)
        .max_by(|(_, v1), (_, v2)| v1.cmp(&v2))
        .ok_or("fail")?
        .1)
}

fn solve_part2(points: &[Point], limit: &usize) -> Result<usize, Box<dyn Error>> {
    // this is wrong, there is no reason that all the points we're searching for are in this area
    let ((x_min, x_max), (y_min, y_max)) = get_limits(points.iter()).ok_or("empty input")?;

    let mut area: usize = 0;
    for x in x_min..=x_max {
        for y in y_min..=y_max {
            if is_ok(&(x, y), points.iter(), limit) {
                area += 1;
            }
        }
    }

    Ok(area)
}

lazy_static! {
    static ref regexp: Regex = Regex::new(r"^(\d+), (\d+)$").unwrap();
}

fn parse_line(s: &str) -> Result<Point, Box<dyn Error>> {
    let caps = regexp.captures(s).ok_or("parsing")?;
    Ok((
        caps.get(1).ok_or("failed to parse")?.as_str().parse()?,
        caps.get(2).ok_or("failed to parse")?.as_str().parse()?,
    ))
}

fn get_sum_distances<'i, I>(p: &Point, iter: I) -> isize
where
    I: Iterator<Item = &'i Point>,
{
    iter.map(|p1| d(p, p1)).sum::<isize>()
}

fn is_ok<'i, I>(p: &Point, iter: I, limit: &usize) -> bool
where
    I: Iterator<Item = &'i Point>,
{
    (get_sum_distances(p, iter) as usize) < *limit
}

fn get_closest<'i, I>(p: &Point, iter: I) -> Option<Point>
where
    I: Iterator<Item = &'i Point>,
{
    let mut min_dist = None;
    let mut min_p = None;

    for p1 in iter {
        match min_dist {
            None => {
                min_dist = Some(d(p, p1));
                min_p = Some(*p1);
            }
            Some(dist) => {
                let new_dist = d(p, p1);
                if new_dist == dist {
                    min_p = None;
                } else if new_dist < dist {
                    min_dist = Some(new_dist);
                    min_p = Some(*p1);
                }
            }
        }
    }

    min_p
}

fn get_limits<'i, I>(mut iter: I) -> Option<((isize, isize), (isize, isize))>
where
    I: Iterator<Item = &'i Point>,
{
    match iter.next() {
        Some(p) => Some(
            iter.fold((*p, *p), |((x_min, x_max), (y_min, y_max)), (x, y)| {
                (
                    (min(x_min, *x), max(x_max, *x)),
                    (min(y_min, *y), max(y_max, *y)),
                )
            }),
        ),
        None => None,
    }
}

fn d(p1: &Point, p2: &Point) -> isize {
    (p1.0 - p2.0).abs() + (p1.1 - p2.1).abs()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solve_part1() -> Result<(), Box<dyn Error>> {
        assert_eq!(
            solve_part1(&vec![(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)])?,
            17,
        );
        Ok(())
    }

    #[test]
    fn test_solve_part2() -> Result<(), Box<dyn Error>> {
        assert_eq!(
            solve_part2(&vec![(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)], &32)?,
            16,
        );
        Ok(())
    }

    #[test]
    fn test_parse_line() -> Result<(), Box<dyn Error>> {
        assert_eq!(parse_line("1, 1").unwrap(), (1, 1));
        assert_eq!(parse_line("1, 2").unwrap(), (1, 2));
        parse_line("1,1").unwrap_err();
        Ok(())
    }

    #[test]
    fn test_get_sum_distances() -> Result<(), Box<dyn Error>> {
        assert_eq!(
            get_sum_distances(
                &(4, 3),
                vec![(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)].iter()
            ),
            30,
        );
        Ok(())
    }

    #[test]
    fn test_get_closest() {
        let cases = vec![
            (vec![(0, 0), (0, 1)], (0, 0), Some((0, 0))),
            (vec![(0, 0), (0, 1), (1, 0)], (0, 0), Some((0, 0))),
            (vec![(1, 0), (0, 1)], (0, 0), None),
        ];
        for (points, p, c) in cases {
            assert_eq!(get_closest(&p, points.iter()), c);
        }
    }

    #[test]
    fn test_d() {
        let cases = vec![
            (((0, 0), (0, 0)), 0),
            (((0, 1), (0, 0)), 1),
            (((2, 0), (0, 2)), 4),
        ];
        for ((p1, p2), e) in cases {
            assert_eq!(d(&p1, &p2), e);
        }
    }

    #[test]
    fn test_get_limits() {
        let v = vec![(1, 1), (2, 0), (-1, 0), (0, 2)];
        assert_eq!(get_limits(v.iter()), Some(((-1, 2), (0, 2))));
    }
}
