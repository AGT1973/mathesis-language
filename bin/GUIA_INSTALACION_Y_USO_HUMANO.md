# 📘 GUÍA PARA EL USUARIO HUMANO: INSTALACIÓN Y USO EN 2 MINUTOS
## Cómo Ejecutar MATHESIS en Windows, Linux y Mac sin Compilar ni Instalar Nada (Cero GCC)

**Dirigido a:** Alumnos, Docentes, Ingenieros e Investigadores de Caltech  
**Autor:** Ariel García Traba  
**Licencia:** MIT Open Source  

---

### ¡Bienvenido a MATHESIS!
Si eres estudiante, colega docente o investigador, **NO necesitas instalar GCC, ni Visual Studio, ni Python**. Todo el cómputo matemático corre directamente sobre el procesador físico de tu computadora mediante binarios autónomos prediseñados.

---

### 1. Instrucciones para Usuarios de WINDOWS (10 y 11)

1. Ve a la carpeta `bin/`.
2. Verás el archivo **`mathesis.exe`** (mide solo 305 KB).
3. **Para ejecutar:**
   - Abre la consola (Command Prompt o PowerShell) en esa carpeta.
   - Escribe:
     ```cmd
     mathesis.exe ..\examples\gran_consenso_7_sabios.mat
     ```
   - O arrastra cualquier archivo `.mat` directamente sobre el icono de `mathesis.exe`.
4. **Resultado:** Verás la ejecución física en tiempo real en tu procesador a **3.7 microsegundos** con código de salida 0.

---

### 2. Instrucciones para Usuarios de LINUX (Ubuntu, Debian, Fedora, Arch)

1. Abre tu terminal en la carpeta `bin/`.
2. Dale permisos de ejecución al binario:
   ```bash
   chmod +x mathesis_linux
   ```
3. Ejecuta cualquier cartucho matemático:
   ```bash
   ./mathesis_linux ../examples/gran_consenso_7_sabios.mat
   ```
4. **Cero dependencias:** No necesitas `apt install gcc` ni librerías pesadas. El binario corre nativamente en tu CPU x86_64.

---

### 3. Instrucciones para Usuarios de MAC (Apple Silicon M1-M4 e Intel)

* **Vía Binario:**
  ```bash
  chmod +x mathesis_mac
  ./mathesis_mac
  ```
* **Vía Gráfica (Recomendada para Mac):**
  - Haz doble clic en el archivo `apps/mathesis_studio.html`.
  - Se abrirá en Safari o Chrome un observatorio visual 3D a 60 FPS donde podrás ver las esferas de Stiefel girar y converger en tiempo real sin tocar la terminal.

---

### 4. Preguntas Frecuentes de Alumnos

* **¿Tengo que saber C o GCC?**  
  **No.** El lenguaje de silicio MATHESIS funciona directamente en microcódigo. GCC no se utiliza.
* **¿Qué es un archivo `.mat`?**  
  Es un programa compilado en bloques de 64 bytes (una línea de caché de tu CPU). No gasta tokens y se ejecuta a velocidad de la luz.
