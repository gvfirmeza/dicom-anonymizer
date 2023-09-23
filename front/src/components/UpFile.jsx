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
      console.log('Resposta da API:', response.data);
      setResponse(response.data);
    } catch (error) {
      console.error('Erro ao enviar o arquivo', error);
    }
  };

  const renderDownloadLink = () => {
    if (response && response.downloadUrl) {
      return (
        <div>
          <h2>Download do Arquivo Anonimizado:</h2>
          <a href={`http://localhost:5000${response.downloadUrl}`} download="dicom_anonimizado.dcm">
            Baixar Arquivo Anonimizado
          </a>
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      <h2>Envie um arquivo DICOM:</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Enviar</button>
      </form>

      {response && (
        <div>
          {renderDownloadLink()}
        </div>
      )}
    </div>
  );
}

export default UploadFile;
