from datetime import datetime
from typing import List, Dict
import unittest

class PacienteNoExisteError(Exception):
    pass

class PacienteYaExisteError(Exception):
    pass

class MedicoNoExisteError(Exception):
    pass

class MedicoYaExisteError(Exception):
    pass

class TurnoDuplicadoError(Exception):
    pass

class RecetaInvalidaError(Exception):
    pass

class Paciente:
    def __init__(self, dni_paciente: str, nombre_paciente: str, fecha_nacimiento: str):
        
        if not dni_paciente.strip():
            raise ValueError("El DNI del paciente no puede estar vacío.")
        if not nombre_paciente.strip():
            raise ValueError("El nombre del paciente no puede estar vacío.")

        try:
            self.__fecha_nacimiento__ = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"Formato de fecha inválido: {fecha_nacimiento}. Debe ser dd/mm/aaaa.")

        self.__dni__ = dni_paciente
        self.__nombre__ = nombre_paciente
        self.__fecha_nacimiento__ = fecha_nacimiento

    def obtener_dni(self):
        return f'El DNI del paciente {self.__nombre__} es: {self.__dni__}'
    
    #Funciones agregadas

    def set_dni(self, dni_paciente):
        self.__dni__ = str(dni_paciente)
    
    def set_nombre(self, nombre_paciente):
        self.__nombre__ = nombre_paciente
    
    def set_nacimiento(self, fecha_nacimiento):
        self.__fecha_nacimiento__ = fecha_nacimiento
        
    def obtener_nombre(self):
        return f'El nombre del paciente es: {self.__nombre__}'
    
    def obtener_nacimiento(self):
        return f'La fecha de nacimiento del paciente {self.__nombre__} es: {self.__fecha_nacimiento__}'
    
    #Función STR
    def __str__(self) -> str:
        return f"Paciente: {self.__nombre__} (DNI: {self.__dni__}) - Nacimiento: {self.__fecha_nacimiento__}"

class Especialidad:
    DIAS_VALIDOS = {"lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"}

    def __init__(self, tipo: str, dias: list[str] = None):

        if not tipo.strip():
            raise ValueError("El tipo de especialidad no puede estar vacío.")
        if dias is None:
            dias = []

        dias_normalizados = [dia.lower() for dia in dias]

        if len(dias_normalizados) != len(set(dias_normalizados)):
            raise ValueError(f"La especialidad {tipo} contiene días duplicados.")
        
        for dia in dias_normalizados:
            if dia not in self.DIAS_VALIDOS:
                raise ValueError(f"El día '{dia}' no es válido. Debe ser uno de {', '.join(self.DIAS_VALIDOS)}.")
        
        self.__tipo__ = tipo
        self.__dias__ = dias
        self.__especialidades__ = []
        
    def obtener_especialidad(self) -> str:
        return f"{self.__tipo__}"
    
    #Funciones agregadas
    
    def set_especialidad(self, especialidad):
        if not especialidad.strip():
            raise ValueError("El tipo de especialidad no puede estar vacío.")
        self.__tipo__ = especialidad
    
    def set_dias(self, dia):
        if self.__dias__ is None:
            self.__dias__ = []
        self.__dias__.append(dia)
    
    #Validaciones
    def verificar_dia(self, dia: str) -> bool:
        if not self.__dias__:
            return False
            
        for d in self.__dias__:
            if d.lower() == dia.lower():
                return True
        return False

    #Función STR
    def __str__(self) -> str:
        if self.__dias__:
            dias_str = ", ".join(self.__dias__)
            return f"Especialidad: {self.__tipo__} - Días disponibles: {dias_str}"
        else:
            return f"Especialidad: {self.__tipo__} - Sin días asignados"

class Medico:
    def __init__(self, matricula_medico: str, nombre_medico: str, especialidad: list[Especialidad]):
        
        if not matricula_medico.strip():
            raise ValueError("La matrícula del médico no puede estar vacía.")
        if not nombre_medico.strip():
            raise ValueError("El nombre del médico no puede estar vacío.")

        self.__matricula__ = matricula_medico
        self.__nombre__ = nombre_medico
        self.__especialidades__ = especialidad if isinstance(especialidad, list) else [especialidad]


    def obtener_matricula(self):
        return f'La matrícula del Médico {self.__nombre__} es: {self.__matricula__}'
    
    def obtener_especialidad_para_dia(self, dia, especialidad: Especialidad)-> str | None:
        for especialidad in self.__especialidades__:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad()
        return None

    #Funciones adicionales personales:

    def set_matricula(self, matricula):
        self.__matricula__ = str(matricula)
    
    def set_nombreM(self, nombre_medico):
        self.__nombre__ = nombre_medico
    
    def set_especialidad(self, especialidad):
        self.__especialidades__ = especialidad

    def agregar_especialidad(self, nueva_especialidad: Especialidad):
        if nueva_especialidad in self.__especialidades__:
            raise ValueError(f"La especialidad {nueva_especialidad.__tipo__} ya está asignada al médico.")
        
        self.__especialidades__.append(nueva_especialidad)
    
    def get_nombre(self):
        return f'El nombre del Médico es: {self.__nombre__}'
    
    def get_especialidad(self, especialidad: Especialidad):
        return f'La especialidad del Médico {self.__nombre__} es: {especialidad.obtener_especialidad()}'
    
    def get_especialidad_completa(self):
        return f'El Médico {self.__nombre__} - {self.__especialidades__}'

    #Función STR
    def __str__(self) -> str:
        return f"Dr. {self.__nombre__} - {self.__especialidades__} (Matrícula: {self.__matricula__})"

class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, especialidad: Especialidad):
        if paciente is None or medico is None:
            raise ValueError("Paciente y médico son requeridos para crear un turno.")
        
        dia_semana = Clinica.obtener_dia_semana_en_espanol(fecha_hora)

        if dia_semana.lower() not in [d.lower() for d in especialidad.__dias__]:
            raise ValueError(f"El médico no trabaja el día {dia_semana}. Días disponibles: {', '.join(especialidad.__dias__)}")

        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__fecha_hora__ = fecha_hora
        self.__especialidad__ = especialidad
    
    def obtener_medico(self) -> Medico:
        return self.__medico__
    
    def obtener_fecha_hora(self) -> datetime:
        return self.__fecha_hora__
    
    #Función STR
    def __str__(self) -> str:
        fecha_formateada = self.__fecha_hora__.strftime("%d/%m/%Y %H:%M")
        return (f"Turno - Paciente: {self.__paciente__}, "
                f"Médico: {self.__medico__}, "
                f"Fecha y Hora: {fecha_formateada}, "
                f"Especialidad: {self.__especialidad__}")

class Receta:
    
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: List[str], fecha: datetime = None):

        if paciente is None or medico is None:
            raise ValueError("Paciente y médico son requeridos para emitir una receta.")
        if not medicamentos or len(medicamentos) == 0:
            raise ValueError("Debe haber al menos un medicamento en la receta.")
        
        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__medicamentos__ = medicamentos
        self.__fecha__ = fecha if fecha else datetime.now()
    
    #Funciones agregadas
    def agregar_medicamentos (self, medicamento):
        self.__medicamentos__.append(medicamento)

    #Función STR
    def __str__(self) -> str:
        fecha_str = self.__fecha__.strftime("%d/%m/%Y")
        medicamentos_str = ", ".join(self.__medicamentos__)
        return f"Receta [{fecha_str}]: {medicamentos_str} - Prescrita por {self.__medico__.__nombre__} para {self.__paciente__.__nombre__}"

class HistoriaClinica():
    def __init__(self, paciente: Paciente ):
        self.__paciente__ = paciente
        self.__turnos__: List[Turno] = []
        self.__recetas__: List[Receta] = []

    #Registro de datos
    def agregar_turno_a_lista(self, turno : Turno):
        self.__turnos__.append(turno)
    
    def agregar_receta_hist(self, receta):
        if receta is None:
            raise ValueError("La receta no puede ser nula.")
        self.__recetas__.append(receta)

    
    #Acceso a la información
    def obtener_turnos(self):
        return f'Los Turnos son: {[str(turno) for turno in self.__turnos__]}'
    
    def obtener_receta(self):
        return f'Las Recetas son: {[str(receta) for receta in self.__recetas__]}'
    
    #Función STR
    def __str__(self) -> str:
        turnos_info = f"{len(self.__turnos__)} turno(s)" if self.__turnos__ else "Sin turnos"
        recetas_info = f"{len(self.__recetas__)} receta(s)" if self.__recetas__ else "Sin recetas"
    
        return f"Historia Clínica de {self.__paciente__.__nombre__} - {turnos_info}, {recetas_info}"

class Clinica():
    def __init__(
            self,
    ):
        self.__pacientes__: Dict[str, Paciente] = {}  
        self.__medicos__: Dict[str, Medico] = {}      
        self.__turnos__: List[Turno] = []
        self.__historias_clinicas__: Dict[str, HistoriaClinica] = {}
        self.__especialidades__: List[Especialidad] = []

    #Registro y acceso
    def agregar_paciente(self, pacienteC: Paciente):
        dni = pacienteC.__dni__
        if dni in self.__pacientes__:
            raise PacienteYaExisteError(f'Ya existe un paciente con el DNI: {dni}')
        self.__pacientes__[dni] = pacienteC
        self.__historias_clinicas__[dni] = HistoriaClinica(pacienteC)
    
    def agregar_medico(self, medico : Medico):
        matricula = medico.__matricula__
        if matricula in self.__medicos__:
            raise MedicoYaExisteError(f"Ya existe un médico con matrícula {matricula}")
        self.__medicos__[matricula] = medico

    def agregar_especialidad(self, especialidad: Especialidad):
        especialidad_normalizada = especialidad.__tipo__.strip().lower()

        if any(esp.__tipo__.strip().lower() == especialidad_normalizada for esp in self.__especialidades__):
            raise ValueError(f"La especialidad '{especialidad.__tipo__}' ya está registrada en la clínica.")

        self.__especialidades__.append(especialidad)
 
    def obtener_medico_por_matricula(self, matricula: str) -> "Medico":
        """Devuelve un médico por su matrícula, si existe"""
        if matricula in self.__medicos__:
            return self.__medicos__[matricula]
        else:
            raise MedicoNoExisteError(f"No existe médico con matrícula {matricula}")
    
    def obtener_pacientes(self) -> List[Paciente]:
        return list(self.__pacientes__.values())

    def obtener_medicos(self) -> List[Medico]:
        return list(self.__medicos__.values())

    #Turnos
    def agendar_turno(self, fecha_hora: datetime, dni: str, matricula: str, especialidad: Especialidad):
    
        if dni not in self.__pacientes__:
            raise PacienteNoExisteError(f"No existe paciente con DNI {dni}")
    
        if matricula not in self.__medicos__:
            raise MedicoNoExisteError(f"No existe médico con matrícula {matricula}")
    
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
    
        # Verificar turno duplicado ANTES de validar la fecha
        for turno in self.__turnos__:
            # Verificar si es exactamente el mismo turno
            if (turno.__fecha_hora__ == fecha_hora and 
                turno.__paciente__ == paciente and 
                turno.__medico__ == medico):
                raise TurnoDuplicadoError(f"Ya existe un turno para {medico.get_nombre()} el {fecha_hora.strftime('%d/%m/%Y %H:%M')}")
    
        # Validación de fecha
        ahora = datetime.now()
        if fecha_hora.date() < ahora.date():
            raise ValueError("No se pueden agendar turnos en el pasado")

        # Crear y agregar el turno
        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos__.append(turno)
    
        # Agregar a historia clínica si existe
        if dni in self.__historias_clinicas__:
            self.__historias_clinicas__[dni].agregar_turno_a_lista(turno)

        return f'Turno para {paciente} con {medico} agregado.'
    
    def obtener_turnos(self):
        return f'Turnos programados: {self.__turnos__}'

    #Recetas e Historias Clínicas
    def emitir_receta(self, dni: str, matricula: str, medicamentos: List[str]):
        # Validar que el paciente existe
        if dni not in self.__pacientes__:
            raise PacienteNoExisteError(f"No existe paciente con DNI {dni}")
    
        # Validar que el médico existe
        if matricula not in self.__medicos__:
            raise MedicoNoExisteError(f"No existe médico con matrícula {matricula}")
    
        # Validaciones para receta inválida
        if not medicamentos:
            raise RecetaInvalidaError("La receta debe contener al menos un medicamento")
    
        if len(medicamentos) > 10:  # Límite máximo de medicamentos
            raise RecetaInvalidaError("La receta no puede contener más de 10 medicamentos")
    
        # Validar que los medicamentos no estén vacíos o sean solo espacios
        for medicamento in medicamentos:
            if not medicamento or not medicamento.strip():
                raise RecetaInvalidaError("Los nombres de medicamentos no pueden estar vacíos")
        
            if len(medicamento.strip()) < 2:
                raise RecetaInvalidaError("Los nombres de medicamentos deben tener al menos 2 caracteres")
    
        # Validar que no haya medicamentos duplicados
        medicamentos_normalizados = [med.strip().lower() for med in medicamentos]
        if len(medicamentos_normalizados) != len(set(medicamentos_normalizados)):
            raise RecetaInvalidaError("La receta no puede contener medicamentos duplicados")
    
        # Si todas las validaciones pasan, crear la receta
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        receta = Receta(paciente, medico, medicamentos)
    
        self.__historias_clinicas__[dni].agregar_receta_hist(receta)
        return f'Receta emitida para {self.__pacientes__[dni]} por {self.__medicos__[matricula]}.'
    
    def obtener_historia_clinica(self, dni: str) -> HistoriaClinica:
        if dni not in self.__pacientes__:
            raise PacienteNoExisteError(f"No existe paciente con DNI {dni}")
        else:
            return self.__historias_clinicas__[dni]
    
    #Validaciones y Utilidades
    def validar_existencia_paciente(self, dni: str) -> bool:
        return dni in self.__pacientes__
    
    def validar_existencia_medico(self, matricula: str) -> bool:
        return matricula in self.__medicos__
    
    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime) -> bool:
        for turno in self.__turnos__:
            if (turno.__medico__.obtener_matricula() == matricula and 
                turno.__fecha_hora__ == fecha_hora):
                return False
        return True
    
    @staticmethod
    def obtener_dia_semana_en_espanol(fecha_hora: datetime) -> str:
        dias_espanol = {
        'monday': 'Lunes',
        'tuesday': 'Martes', 
        'wednesday': 'Miércoles',
        'thursday': 'Jueves',
        'friday': 'Viernes',
        'saturday': 'Sábado',
        'sunday': 'Domingo'
    }
        dia_ingles = fecha_hora.strftime('%A').lower()
        return dias_espanol.get(dia_ingles, dia_ingles)

    def obtener_especialidad_disponible(self, medico: Medico, dia_semana: str, especialidad: Especialidad) -> str:
        especialidad_medico = medico.__especialidades__
        
        # Verificar si la especialidad del médico existe en el sistema
        if especialidad_medico not in self.__especialidades__:
            return f"La especialidad '{especialidad_medico}' del Dr. {medico.__nombre__} no está registrada en el sistema"
        
        especialidad_obj = self.__especialidades__[especialidad_medico]
        
        # Verificar si la especialidad está disponible en el día solicitado
        if especialidad.verificar_dia(dia_semana):
            return f"La especialidad '{especialidad_medico}' del Dr. {medico.__nombre__} está disponible el día {dia_semana.capitalize()}"
        else:
            dias_disponibles = ", ".join(especialidad.__dias__) if especialidad.__dias__ else "ningún día"
            return f"La especialidad '{especialidad_medico}' del Dr. {medico.__nombre__} NO está disponible el día {dia_semana.capitalize()}. Días disponibles: {dias_disponibles}"
    
    def validar_especialidad_en_dia(self, medico: Medico, especialidad_solicitada: str, dia_semana: str) -> bool:
        # Verificar si el médico tiene la especialidad solicitada
        if not hasattr(medico, '__especialidades__'):
            return False
            
        # Si el médico tiene múltiples especialidades (lista)
        if isinstance(medico.__especialidades__, list):
            especialidades_medico = medico.__especialidades__
        else:
            # Si el médico tiene una sola especialidad
            especialidades_medico = [medico.__especialidades__]
        
        # Buscar la especialidad solicitada entre las especialidades del médico
        especialidad_encontrada = None
        for esp in especialidades_medico:
            if isinstance(esp, str):
                if esp == especialidad_solicitada:
                    # Buscar el objeto especialidad en el sistema
                    for esp_obj in self.__especialidades__:
                        if esp_obj.__tipo__ == especialidad_solicitada:
                            especialidad_encontrada = esp_obj
                            break
            elif hasattr(esp, '__tipo__'):
                if esp.__tipo__ == especialidad_solicitada:
                    especialidad_encontrada = esp
                    break
        
        if especialidad_encontrada is None:
            return False
        
        # Verificar si la especialidad está disponible en el día solicitado
        return especialidad_encontrada.verificar_dia(dia_semana)

    #Función STR
    def __str__(self):
        return f'Pacientes: {self.__pacientes__}\n Medicos: {self.__medicos__}\n Turnos: {self.__turnos__}'
    
class CLI:
    
    def __init__(self):
        self.clinica = Clinica()
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "="*50)
        print("SISTEMA DE GESTIÓN DE CLÍNICA MÉDICA")
        print("="*50)
        print("1. Agregar paciente")
        print("2. Agregar médico")
        print("3. Agendar turno")
        print("4. Emitir receta")
        print("5. Ver historia clínica")
        print("6. Ver todos los turnos")
        print("7. Ver todos los pacientes")
        print("8. Ver todos los médicos")
        print("9. Ver los médicos por matrículas")
        print("10. Agregar especialidad")
        print("11. Obtener especialidad disponible")
        print("12. Salir")
        print("="*50)
    
    def agregar_paciente(self):
        print("\n--- AGREGAR PACIENTE ---")
        dni = str(input("DNI: "))
        nombre = str(input("Nombre completo: "))            
        fecha_nacimiento = str(input("Fecha de nacimiento (dd/mm/aaaa): "))
        paciente = Paciente(dni, nombre, fecha_nacimiento)
        try:
            self.clinica.agregar_paciente(paciente)
            print(f"Paciente {nombre} agregado exitosamente")
        except PacienteYaExisteError as e:
            print(e)    
    
    def agregar_medico(self):
        print("\n--- AGREGAR MÉDICO ---")
        matricula = str(input("Matrícula: "))
        nombre = str(input("Nombre completo: "))            
        especialidad = str(input("Especialidad: "))  
        medico = Medico(matricula, nombre, especialidad)
        try:
            self.clinica.agregar_medico(medico)
            print(f"Dr. {nombre} agregado exitosamente")
        except MedicoYaExisteError as e:
            print(str(e))   
    
    def agendar_turno(self):
        try:
            print("\n--- AGENDAR TURNO ---")
            dni = str(input("DNI del paciente: "))
            matricula = str(input("Matrícula del médico: "))
            fecha_str = str(input("Fecha y hora (dd/mm/aaaa HH:MM): "))
            
            fecha_hora = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
            self.clinica.agendar_turno(dni, matricula, fecha_hora)
            print("Turno agendado exitosamente")
            
        except (PacienteNoExisteError, MedicoNoExisteError, TurnoDuplicadoError) as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error de formato: {e}")

    
    def emitir_receta(self):
        try:
            print("\n--- EMITIR RECETA ---")
            dni = str(input("DNI del paciente: "))
            matricula = str(input("Matrícula del médico: "))
            medicamentos_str = str(input("Medicamentos (separados por coma): "))
        
            medicamentos = [med.strip() for med in medicamentos_str.split(",")]
            resultado = self.clinica.emitir_receta(dni, matricula, medicamentos)
            print("Receta emitida exitosamente")
            print(resultado)
        
        except PacienteNoExisteError as e:
            print(f"Error - Paciente no encontrado: {e}")
        
        except MedicoNoExisteError as e:
            print(f"Error - Médico no encontrado: {e}")
        
        except RecetaInvalidaError as e:
            print(f"Error - Receta inválida: {e}")
    
    def ver_historia_clinica(self):
        try:
            print("\n--- VER HISTORIA CLÍNICA ---")
            dni = str(input("DNI del paciente: "))
            
            historia = self.clinica.obtener_historia_clinica(dni)
            print(historia)
            
        except PacienteNoExisteError as e:
            print(f"Error: {e}")

    
    def ver_todos_los_turnos(self):
        print("\n--- TODOS LOS TURNOS ---")
        turnos = self.clinica.obtener_turnos()
        
        if turnos:
            for i, turno in enumerate(turnos, 1):
                print(f"{i}. {turno}")
        else:
            print("No hay turnos registrados")
    
    def ver_todos_los_pacientes(self):
        print("\n--- TODOS LOS PACIENTES ---")
        pacientes = self.clinica.obtener_pacientes()  # Llamada al método correcto
        
        if pacientes:
            for i, paciente in enumerate(pacientes, 1):
                print(f"{i}. {paciente}")
        else:
            print("No hay pacientes registrados.")

    def ver_todos_los_medicos(self):
        print("\n--- TODOS LOS MÉDICOS ---")
        medicos = self.clinica.obtener_medicos()  # Llamada al método correcto
        
        if medicos:
            for i, medico in enumerate(medicos, 1):
                print(f"{i}. {medico}")
        else:
            print("No hay médicos registrados.")

    def buscar_medico_por_matricula(self, matricula: str):
        try:
            medico = self.clinica.obtener_medico_por_matricula(matricula)  # Llamada directa
            print(f"\nMédico encontrado: {medico}")
        except MedicoNoExisteError as e:
            print(f"Error: {e}")
    
    def agregar_especialidad(self):
        print("\n--- AGREGAR ESPECIALIDAD ---")
        tipo = str(input("Tipo de especialidad: "))
        print("Ingrese los días disponibles (uno por línea, presione Enter sin texto para terminar):")
        
        dias = []
        while True:
            dia = str(input("Día: ")).strip()
            if dia == "":
                break
            dias.append(dia)
        
        especialidad = Especialidad(tipo, dias)

        try:
            self.clinica.agregar_especialidad(especialidad)
            print(f"Especialidad {tipo} agregada exitosamente")
            if dias:
                print(f"Días disponibles: {', '.join(dias)}")
        except Exception as e:
            print(f"Error al agregar especialidad: {e}")
    
    def obtener_especialidad_disponible(self):
        print("\n--- OBTENER ESPECIALIDAD DISPONIBLE ---")
        matricula = str(input("Matrícula del médico: "))
        dia_semana = str(input("Día de la semana: "))
            
        if matricula not in self.clinica.__medicos__:
            print(f"Error: No existe médico con matrícula {matricula}")
            return
        
        medico = self.clinica.__medicos__[matricula]
        resultado = self.clinica.obtener_especialidad_disponible(medico, dia_semana)
        print(resultado)

    def ejecutar(self):
        """Ejecuta la interfaz CLI"""
        while True:
            self.mostrar_menu()
            opcion = str(input("Seleccione una opción (1-11): "))
            print("opcion: ", opcion)
            if opcion == "1":
                self.agregar_paciente()
            elif opcion == "2":
                self.agregar_medico()
            elif opcion == "3":
                self.agendar_turno()
            elif opcion == "4":
                self.emitir_receta()
            elif opcion == "5":
                self.ver_historia_clinica()
            elif opcion == "6":
                self.ver_todos_los_turnos()
            elif opcion == "7":
                self.ver_todos_los_pacientes()
            elif opcion == "8":
                self.ver_todos_los_medicos()
            elif opcion == "9":
                self.buscar_medico_por_matricula()
            elif opcion == "10":
                self.agregar_especialidad()
            elif opcion == "11":
                self.obtener_especialidad_disponible()
            elif opcion == "12":
                print("¡Gracias por usar el sistema de la clínica!")
                break
            else:
                print("Opción inválida. Por favor seleccione del 1 al 12.")

def main():
    """Función principal"""
    print("🏥 Bienvenido al Sistema de Gestión de Clínica Médica")
    print("\n¿Qué desea hacer?")
    print("1. Ejecutar la aplicación")
    print("2. Ejecutar tests unitarios")
    print("3. Salir")
    
    opcion = input("Seleccione una opción (1-3): ").strip()
    
    if opcion == "1":
        cli = CLI()
        cli.ejecutar()
    elif opcion == "2":
        print("\nEjecutando tests unitarios...")
        unittest.main(argv=[''], exit=False, verbosity=2)
    elif opcion == "3":
        print("¡Hasta luego!")
    else:
        print("Opción inválida")

if __name__ == "__main__":
    main()