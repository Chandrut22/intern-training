// Using literal 

let obj1 = {
    name: "Sourav",
    age: 23,
    job: "Developer"
};
console.log(obj1);


// Using Constructor
let obj2 = new Object();
obj2.name= "Sourav",
obj2.age= 23,
obj2.job= "Developer"

console.log(obj2);

// access
console.log(obj1['age'], " ", obj2.name)

// modify
obj1.age = 22;
console.log(obj1);

// add the properties
let car = { model: "Tesla" };
car.color = "Red";
console.log(car);

// delete the properties
delete car.color;
console.log(car);

// check the property is exist or not 
console.log("color" in car);
console.log(car.hasOwnProperty("model"));


// ierate the object
let detail = {name:"Chandru", age:22}
for(let key in detail){
    console.log(key+" : "+detail[key])
}


let name = {name:"Chandru"};
let age = {age:22};

let d = {...obj1,...obj2}

console.log(d);

console.log(Object.keys(d).length);

console.log(typeof d === "object" && d !== null);