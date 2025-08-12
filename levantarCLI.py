import subprocess
import os
import sys

def abrir_terminales_ejecutar_main(num_terminales):
    """
    Abre múltiples terminales en macOS/Linux ejecutando main.py en paralelo
    """
    # Obtener la ruta actual del script
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    programa = 'main.py'
    
    # Verificar que main.py existe en la ruta actual
    main_py_path = os.path.join(ruta_actual, programa)
    if not os.path.isfile(main_py_path):
        print(f"❌ No se encontró {programa} en la ruta: {ruta_actual}")
        return
    
    # Detectar el sistema operativo
    sistema = sys.platform
    
    print(f"🚀 Iniciando {num_terminales} procesos paralelos de {programa}")
    print(f"📁 Directorio: {ruta_actual}")
    print(f"💻 Sistema: {sistema}")
    print("-" * 60)
    
    # Comandos para diferentes sistemas operativos
    procesos_iniciados = 0
    
    for i in range(num_terminales):
        try:
            if sistema == "darwin":  # macOS
                # Usar Terminal.app de macOS
                applescript = f'''
                tell application "Terminal"
                    do script "cd '{ruta_actual}' && python {programa}"
                    activate
                end tell
                '''
                subprocess.Popen(['osascript', '-e', applescript])
                
            elif sistema.startswith("linux"):  # Linux
                # Intentar diferentes terminales comunes en Linux
                terminales_linux = [
                    'gnome-terminal',
                    'konsole', 
                    'xfce4-terminal',
                    'xterm'
                ]
                
                terminal_usado = None
                for terminal in terminales_linux:
                    try:
                        if terminal == 'gnome-terminal':
                            subprocess.Popen([
                                terminal, '--', 'bash', '-c', 
                                f'cd "{ruta_actual}" && python {programa}; exec bash'
                            ])
                        elif terminal == 'konsole':
                            subprocess.Popen([
                                terminal, '--workdir', ruta_actual, '-e', 
                                'bash', '-c', f'python {programa}; exec bash'
                            ])
                        elif terminal == 'xfce4-terminal':
                            subprocess.Popen([
                                terminal, '--working-directory', ruta_actual, 
                                '--command', f'bash -c "python {programa}; exec bash"'
                            ])
                        else:  # xterm
                            subprocess.Popen([
                                terminal, '-e', 'bash', '-c', 
                                f'cd "{ruta_actual}" && python {programa}; exec bash'
                            ])
                        terminal_usado = terminal
                        break
                    except FileNotFoundError:
                        continue
                        
                if not terminal_usado:
                    print(f"❌ No se encontró un terminal compatible en Linux")
                    return
                    
            else:
                print(f"❌ Sistema operativo no soportado: {sistema}")
                print("💡 Este script funciona en macOS y Linux")
                return
                
            procesos_iniciados += 1
            print(f"✅ Terminal {i+1} iniciado correctamente")
            
        except Exception as e:
            print(f"❌ Error al iniciar terminal {i+1}: {e}")
    
    print("-" * 60)
    print(f"🎉 Se iniciaron {procesos_iniciados}/{num_terminales} terminales exitosamente")
    
    if procesos_iniciados > 0:
        print("\n📋 Instrucciones:")
        print("• Cada terminal ejecutará main.py independientemente")
        print("• Los experimentos se procesan desde la base de datos en orden")
        print("• Puedes cerrar este script, los terminales seguirán ejecutándose")
        print("• Para detener: cierra cada terminal manualmente")
        
        print("\n📊 Monitoreo:")
        print("• Archivos CSV se crean en Resultados/")
        print("• Progreso visible en cada terminal")
        print("• Estado en BD: sqlite3 BD/resultados.db \"SELECT estado, COUNT(*) FROM experimentos GROUP BY estado;\"")

def main():
    print("🧪 SCP-USCP Parallel Experiment Launcher (macOS/Linux)")
    print("=" * 60)
    
    try:
        # Verificar si hay experimentos pendientes
        try:
            import sqlite3
            conn = sqlite3.connect('BD/resultados.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM experimentos WHERE estado = 'pendiente'")
            pendientes = cursor.fetchone()[0]
            conn.close()
            
            if pendientes == 0:
                print("⚠️  No hay experimentos pendientes en la base de datos")
                print("💡 Ejecuta primero: python poblarDB.py")
                return
            else:
                print(f"📋 Experimentos pendientes: {pendientes}")
                
        except Exception as e:
            print(f"⚠️  No se pudo verificar la base de datos: {e}")
            print("💡 Asegúrate de haber ejecutado: python crearBD.py && python poblarDB.py")
    
        # Configuración de terminales
        num_terminales_default = 3
        
        print(f"\n🔧 Configuración:")
        respuesta = input(f"¿Cuántos terminales paralelos abrir? (default: {num_terminales_default}): ").strip()
        
        if respuesta:
            try:
                num_terminales = int(respuesta)
                if num_terminales < 1 or num_terminales > 10:
                    print("❌ Número debe estar entre 1 y 10")
                    return
            except ValueError:
                print("❌ Por favor ingresa un número válido")
                return
        else:
            num_terminales = num_terminales_default
        
        print(f"\n🚀 Abriendo {num_terminales} terminales...")
        abrir_terminales_ejecutar_main(num_terminales)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()