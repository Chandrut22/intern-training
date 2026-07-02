// Generics in TypeScripts

function identify<MyType>(arg: MyType){
    return arg;
}

let o1 = identify<string>("Chandru");
let o2 = identify<number>(100);

//Generic with arrays 
function getFirstElement<T>(arr:T[]): T | undefined{
    return arr[0];
}

let n1 = getFirstElement([1,2,3,4]);
let n2 = getFirstElement(["a","B","c"]);

interface KeyValuePair<K,V>{
    key : K,
    value : V,
}

let strNumPair: KeyValuePair<string,number> = {
    key : "age",
    value: 22
}


// interface generics
interface KeyValuePairComplex <K,V>{
    key : {
        name : string,
        myKey : K
    },
    value : V,
}


let stringNumPair: KeyValuePairComplex<string,number> = {
    key:{
        name : "Chandru",
        myKey : "chan"
    },
    value: 22,
}


//Generics classes 

class DataStorage<T>{
    private data: T[] = [];

    addItem(item: T): void{
        this.data.push(item)
    }

    removeItem(item: T): void{
        this.data = this.data.filter((i) => i !== item);
    }

    getItems(): T[]{
        return [...this.data];
    }
}

let textStorage = new DataStorage<string>();


// Generics Constrains
interface Lengthwise{
    length: number
}


function loglength<T extends Lengthwise>(arg : T): T{
    console.log(arg.length);
    return arg
}

loglength([1,2,3,4])
loglength("Hello")
// loglength(123)