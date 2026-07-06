// let: Block-scoped and can be reassigned.
// var: Function-scoped and can be reassigned.
// const: Block-scoped and cannot be reassigned.
// let vs var: let is safer because it's block-scoped, unlike var.
// const: Used for values that shouldn’t change, but objects/arrays inside can still change.


import { number, add } from "./scope";

console.log(number);      
console.log(add(5, 3));

if(true){
    var a = 1; // global Scope
    let b = 2;
    const c = 3;
}


console.log(a);
// console.log(b);
// console.log(c); both let and const is block

console.log(x);
var x =5;

// console.log(y) 
let y=10

// console.log(z)
const z=10


let c;
console.log(c)
c = 5;
console.log(c)


// const d;
// console.log(c)
// d = 5;
// console.log(c)  remains uninitialized until its declaration is evaluated.


const numbers = [1, 2, 3]; // The const declaration makes the reference to the numbers array constant, but its contents can still be modified. 
numbers.push(4);  
console.log(numbers);  
// numbers = [5, 6];


const person = { name: "Pranjal", age: 30 }; // The const declaration makes the reference to the person object constant, but its properties can be modified.
person.age = 31;  
console.log(person); 
// person = { name: "Nanda" };
