
//  == -> compares two values after converting them into common type
// === -> compares both values and types without any convertion



// Implicit Type Conversion

console.log(5 + "5");

console.log(true + 1);

console.log(5 == "5");

let res = Boolean("");  
let res2 = Boolean("Hello");  
console.log(res)
console.log(res2)


// Explicit Conversion

let n = 123;
let s1 = String(n);  
let s2 = n.toString();  
console.log(s1)
console.log(s2)


let s = "123";
let n = Number(s);  
let s1 = "12.34";
let n1 = parseFloat(s1);  
console.log(n)
console.log(n1)


let str = "Hello";
let b1 = Boolean(str);  
let emptyStr = "";
let b2 = Boolean(emptyStr);  
console.log(b1)
console.log(b2)