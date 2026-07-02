"use strict";
// primitive data-type 
let username = "Chandru";
let age = 22;
let isAdmin = true;
// Array
let arr = [1, 2, 3, 4, 5];
let names = ["Chan", "Sai", "Snegan"];
//Tuples
let tuple = ["Chan", 12];
//Enum
var Color;
(function (Color) {
    Color[Color["Red"] = 0] = "Red";
    Color[Color["Blue"] = 1] = "Blue";
    Color[Color["Green"] = 2] = "Green";
})(Color || (Color = {}));
let favColor = Color.Blue;
//Any
let random;
random = "Chan";
random = 22;
//Unknown (safer than any)
let userinput;
userinput = 4;
userinput = "Chan";
function ing(msg) {
    console.log("Hello EveryOne");
}
let ch = "Chan";
// ch = 5; Type interference
