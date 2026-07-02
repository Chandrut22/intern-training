// Basic Function with type 
function add(a:number, b:number): number{
    return a+b;
}

// optional parameter
function greet(name:string, greeting?:string): string{
    if(greeting){
        return `${greeting}, ${name}`;
    }
    return `hello, ${name}!`;
}

// default parameter
function multiply(n1: number,n2: number = 1): number{
    return n1*n2
}

//Rest Function
function sum(...numbers: number[]): number{
    return numbers.reduce((total,n) => total+n,0)
}

// Arrow function 
const division = (a:number, b:number):number => a/b;
// Function type
let calculate: (x:number, y:number) => number;
calculate = add;
