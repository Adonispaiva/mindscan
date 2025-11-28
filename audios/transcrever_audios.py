import os
import whisper

# Carregar modelo
model = whisper.load_model("medium")  # pode trocar para "small" se quiser mais rápido

# Pasta atual
folder = os.getcwd()

print(f"Transcrevendo áudios da pasta: {folder}\n")

for file in os.listdir(folder):
    if file.lower().endswith((".mp3", ".wav", ".ogg", ".m4a")):
        print(f"--> Transcrevendo: {file}")
        audio_path = os.path.join(folder, file)

        result = model.transcribe(audio_path, fp16=False)

        # Salvar transcrição
        output_file = file.rsplit(".", 1)[0] + "_transcricao.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print(f"    ✔ Transcrição salva em: {output_file}")

print("\nFinalizado.")
