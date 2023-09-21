import React, { useState } from 'react';
import axios from 'axios';

function UploadFile() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/anonimizar_dicom', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Arquivo enviado com sucesso');
      // Você pode acessar a resposta da API Flask aqui
      console.log('Resposta da API:', response.data);
      setResponse(response.data); // Armazene a resposta em um estado
    } catch (error) {
      console.error('Erro ao enviar o arquivo', error);
    }
  };

  return (
    <div>
      <h2>Envie um arquivo DICOM:</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Enviar</button>
      </form>

      {/* Exibir a resposta da API, se houver */}
      {response && (
        <div>
          <h2>Resposta da API:</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default UploadFile;
