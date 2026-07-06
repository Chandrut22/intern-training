interface Data {
    title : string,
    description: string
}

const style = {
    card : {padding: '10px', border:'2px solid', width:'300px', margin:'10px'}
}

function Card(data : Data){
    return(
            <div className="card" style={style.card}>
                <h1>Title: {data.title}</h1>
                <p>Description: {data.description}</p>
            </div>
    )
}

export default Card;