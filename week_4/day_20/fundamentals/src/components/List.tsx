export interface Rankcard { 
    id: number,
    name: string,
    ispass: boolean
}

interface RankList{
    lists : Rankcard[]
}


function List({lists} : RankList){
    const listItem = lists.map((l) =>  l.ispass === true ? 
            (<li key={l.id} className=" text-green-700">{l.name} - Pass</li>) : 
            (<li key={l.id} className=" text-red-700">{l.name} - Fail</li>));

    return (<ul className=" py-3 flex-col justify-items-center">{listItem}</ul>)
}

export default List;