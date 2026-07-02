"use strict";
// Type assertion
let someValue = "Chandru";
let strlength = someValue.length;
let strlength2 = someValue.length;
// Type Guards 
function processValue(value) {
    if (typeof value === "string") {
        console.log(value.toLowerCase());
    }
    else {
        console.log(value.toFixed(2));
    }
}
// instanceof type guard
class Dog {
    bark() {
        console.log("Woof !!!");
    }
}
class Cat {
    meow() {
        console.log("Meow !!!");
    }
}
function makeSound(animal) {
    if (animal instanceof Dog) {
        animal.bark();
    }
    else {
        animal.meow();
    }
}
