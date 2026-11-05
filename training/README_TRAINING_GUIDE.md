# 🎓 GUÍA DE ENTRENAMIENTO QLoRA EN KAGGLE (100% GRATUITO)
## Para crear el modelo local MATHESIS-1.5B (DeepSeek-R1-Distill / Qwen-2.5-Coder)

---

### Paso 1: Abrir Kaggle (o Google Colab)
1. Entrá a [kaggle.com](https://www.kaggle.com) $\to$ **New Notebook**.
2. En la barra lateral derecha (*Notebook options*):
   - **Accelerator:** Elegí `GPU T4 x2` (o `GPU P100`). Te da 30 horas semanales gratis.
   - **Internet:** `On` (Activado).

---

### Paso 2: Subir el Dataset Verificado
1. En la pestaña **Input / Data** de Kaggle, hacé click en **Upload** $\to$ seleccioná el archivo generado en tu máquina:
   [`E:\MATHESIS\training\mathesis_train_dataset.jsonl`](file:///E:/MATHESIS/training/mathesis_train_dataset.jsonl) (pesa solo 656 KB, contiene 600 muestras exactas de 64 bytes).

---

### Paso 3: Pegar y Ejecutar el Script
1. Pegá el contenido de [`E:\MATHESIS\training\kaggle_finetune_mathesis.py`](file:///E:/MATHESIS/training/kaggle_finetune_mathesis.py).
2. Hacé click en **Run All** (o apretá `Shift + Enter`).
3. **Tiempo de entrenamiento:** ~35 minutos en la T4 de Kaggle. Consumo de VRAM: ~4.5 GB de los 16 GB disponibles.

---

### Paso 4: Descargar el Adaptador LoRA
1. Al terminar, el script genera automáticamente el archivo `mathesis_lora_adapter.zip` (pesa ~15 MB).
2. Lo descargás a tu PC y lo descomprimís en:
   `E:\MATHESIS\training\mathesis_lora_adapter\`
3. Ejecutás en tu máquina:
   ```bash
   python E:\MATHESIS\training\local_cpu_inference.py
   ```
   ¡Y listo! Tu procesador AMD A4-6300 tendrá su propio modelo de razonamiento continuo MATHESIS corriendo 100% offline en CPU local.
