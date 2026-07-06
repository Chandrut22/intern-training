class Person{
    private name: string;
    protected age : number;
    public email: string;

    constructor(name: string, age:number, email:string){
        this.name = name;
        this.age = age;
        this.email = email
    }

    public introduce() : string {
        return `Hi, I'm ${this.name} and I'm ${this.age} years old.`;
    }

    public getName(): string{
        return this.name;
    }

    public setName(name:string): void{
        this.name = name;
    }
}

class Employee{
    constructor(
        private id: number,
        public name: string,
        protected department: string,
    ){}

    getDetails(): string {
        return `${this.name} works in ${this.department}`
    }
}


let chan = new Employee(1,"Chandru","Intern");
console.log(chan.getDetails())


class Manager extends Employee{
    constructor(
        id:number,
        name:string,
        department:string,
        private teamSize: number,
    ){
        super(id,name,department)
    }

    getTeamInfo(): string{
        return `${this.name} manages ${this.teamSize} people`;
    }
}