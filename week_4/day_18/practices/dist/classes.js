"use strict";
class Person {
    constructor(name, age, email) {
        this.name = name;
        this.age = age;
        this.email = email;
    }
    introduce() {
        return `Hi, I'm ${this.name} and I'm ${this.age} years old.`;
    }
    getName() {
        return this.name;
    }
    setName(name) {
        this.name = name;
    }
}
class Employee {
    constructor(id, name, department) {
        this.id = id;
        this.name = name;
        this.department = department;
    }
    getDetails() {
        return `${this.name} works in ${this.department}`;
    }
}
let chan = new Employee(1, "Chandru", "Intern");
console.log(chan.getDetails());
