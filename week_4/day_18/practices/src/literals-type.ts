// String literal types
let direction: "north" | "south" | "east" | "west";
// direction = "chan"
direction = "north"

// numeric literal types
let dice : 1 | 2 | 3 | 4 | 5 | 6;


//Combine with other types
type SuccessResponse = {
    status : "Success",
    data: any
}

type ErrorResponse = {
    status : "error",
    msg : string
}

type ApiResponse = SuccessResponse | ErrorResponse;
