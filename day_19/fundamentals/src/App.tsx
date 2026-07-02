import { useState } from 'react'
import Card  from './components/Card'
import List from './components/List'

function App() {
  const [count, setCount] = useState(0)

  const ranklist = [
    {name:"Chandru", pass:"pass" as const},
    {name:"Hari", pass:"fail" as const},
    {name:"Dhanush", pass:"pass" as const},
    {name:"AkilRaj", pass:"fail" as const},

  ]

  return (
    <>  
        <div>
          <h4>Countor count is: {count}</h4>
        </div>
        <button type="button" onClick={() => setCount((count) => count + 1)}>
          Increment
        </button>

        <button type="button" onClick={() => setCount((count) => count - 1)}>
          Decrement
        </button>


        <Card {...{title:"Tree", description:"Living thing"}}/>
        <Card {...{title:"Car", description:"Non - Living thing"}}/>
        <Card {...{title:"Animals", description:"Living thing"}}/>

        <List lists={ranklist}/>

        
    </>
  )
}

export default App
