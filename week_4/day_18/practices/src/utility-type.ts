interface ToDo{
    title : string,
    description : string,
    completed: boolean,
    createdAt: Date,
    assignedTo: string,
}

// Partial - makes all into optional properties
type partialToDo = Partial<ToDo>;


// Required - makes all into required properties
type requiredTodo = Required<ToDo>;


// ReadOnly - makes all into readonly properties
type readOnlyTodo = Readonly<ToDo>;


// Pick - picks specifices properties
type ToDoPreview = Pick<ToDo,"title"|"completed">


//Omit - omit the specific properties
type TodoWithoutDate = Omit<ToDo,"createdAt">

//Record - construct the object type with specific key and values

type PageInfo = {
    title : string,
    url : string,
}

type Pages = "home" | "about" | "contact";
type merged = Record<Pages,PageInfo>


let pages : merged = {
    home : { title: "Home" , url : "/"},
    about : { title: "About" , url : "/about"},
    contact : { title: "Contact" , url : "/contact"}
}


//