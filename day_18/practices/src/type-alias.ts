// Type alias
type Point = {
    x:number;
    y:number;
};

let point: Point = {x:10, y:20};

// type alias with different datatypes
type ID = string | number;

let userId : ID = "Chan123";
let prodId : ID = 123;

// type vs interface 

// interface can be extended, type aliases cannot 
interface Car{
    name : string;
}

interface Car_Model extends Car{
    model_name: string;
    price:number;
}

let model_car: Car_Model = {
    name: "Laptop",
    model_name: "Lenovo",
    price: 70000,
}

// Interface can be declared multiple time and will merge

interface Person1{
    name: String
}

interface Person1{
    age: Number
}

let p: Person1 = {
    name: "Chandru",
    age: 22,
}

// Use Interface for shape object 
// type aliases for union/ intersections 