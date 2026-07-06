// Data Types 
// a) Primitive Data Types
//      i) Numeric Type - Number, bigInt
//      ii) Non Numeric Type - String, Boolean, null, undefined, Symbol
// b) Non - Primitive Data Types - object, array, function

// Number
let n1 = 2;
console.log(n1)

let n2 = 1.3;
console.log(n2)

let n3 = Infinity;
console.log(n3)

let n4 = 'something here too' / 2;
console.log(n4)


//String 

let s1 = "Hello There";
console.log(s1); 

let s2 = 'Single quotes work fine';
console.log(s2); 

let s3 = `can embed ${s1}`;
console.log(s3);


// boolean

let b1 = true;
console.log(b1);  

let b2 = false;
console.log(b2);

// null

let age = null;
console.log(age)

//undefined

let a;
console.log(a)

// Symbol
let sy1 = Symbol("Geeks");
let sy2 = Symbol("Geeks");
console.log(sy1 == sy2);


let gfg = {
    type: "Company",
    location: "Noida"
}
console.log(gfg.type)


let a1 = [1, 2, 3, 4, 5];
console.log(a1);

let a2 = [1, "two", { name: "Object" }, [3, 4, 5]];
console.log(a2);


function greet(name) { return "Hello, " + name + "!"; }
console.log(greet("Ajay"));