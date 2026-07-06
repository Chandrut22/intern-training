import { useEffect } from "react";

interface props {
    name : string
}


export const Fun = (p: props) =>{
    useEffect(() => {
    console.log("Mounted");

    return () => {
      console.log("Unmounted");
    };
  }, []);

    return (
        <h1>{p.name}</h1>
    )
}

