interface Rankcard { 
    name: string,
    pass: "pass" | "fail"
}


interface Rank{
    lists : Rankcard[]
}



function List({lists} : Rank){
    const listItem = lists.map((l) => <li style={{color: l.pass=='pass' ? 'green': 'red'}}>{l.name} - {l.pass}</li>);
    return (<ul>{listItem}</ul>)
}

export default List;