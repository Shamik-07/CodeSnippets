fn main() {
    // just printing hello world
    println!("Hello, Rust from CARGO! \n");

    // different data types
    println!("Different simple data types! \n");
    let x: i32 = -70;
    let y: u64 = 345;
    println!("Signed integer:{}", x);
    println!("Unsigned integer:{}", y);
    let y: f64 = 345.89898;
    println!("Signed floating point:{}", y);
    let y: f64 = -345.89898;
    println!("Negative signed floating point:{}", y);
    let y: bool = true;
    println!("Boolean data type:{}", y);
    let y: char = 'a';
    println!("A single character data type. \
        Notice the single quote.:{}", y);
    let y: &str = "abc";
    println!("A string data type. \
        Notice the double quotes:{}", y);

    // compound data types
    println!("\nDifferent compound data types!\n");

    println!("Arrays must contain homogenous data types.\n");

    let some_numbers: [i32; 5] = [1,2,3,4,5];
    println!("An array of EXACTLY 5 numbers: {:?}. \
    This cannot hold more/less than 5 numbers.", some_numbers);

    println!("This array contains 5 integers and can contain \
    only integers because we have defined it such. \
    It cannot contain any other data type. \
    To print this array one needs to use a different \
    formatter i.e. a debugging formatter {{:?}}. \
    Notice the question mark inside the formatter.");

    let some_numbers = [1,2,3];
    println!("\n An array without any pre-defined size and\
        without pre-defined data type: {:?} \n", some_numbers);

    let some_strings: [&str; 3] = ["ab","abc","123"];
    println!("An array of strings: {:?}. \
    This cannot hold more/less than 3 strings.", some_strings);
    println!("\n We can also print the first element: \
    {}",some_strings[0]);
    
    let only_str:[String;1] = ["asdsa".to_string()];
    println!("\n An array of string: {:?}", only_str); 

    println!("\n To have mixed data types, one can use 
        tuples. Either you can define the tuple data types
        or leave it empty. Below is a tuple with pre-defined 
        data types");

    let some_tuple: (&str, i32, bool) = ("bob", 234, true);
    println!("A tuple containing different data types: {:?}. \
    Notice that the data types must be enclosed in ().", 
        some_tuple);

    println!("\n Tuples can even have compound data types such \
        as arrays.");

    let some_tuple = ("bob", 234, true, [1,2,3,4]);

    println!("A tuple containing compound data types: {:?}. \
    One doesn't need to pre-define the data types always.", 
        some_tuple);

    
    // slices

    let some_numbers:&[i32] = &[1,2,3,4,5];
    println!("\n An array with pre-defined data type and it's a slice \
        as it has a {{&}} outside the array and outside the \
        data type definition. The advantage of such as slice is that it \
        has stored all the numbers contiguously: {:?} \n", some_numbers);

    let str_slices:&[&str] = &["asd", "asdasd", "eee"];
    println!("\n This is a string slice: {:?}. \
        This can refer to a part of the string, for instance \
        n chars or more of the string.", str_slices);

    let only_str:&[&String] = &[&"asd".to_string(), 
    &"bbfgdfg".to_string()];
    println!("\n This is a reference string: {:?}.\
        This refers to the entire string and not part of the string. \
        Slicing isn't allowed here.", only_str); 

    // Strings vs strings slices
    // Strings are growable, mutable i.e. push and delete data
    


}
