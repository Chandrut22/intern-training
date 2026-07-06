"use strict";
// traditional object type annotation
let user = {
    name: "Chan",
    age: 27,
};
let user1 = {
    id: 1,
    name: "Chan",
    age: 27,
};
let laptop = {
    name: "Macbook Pro",
    price: 2000,
    getDiscount(percentage) {
        return this.price * (percentage / 100);
    }
};
