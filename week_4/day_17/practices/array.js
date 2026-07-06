let a = [];
console.log(a);

let b = [10,20,30];
console.log(b);

let c = new Array(10, 20, 30);
console.log(c);

let arr = ["HTML", "CSS", "JS"];
console.log(arr[0], arr[arr.length-1]);

arr[1] = "Bootstrap"
console.log(arr)

arr.push("Node.js")
arr.unshift("React")

console.log(arr)


let lst = arr.pop()
let fst = arr.shift()
arr.splice(1,2)

console.log(arr)

arr = ["HTML", "CSS", "JS", "React"];

for(let i=0;i<arr.length;i++){
    console.log(arr[i]);
}

arr.forEach(function myfunc(element){
    console.log(element);
});

let arr1 = ["HTML", "CSS", "JS", "React"];
let arr2 = ["Node.js", "Express.js"];

let concateArray = arr1.concat(arr2);

console.log("Concatenated Array: ", concateArray);

console.log(concateArray.toString());

// -----------------------------------------------------------------------------------------------------------------------------------
arr = [1,2,3,4,5];

arr.forEach(element => {
    console.log(element);
})

squareArr = [];
let items = [1,29,47];
items.forEach(item => {
    squareArr.push(item * item);
});

console.log(squareArr);

// ------------------------------------------------------------------------------------------------------------------------------------------

arr = [1,2,3,4,5];
let sq = arr.map(x => x*2)
console.log(sq);

let sqrt = arr.map(num => Math.sqrt(num))

console.log(sqrt);


arr = ['1','2','3','4']
let number = arr.map(n => parseInt(n))
console.log(number)


// ------------------------------------------------------------------------------------------------------------------------------------------------

function canVote(num){
    return num >= 18;
}

let filterArr = [18,13,21,34,17].filter(canVote);

console.log(filterArr)

function isPostive(value){
    return 0 < value;
}

filterArr = [-1,33,24,456,0,-13].filter(isPostive);
console.log(filterArr)


// ---------------------------------------------------------------------------------------------------------------------------------------------