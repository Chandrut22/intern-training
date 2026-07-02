// traditional object type annotation

let user:{name:string, age:number} = {
    name:"Chan",
    age:27,
};

//Interface

interface User{
    name: string;
    age: number;
    email ?: string; // optional property
    readonly id : number // readonly property
}

let user1:User = {
    id:1,
    name:"Chan",
    age:27,
};

// user1.id = 2;

// Interface with methods
interface Product{
    name: string;
    price: number;
    getDiscount(percentage : number) : number; 
}

let laptop: Product = {
    name : "Macbook Pro",
    price : 2000,
    getDiscount(percentage){
        return this.price * (percentage/100);
    }
}