import { useState, useEffect } from 'react'
import { useNavigate } from "react-router-dom";

function UploadFile() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  
  const handleFileChange = (e) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (file) {
      console.log('Uploading file...');
  
      const formData = new FormData();
      formData.append('file', file);
  
      try {
        // You can write the URL of your server or any other endpoint used for file upload
        const result = await fetch('http://localhost:8000/upload-file?type=INPUT&parent_id=0', {
          method: 'POST',
          body: formData,
        });
  
        const data = await result.json();
  
        console.log(data);

        setFile(null);
        navigate('/list')
      } catch (error) {
        console.error(error);
      }
    }
  };
  
  return (
    <div>
        <div className="input-group">
            <input id="file" type="file" onChange={handleFileChange} />
        </div>
        <p>
            {file && (
            <section>
                File details:
                <ul>
                <li>Name: {file.name}</li>
                <li>Type: {file.type}</li>
                <li>Size: {file.size} bytes</li>
                </ul>
            </section>
            )}
        </p>

        {file && (
        <button 
            onClick={handleUpload}
            className="submit"
        >Upload a file</button>
        )}
    </div>
  )
}

export default UploadFile
