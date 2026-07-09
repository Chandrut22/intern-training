interface Todo {
    id: number;
    title: string;
    description: string;
    completed: boolean;
}


export type UpdateTaskPayload = {
  title: string;
  description: string;
  is_competed: boolean; 
};


export async function getTodos(): Promise<Todo[]> {
    const response = await fetch("http://127.0.0.1:8000/tasks");

    console.log(response);

    if (!response.ok) {
        throw new Error("Failed to fetch todos");
    }

    const data = await response.json();

    console.log(data);

    return data;
}


export async function getTodoById(id: number) {
    const response = await fetch(`http://127.0.0.1:8000/tasks/${id}`);

    if (!response.ok) {
        throw new Error("Task not found");
    }

    return response.json();
}


export async function createTodo(data: {
    title: string;
    description: string;
    is_competed : boolean;
}) {
    const response = await fetch("http://127.0.0.1:8000/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        throw new Error("Failed to create task");
    }

    return response.json();
}


export async function updateTodo(id: number, data: UpdateTaskPayload) {
    console.log("API Func")
    console.log(data)
    const response = await fetch(`http://127.0.0.1:8000/task/${id}`, {
        method: "PUT",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        throw new Error("Update failed");
    }

    return response.json();
}

export async function deleteTodo(id: number) {
    const response = await fetch(`http://127.0.0.1:8000/task/${id}`, {
        method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Delete failed");
    }

    return response.json();
}