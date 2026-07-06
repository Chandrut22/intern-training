interface Data {
    title : string,
    description: string
}

function Card(data : Data){
    return(
            <div className="rounded-2xl bg-green-200 p-5 text-center text-[18px]">
                <h1><span className="font-semibold">Title: </span> {data.title}</h1>
                <p><span className="font-semibold">Description: </span>{data.description}</p>
            </div>
    )
}

export default Card;