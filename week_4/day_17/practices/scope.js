

// Declaring a global variable
// Global Variable accessed from within a function 
const x1 = 10;

function fun1() {
    console.log(x1);
}

fun1();

function fun2(){
    
    // This variable is local to fun2() and 
    // cannot be accessed outside this function
    let x2 = 10;
    console.log(x2);
}

fun2();


{
    
    // Var can Accessible inside & outside the block scope 
    var xg = 10;
    
    // let , const Accessible only inside the block scope
    const y = 20;
    let z = 30;
    
    console.log(xg);
    console.log(y);
    console.log(z);
}

console.log(xg);

// (module file)
export const number = 10;

export function add(a, b) {
  return a + b;
}
