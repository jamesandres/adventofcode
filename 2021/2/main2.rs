use std::fs;

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Something went wrong reading the file");
    let rows: Vec<(String, u8)> = contents
        .split("\n")
        .filter(|&s| !s.is_empty())
        .map(|s| string_to_instructions(s.to_string()))
        .collect();

    let mut horizontal: u16 = 0;
    let mut depth: u32 = 0;
    let mut aim: u16 = 0;

    for (direction, magnitude) in rows {
        match direction.as_str() {
            "forward" => {
                horizontal += magnitude as u16;
                depth += aim as u32 * magnitude as u32;
            }
            "down" => aim += magnitude as u16,
            "up" => aim -= magnitude as u16,
            _ => (),
        }
    }

    let mult: u32 = horizontal as u32 * depth;
    println!("{}", mult);
}

fn string_to_instructions(string: String) -> (String, u8) {
    let parts: Vec<&str> = string.split_whitespace().collect();
    return (parts[0].to_string(), string_to_u8(parts[1].to_string()));
}

fn string_to_u8(string: String) -> u8 {
    return string.parse::<u8>().unwrap();
}
