"use strict";
// Basic Function with type 
function add(a, b) {
    return a + b;
}
// optional parameter
function greet(name, greeting) {
    if (greeting) {
        return `${greeting}, ${name}`;
    }
    return `hello, ${name}!`;
}
// default parameter
function multiply(n1, n2 = 1) {
    return n1 * n2;
}
//Rest Function
function sum(...numbers) {
    return numbers.reduce((total, n) => total + n, 0);
}
const division = (a, b) => a / b;
let calculate;
calculate = add;
