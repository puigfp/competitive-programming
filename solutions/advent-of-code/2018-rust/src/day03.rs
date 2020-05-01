use std::cmp;
use std::collections;
use std::error::Error;
use std::fs::read_to_string;

#[macro_use]
extern crate lazy_static;

extern crate regex;

use regex::Regex;

fn main() -> Result<(), Box<dyn Error>> {
    let content = read_to_string("input/day3")?;

    let rectangles: Vec<Rectangle> = content
        .lines()
        .map(parse_line)
        .collect::<Result<Vec<Rectangle>, Box<dyn Error>>>()?;

    println!("part 1: {}", solve_part1(&rectangles));
    println!("part 2: {}", solve_part2(&rectangles).ok_or("fail")?);

    Ok(())
}

fn solve_part1(v: &Vec<Rectangle>) -> usize {
    let mut intersections: Vec<Rectangle> = Vec::new();

    // compute intersections
    for (i, r1) in v.iter().enumerate() {
        for (j, r2) in v.iter().enumerate() {
            if j >= i {
                break;
            }
            let intersection = get_intersection(r1, r2);
            match intersection {
                Some(r) => intersections.push(r),
                None => (),
            }
        }
    }

    let mut overlaps: collections::HashSet<(isize, isize)> = collections::HashSet::new();

    for int in intersections {
        for i in (int.0).0..(int.1).0 {
            for j in (int.0).1..(int.1).1 {
                overlaps.insert((i, j));
            }
        }
    }

    overlaps.len()
}

fn solve_part2(v: &Vec<Rectangle>) -> Option<usize> {
    'outer: for (i, r1) in v.iter().enumerate() {
        'inner: for (j, r2) in v.iter().enumerate() {
            if i == j {
                continue 'inner;
            }
            match get_intersection(r1, r2) {
                Some(_) => continue 'outer,
                None => (),
            }
        }
        return Some(i + 1);
    }
    None
}

lazy_static! {
    static ref regexp: Regex = Regex::new(r"^#\d+ @ (\d+),(\d+): (\d+)x(\d+)$").unwrap();
}

fn parse_line(line: &str) -> Result<Rectangle, Box<dyn Error>> {
    let caps = regexp.captures(&line).ok_or("parsing")?;
    let x1: isize = caps.get(1).ok_or("parsing")?.as_str().parse()?;
    let y1: isize = caps.get(2).ok_or("parsing")?.as_str().parse()?;
    let x2: isize = x1 + caps.get(3).ok_or("parsing")?.as_str().parse::<isize>()?;
    let y2: isize = y1 + caps.get(4).ok_or("parsing")?.as_str().parse::<isize>()?;
    Ok(((x1, y1), (x2, y2)))
}

// ((top left corner), (right bottom corner))
type Rectangle = ((isize, isize), (isize, isize));

fn get_area(s: &Rectangle) -> isize {
    ((s.0).0 - (s.1).0) * ((s.0).1 - (s.1).1)
}

fn get_intersection(s1: &Rectangle, s2: &Rectangle) -> Option<Rectangle> {
    let i: Rectangle = (
        (cmp::max((s1.0).0, (s2.0).0), cmp::max((s1.0).1, (s2.0).1)),
        (cmp::min((s1.1).0, (s2.1).0), cmp::min((s1.1).1, (s2.1).1)),
    );

    if (i.0).0 >= (i.1).0 || (i.0).1 >= (i.1).1 {
        return None;
    }

    Some(i)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_line() {
        assert_eq!(parse_line("#1 @ 1,3: 4x4").unwrap(), ((1, 3), (5, 7)));
        parse_line("fewiufhwef").unwrap_err();
    }

    #[test]
    fn test_get_intersection() {
        let cases: Vec<((Rectangle, Rectangle), Option<Rectangle>)> = vec![
            // overlapping rectangles
            ((((1, 1), (3, 3)), ((2, 2), (4, 4))), Some(((2, 2), (3, 3)))),
            ((((2, 1), (6, 4)), ((0, 0), (4, 2))), Some(((2, 1), (4, 2)))),
            (
                (((-2, 1), (6, 4)), ((0, 0), (4, 2))),
                Some(((0, 1), (4, 2))),
            ),
            // included rectangle
            ((((0, 0), (6, 4)), ((1, 0), (2, 2))), Some(((1, 0), (2, 2)))),
            // non-overlapping rectangles
            ((((0, 0), (2, 1)), ((2, 1), (4, 2))), None),
        ];

        for ((r1, r2), i) in cases {
            assert_eq!(get_intersection(&r1, &r2), i);
        }
    }

    #[test]
    fn test_get_area() {
        let cases: Vec<(Rectangle, isize)> = vec![((((0, 0), (1, 1))), 1), (((-1, -2), (0, 1)), 3)];

        for (r, a) in cases {
            assert_eq!(get_area(&r), a);
        }
    }

    #[test]
    fn test_solve_part1() {
        let v = vec![
            ((1, 3), (5, 7)),
            ((3, 1), (7, 5)),
            ((5, 5), (7, 7)),
            ((3, 3), (5, 5)),
        ];
        assert_eq!(solve_part1(&v), 4);
    }

    #[test]
    fn test_solve_part2() {
        let v = vec![((1, 3), (5, 7)), ((3, 1), (7, 5)), ((5, 5), (7, 7))];
        assert_eq!(solve_part2(&v), Some(3));
    }
}
