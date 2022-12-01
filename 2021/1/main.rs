// use std::env;
use std::fs;


fn main() {
    let mut num_increases = 0;
    let mut prev_value = 99999999;

    let contents = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let rows = contents.split("\n");

    for string_value in rows {
        let value = match string_value.parse::<i32>() {
            Ok(number)  => number,
            Err(..)     => -1,
        };

        if value > prev_value {
            num_increases += 1;
        }

        prev_value = value;
    }

    println!("{}", num_increases);
}
