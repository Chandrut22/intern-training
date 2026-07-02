// Union types (OR)
type Status = "pending" | "approved" | "rejected"
type dataType = "Chan" | false | 22

function setStatus(status: Status): void{
    console.log(`Status set to: ${status}`);
}

setStatus("approved")


//Intersection type (AND)
interface Colorful { 
    color: String;
}

interface Circle {
    radius: number;
}

type ColorfulCircle = Colorful & Circle

let mycircle : ColorfulCircle = {
    color : "red",
    radius : 10,
}