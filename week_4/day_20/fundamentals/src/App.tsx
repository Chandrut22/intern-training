import { useState } from 'react'
import Card  from './components/Card'
// import List from './components/List'
import {Form} from './components/Form'
function App() {
  const [count, setCount] = useState(0)

  // const ranklist = [
  //   {name:"Chandru", pass:"pass" as const},
  //   {name:"Hari", pass:"fail" as const},
  //   {name:"Dhanush", pass:"pass" as const},
  //   {name:"AkilRaj", pass:"fail" as const},

  // ]

  return (
    <>  
        <div className="flex justify-center py-10">
          <div className="rounded-4xl bg-blue-200 p-10">
            <h4 className="py-10 text-center font-semibold">Countor count is: {count}</h4>
            <div className="flex justify-between gap-5">
                <button className='rounded-xl bg-blue-500 px-8 py-5 text-white hover:bg-blue-600' type="button" onClick={() => setCount((count) => count + 1)}>
                  Increment
                </button>

                <button className='rounded-xl bg-blue-500 px-8 py-5 text-white hover:bg-blue-600' type="button" onClick={() => setCount((count) => count - 1)}>
                  Decrement
                </button>
            </div>
          </div>
        </div>
          
        <div className="flex flex-wrap justify-center-safe gap-5">
            <Card {...{title:"Tree", description:"Living thing"}}/>
            <Card {...{title:"Car", description:"Non - Living thing"}}/>
            <Card {...{title:"Animals", description:"Living thing"}}/>
            <Card {...{title:"Sengan", description:"Living thing"}} />
        </div>

        {/* <div className="m-10 bg-gray-300 rounded-3xl">
              <List lists={ranklist}/>
        </div> */}


         <div className="rounded-4xl bg-blue-200 p-5 m-10">
          <Form/>
         </div>

        

        
    </>
  )
}

export default App
