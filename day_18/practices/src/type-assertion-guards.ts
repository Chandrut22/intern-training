// Type assertion
let someValue : unknown = "Chandru";
let strlength : number = (someValue as string).length;
let strlength2 : number = (<string> someValue).length;

// Type Guards 
function processValue(value: string | number){
    if(typeof value === "string"){
        console.log(value.toLowerCase())
    }else{
        console.log(value.toFixed(2))
    }
}

// instanceof type guard
class Dog{
    bark(){
        console.log("Woof !!!");
    }
}

class Cat{
    meow(){
        console.log("Meow !!!");
    }
}

function makeSound(animal : Cat | Dog){
    if (animal instanceof Dog){
        animal.bark()
    }else{
        animal.meow()
    }
}