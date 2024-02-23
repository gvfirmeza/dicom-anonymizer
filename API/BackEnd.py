from flask import Flask, request, jsonify, send_from_directory, send_file  
from flask_cors import CORS
import pydicom
import os

app = Flask(__name__)
CORS(app, resources={r"/anonimizar_dicom": {"origins": "http://localhost:3000"}})  # Configure o CORS para a sua aplicação

# Pasta onde os arquivos DICOM enviados serão armazenados temporariamente
UPLOAD_FOLDER = '.\uploads'
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

        return ds, file_path
    except Exception as e:
        print(f'Erro durante a anonimização: {str(e)}')
        return None, None

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

        # Anonimize o DICOM e obtenha o objeto DICOM e o caminho do arquivo
        dicom_response, dicom_anonimizado_path = anonymize_dicom(temp_file_path)

        if dicom_response is not None:
            # Prepare a resposta com os metadados anonimizados e o caminho para download
            response_data = {
                'ID do Paciente': str(dicom_response.PatientID),
                'Nome do Paciente': str(dicom_response.PatientName),
                'Data de Nascimento': str(dicom_response.PatientBirthDate),
                'Genero do Paciente': str(dicom_response.PatientSex),
                'Idade do Paciente': str(dicom_response.PatientAge),
                'downloadUrl': f'/baixar/{os.path.basename(dicom_anonimizado_path)}',
            }

            return jsonify(response_data), 200
        else:
            return jsonify({'error': 'Erro durante a anonimização'}), 500
    except Exception as e:
        print(f'Erro durante o processamento: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/baixar/<filename>', methods=['GET'])
def download_anonimized_dicom(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
