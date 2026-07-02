// primitive data-type 

let username: string = "Chandru";
let age: number = 22;
let isAdmin: boolean = true;

// Array
let arr: number[] = [1,2,3,4,5];
let names: string[] = ["Chan","Sai","Snegan"];


//Tuples
let tuple : [string, number] = ["Chan",12];


//Enum
enum Color{
    Red,
    Blue,
    Green
}

let favColor: Color = Color.Blue;

//Any
let random: any
random = "Chan";
random = 22;


//Unknown (safer than any)
let userinput : unknown;
userinput = 4;
userinput = "Chan"

function ing(msg: string): void{
    console.log("Hello EveryOne");
}


let ch = "Chan";
// ch = 5; Type interference