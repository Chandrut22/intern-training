function greet() { // Named Function
  return "Hello!";
}
console.log(greet());


const greet = function() { // anonymous function
  return "Hi there!";
};
console.log(greet());


const add = function(a, b) { //function expression
  return a + b;
};
console.log(add(2, 3));

const square = n => n * n; // Arrow Function
console.log(square(4));


(function () { // Immediately Invoked Function Expression
    console.log("This runs immediately!");
})();

function outerFun(a) { // nested Function
    function innerFun(b) {
        return a + b;
    }
    return innerFun;
}

const addTen = outerFun(10);
console.log(addTen(5));