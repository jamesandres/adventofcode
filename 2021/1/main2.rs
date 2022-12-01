// use std::env;
use std::fs;

fn main() {
    let mut num_increases = 0;
    let mut prev_window: [i32; 3] = [i32::MAX, i32::MAX, i32::MAX];

    let contents = fs::read_to_string("input.txt").expect("Something went wrong reading the file");
    let rows: Vec<i32> = contents
        .split("\n")
        .map(|s| string_to_i32(s.to_string()))
        .collect();

    for window in rows.windows(3) {
        if prev_window[0] != i32::MAX {
            let window_sum: i32 = window.iter().sum();
            let prev_window_sum: i32 = prev_window.iter().sum();

            println!("window: {:?} -> {}", window, window_sum);
            println!("prev_window: {:?} -> {}", prev_window, prev_window_sum);

            if window_sum > prev_window_sum {
                println!("... INCREASE!");
                num_increases += 1;
            } else {
                println!("...");
            }
        } else {
            println!("... SKIP FIRST");
        }

        prev_window[0] = window[0];
        prev_window[1] = window[1];
        prev_window[2] = window[2];
    }

    println!("{}", num_increases);
}

fn string_to_i32(string: String) -> i32 {
    return match string.parse::<i32>() {
        Ok(number) => number,
        Err(..) => -1,
    };
}
