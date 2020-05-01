use std::cmp::Ord;
use std::collections::HashMap;
use std::error::Error;
use std::fs::read_to_string;

#[macro_use]
extern crate lazy_static;

extern crate regex;
use regex::Regex;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_to_string("input/day4")?;

    println!("part 1: {}", solve_part1(&input)?);
    println!("part 2: {}", solve_part2(&input)?);

    Ok(())
}

fn solve_part1(input: &str) -> Result<usize, Box<dyn Error>> {
    let mut events = input
        .lines()
        .map(|line| parse_line(line))
        .collect::<Result<Vec<Event>, Box<dyn Error>>>()?;
    events.sort_by(|a, b| a.etime.cmp(&b.etime));

    let mut sleep: HashMap<usize, usize> = HashMap::new();
    let mut times: HashMap<(usize, usize), usize> = HashMap::new();
    let mut guard = None;
    let mut asleep = None;
    for event in events {
        match (event.etype, guard, asleep) {
            (EventType::Guard(g), _, _) => guard = Some(g),
            (EventType::FallsAsleep, _, _) => asleep = Some(event.etime),
            (EventType::WakesUp, _, Some(t)) => {
                if let Some(g) = guard {
                    let current = match sleep.get(&g) {
                        Some(j) => j + event.etime.4 - t.4,
                        None => event.etime.4 - t.4,
                    };
                    sleep.insert(g, current);
                    for i in t.4..event.etime.4 {
                        let key = (g, i);
                        let current = match times.get(&key) {
                            Some(j) => j + 1,
                            None => 1,
                        };
                        times.insert(key, current);
                    }
                    asleep = None;
                }
            }
            _ => (),
        }
    }

    let guard: &usize = sleep
        .keys()
        .max_by(|a, b| sleep.get(a).cmp(&sleep.get(b)))
        .ok_or("fail")?;

    let time: &usize = times
        .keys()
        .filter(|(a, _)| a == guard)
        .map(|(_, b)| b)
        .max_by(|a, b| times.get(&(*guard, **a)).cmp(&times.get(&(*guard, **b))))
        .ok_or("fail")?;

    Ok(guard * time)
}

fn solve_part2(input: &str) -> Result<usize, Box<dyn Error>> {
    let mut events = input
        .lines()
        .map(|line| parse_line(line))
        .collect::<Result<Vec<Event>, Box<dyn Error>>>()?;
    events.sort_by(|a, b| a.etime.cmp(&b.etime));

    let mut times: HashMap<(usize, usize), usize> = HashMap::new();
    let mut guard = None;
    let mut asleep = None;
    for event in events {
        match (event.etype, guard, asleep) {
            (EventType::Guard(g), _, _) => guard = Some(g),
            (EventType::FallsAsleep, _, _) => asleep = Some(event.etime),
            (EventType::WakesUp, _, Some(t)) => {
                if let Some(g) = guard {
                    for i in t.4..event.etime.4 {
                        let key = (g, i);
                        let current = match times.get(&key) {
                            Some(j) => j + 1,
                            None => 1,
                        };
                        times.insert(key, current);
                    }
                    asleep = None;
                }
            }
            _ => (),
        }
    }

    let (guard, time): &(usize, usize) = times
        .keys()
        .max_by(|a, b| times.get(a).cmp(&times.get(b)))
        .ok_or("fail")?;

    Ok(guard * time)
}

type Time = (usize, usize, usize, usize, usize);

#[derive(Debug, PartialEq)]
enum EventType {
    Guard(usize),
    FallsAsleep,
    WakesUp,
}

#[derive(Debug, PartialEq)]
struct Event {
    etime: Time,
    etype: EventType,
}

lazy_static! {
    static ref full_regexp: Regex =
        Regex::new(r"^\[(\d{4})\-(\d{2})\-(\d{2}) (\d{2}):(\d{2})\] (.*)+$").unwrap();
    static ref guard_regexp: Regex = Regex::new(r"^Guard #(\d+) begins shift$").unwrap();
}

fn parse_line(s: &str) -> Result<Event, Box<dyn Error>> {
    let caps = full_regexp.captures(s).ok_or("parsing")?;

    let time: Time = (
        caps.get(1).ok_or("failed to parse")?.as_str().parse()?,
        caps.get(2).ok_or("failed to parse")?.as_str().parse()?,
        caps.get(3).ok_or("failed to parse")?.as_str().parse()?,
        caps.get(4).ok_or("failed to parse")?.as_str().parse()?,
        caps.get(5).ok_or("failed to parse")?.as_str().parse()?,
    );

    let end = caps.get(6).ok_or("failed to parse")?.as_str();

    let caps = guard_regexp.captures(end);
    if let Some(c) = caps {
        return Ok(Event {
            etime: time,
            etype: EventType::Guard(c.get(1).ok_or("failed to parse")?.as_str().parse()?),
        });
    }

    if end == "falls asleep" {
        return Ok(Event {
            etime: time,
            etype: EventType::FallsAsleep,
        });
    }

    if end == "wakes up" {
        return Ok(Event {
            etime: time,
            etype: EventType::WakesUp,
        });
    }

    Err("failed to parse".into())
}

#[cfg(test)]
mod tests {
    use super::*;

    static INPUT: &str = "[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up";

    #[test]
    fn test_solve_part1() {
        assert_eq!(solve_part1(INPUT).unwrap(), 240);
    }

    #[test]
    fn test_solve_part2() {
        assert_eq!(solve_part2(INPUT).unwrap(), 4455);
    }

    #[test]
    fn test_parse_line() {
        let s = "[1518-11-01 00:00] Guard #10 begins shift";
        assert_eq!(
            parse_line(s).unwrap(),
            Event {
                etime: (1518, 11, 01, 00, 00),
                etype: EventType::Guard(10),
            }
        );

        let s = "[1518-11-01 00:05] falls asleep";
        assert_eq!(
            parse_line(s).unwrap(),
            Event {
                etime: (1518, 11, 01, 00, 05),
                etype: EventType::FallsAsleep,
            }
        );

        let s = "[1518-11-01 00:25] wakes up";
        assert_eq!(
            parse_line(s).unwrap(),
            Event {
                etime: (1518, 11, 01, 00, 25),
                etype: EventType::WakesUp,
            }
        );

        let s = "fewiuhfuewf";
        parse_line(s).unwrap_err();
    }
}
