import React, { useState, useEffect } from 'react';
import List from './List';

interface UserItem {
  id: number;
  name: string;
  ispass: boolean;
}

export function Form() {
  const [inputs, setInputs] = useState<UserItem>({
    id : 0,
    name : '',
    ispass: true
  });
  
  const [list, setList] = useState<UserItem[]>([]);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    console.log(event);
    const { name, value, checked } = event.target;
    setInputs(values => ({ ...values, [name]: event.type === 'checkbox'? checked : value}));
  };

  const handleSubmit = (event: React.SubmitEvent<HTMLFormElement>) => {
    event.preventDefault();
    
    if (!inputs.name) return;

    const newItem: UserItem = {
      id: Date.now(),
      name: inputs.name,
      ispass: inputs.ispass
    };

    setList(prevList => [...prevList, newItem]);

    setInputs({id:0 ,name: "", ispass: false });
  };

  useEffect(() => {
        if(list.length > 0){
            document.title = `${list[list.length - 1].name} Data is updated`;
        }
}, [list]);

  return (
    <div>
      {/* Form Element */}
      <form onSubmit={handleSubmit}>
        <label>Name: 
          <input type="text" name="name" value={inputs.name} onChange={handleChange} />
        </label>
        <label>
            <input type="checkbox" name="ispass" checked={inputs.ispass} onChange={handleChange}/> Is Pass
        </label>
        <br />
        <button type="submit">Add to List</button>
      </form>
        <List lists={list}/>
      
    </div>
  );
}
