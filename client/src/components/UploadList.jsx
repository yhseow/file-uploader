import { useState, useEffect } from 'react'
import axios from "axios";

function UploadList() {
  const [array, setArray] = useState([]);

  const fetchAPI = async () => {
    const response = await axios.get("http://localhost:8000/upload-files");
    console.log(response.data);
    setArray(response.data);
  };

  useEffect(()=> {
    fetchAPI();
  }, []);


  const deleteFile= (input_id) => {
    console.log(input_id);
    fetch('http://localhost:8000/upload-file/' + input_id, { method: 'DELETE'}).then(()=> fetchAPI())
  }
  return (
    <div>
        {array.map((f, index) => (
            <div key={index}>
            <span>{f.old_name}</span>, 
            <span>{f.create_date}</span>, 
            <span>{f.type}</span>
            <button key={f.id} onClick={(e) => {
                deleteFile(f.id);
            }}>Delete</button>

            <a href={"http://localhost:8000/download-file?input_id=" + f.id}>Download</a>
            </div>
        ))}
    </div>
  )
}

export default UploadList
