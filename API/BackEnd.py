from flask import Flask, request, jsonify
import pydicom
from pydicom import Dataset
import os

app = Flask(__name__)

# Pasta onde os arquivos DICOM enviados serão armazenados temporariamente
UPLOAD_FOLDER = 'API/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def anonymize_dicom(file_path):
    try:
        # Carregue o arquivo DICOM
        ds = pydicom.dcmread(file_path)

        # Anonimize os dados (substitua os campos relevantes)
        ds.PatientID = "DADO ANONIMIZADO"
        ds.PatientName = "DADO ANONIMIZADO"
        ds.PatientBirthDate = "DADO ANONIMIZADO"
        ds.PatientSex = "DADO ANONIMIZADO"
        ds.PatientAge = "DADO ANONIMIZADO"
        # Adicione mais campos a serem anonimizados conforme necessário

        # Salve o DICOM anonimizado
        ds.save_as(file_path)

        return ds
    except Exception as e:
        return str(e)

@app.route('/anonimizar_dicom', methods=['POST'])
def anonimizar_dicom():
    try:
        # Verifique se o arquivo DICOM foi enviado como parte da solicitação POST
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo DICOM enviado'}), 400

        file = request.files['file']

        # Verifique se é um arquivo DICOM válido
        if not file.filename.endswith('.dcm'):
            return jsonify({'error': 'O arquivo não é um arquivo DICOM válido'}), 400

        # Salve o arquivo DICOM enviado temporariamente
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(temp_file_path)

        # Anonimize o DICOM
        dicom_response = anonymize_dicom(temp_file_path)

        # Prepare a resposta com os metadados anonimizados
        metadados_anonimizados = {
            'ID do Paciente': str(dicom_response.PatientID),
            'Nome do Paciente': str(dicom_response.PatientName),
            'Data de Nascimento': str(dicom_response.PatientBirthDate),
            'Genero do Paciente': str(dicom_response.PatientSex),
            'Idade do Paciente': str(dicom_response.PatientAge),
        }

        return jsonify(metadados_anonimizados), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
