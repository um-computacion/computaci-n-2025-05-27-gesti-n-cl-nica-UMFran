import unittest
from datetime import datetime
from src.clinica import (Clinica, Paciente, Medico, Turno, Receta, HistoriaClinica, Especialidad, CLI, PacienteNoExisteError, PacienteYaExisteError, MedicoNoExisteError, MedicoYaExisteError, TurnoDuplicadoError, RecetaInvalidaError)
from unittest.mock import patch

class TestPaciente(unittest.TestCase):
    def setUp(self):
        self.paciente = Paciente("12345678", "Juan Pérez", "01/01/1980")

    def test_creacion_paciente(self):
        self.assertEqual(self.paciente.__dni__, "12345678")
        self.assertEqual(self.paciente.__nombre__, "Juan Pérez")
        self.assertEqual(self.paciente.__fecha_nacimiento__, "01/01/1980")

    def test_obtener_dni(self):
        self.assertEqual(self.paciente.obtener_dni(), "El DNI del paciente Juan Pérez es: 12345678")

    def test_set_dni(self):
        self.paciente.set_dni("87654321")
        self.assertEqual(self.paciente.__dni__, "87654321")

    def test_set_nombre(self):
        self.paciente.set_nombre("Carlos Gómez")
        self.assertEqual(self.paciente.__nombre__, "Carlos Gómez")

    def test_set_nacimiento(self):
        self.paciente.set_nacimiento("02/02/1990")
        self.assertEqual(self.paciente.__fecha_nacimiento__, "02/02/1990")

    def test_obtener_nombre(self):
        self.assertEqual(self.paciente.obtener_nombre(), "El nombre del paciente es: Juan Pérez")

    def test_obtener_nacimiento(self):
        self.assertEqual(self.paciente.obtener_nacimiento(), "La fecha de nacimiento del paciente Juan Pérez es: 01/01/1980")

    def test_obtener_paciente(self):
        self.assertEqual(self.paciente.__str__(), "Paciente: Juan Pérez (DNI: 12345678) - Nacimiento: 01/01/1980")
    
    def test_creacion_paciente_dni_vacio(self):
        with self.assertRaises(ValueError):
            Paciente("", "Juan Pérez", "10/05/1980")  
        with self.assertRaises(ValueError):
            Paciente("   ", "Ana Gómez", "15/08/1995")  
    
    def test_creacion_paciente_nombre_vacio(self):
        with self.assertRaises(ValueError):
            Paciente("12345678", "", "10/05/1980")  
        with self.assertRaises(ValueError):
            Paciente("87654321", "   ", "15/08/1995")  
    
    def test_creacion_paciente_fecha_vacia(self):
        """Verifica error al crear paciente con fecha de nacimiento vacía"""
        with self.assertRaises(ValueError):
            Paciente("12345678", "Juan Pérez", "")
    
    def test_fecha_formato_invalido(self):
        with self.assertRaises(ValueError):
            Paciente("12345678", "Juan Pérez", "1980-05-10")  
        with self.assertRaises(ValueError):
            Paciente("87654321", "Ana Gómez", "10/05/80")

class TestEspecialidad(unittest.TestCase):
    
    def test_creacion_instancia(self):
        especialidad = Especialidad("Cardiología")
        self.assertEqual(especialidad.__tipo__, "Cardiología")
        self.assertEqual(especialidad.__dias__, [])

    def test_obtener_especialidad(self):
        especialidad = Especialidad("Neurología")
        self.assertEqual(especialidad.obtener_especialidad(), "Neurología")

    def test_set_especialidad(self):
        especialidad = Especialidad("Pediatría")
        especialidad.set_especialidad("Gastroenterología")
        self.assertEqual(especialidad.__tipo__, "Gastroenterología")

    def test_set_dias(self):
        especialidad = Especialidad("Dermatología")
        especialidad.set_dias("Lunes")
        especialidad.set_dias("Martes")
        self.assertEqual(especialidad.__dias__, ["Lunes", "Martes"])

    def test_verificar_dia_presente(self):
        especialidad = Especialidad("Oncología", ["Lunes", "Martes"])
        self.assertTrue(especialidad.verificar_dia("lunes"))
        self.assertTrue(especialidad.verificar_dia("MARTES"))
        self.assertFalse(especialidad.verificar_dia("miércoles"))

    def test_creacion_especialidad_tipo_vacio(self):
        """Verifica error al crear especialidad con tipo vacío"""
        with self.assertRaises(ValueError):
            Especialidad("")
    
    def test_creacion_con_dia_mal_escrito(self):
        """Verifica error al crear especialidad con día mal escrito"""
        with self.assertRaises(ValueError):
            Especialidad("Cardiología", ["Luns"])  
    
    def test_creacion_con_dia_inexistente(self):
        """Verifica error al crear especialidad con día inexistente"""
        with self.assertRaises(ValueError):
            Especialidad("Cardiología", ["Lunesday"]) 
    
    def test_evitar_dias_duplicados(self):
        with self.assertRaises(ValueError):
            Especialidad("Cardiología", ["Lunes", "lunes", "Miércoles"])  
        with self.assertRaises(ValueError):
            Especialidad("Dermatología", ["martes", "Martes", "Viernes"])  
    
    def test_evitar_dias_duplicados_creacion_case_insensitive(self):
        with self.assertRaises(ValueError):
            Especialidad("Cardiología", ["Lunes", "lunes", "Miércoles"])  
        with self.assertRaises(ValueError):
            Especialidad("Dermatología", ["martes", "MARTES", "Viernes"])  
    
    def test_str_con_dias(self):
        especialidad = Especialidad("Cardiología", ["Lunes", "Miércoles"])
        resultado = str(especialidad)
        self.assertEqual(
            resultado,
            "Especialidad: Cardiología - Días disponibles: Lunes, Miércoles"
        )

    def test_str_sin_dias(self):
        especialidad = Especialidad("Neurología")
        resultado = str(especialidad)
        self.assertEqual(
            resultado,
            "Especialidad: Neurología - Sin días asignados"
        )

class TestMedico(unittest.TestCase):
    
    def test_creacion_instancia(self):
        especialidad = Especialidad("Cardiología", ["Lunes", "Miércoles"])
        medico = Medico("12345", "Dr. Juan Pérez", especialidad)
        self.assertEqual(medico.__matricula__, "12345")
        self.assertEqual(medico.__nombre__, "Dr. Juan Pérez")
        self.assertEqual(especialidad.__tipo__, "Cardiología")
        self.assertEqual(especialidad.__dias__, ["Lunes", "Miércoles"])

    def test_obtener_matricula(self):
        medico = Medico("67890", "Dr. Ana López", Especialidad("Neurología"))
        self.assertEqual(medico.obtener_matricula(), "67890")

    def test_set_matricula(self):
        medico = Medico("11111", "Dr. Pedro Gómez", Especialidad("Pediatría"))
        medico.set_matricula("22222")
        self.assertEqual(medico.__matricula__, "22222")

    def test_set_nombreM(self):
        medico = Medico("33333", "Dr. María Torres", Especialidad("Dermatología"))
        medico.set_nombreM("Dr. Sofía Torres")
        self.assertEqual(medico.__nombre__, "Dr. Sofía Torres")

    def test_get_especialidad(self):
        especialidad = Especialidad("Oncología")
        medico = Medico("44444", "Dr. Luis Fernández", especialidad)
        self.assertEqual(medico.get_especialidad(especialidad), "La especialidad del Médico Dr. Luis Fernández es: Oncología")

    def test_set_especialidad(self):
        especialidad1 = Especialidad("Traumatología")
        especialidad2 = Especialidad("Cirugía")
        medico = Medico("55555", "Dr. Andrés Ruiz", especialidad1)
        medico.set_especialidad(especialidad2)
        self.assertEqual(medico.__especialidades__.__tipo__, "Cirugía")

    def test_verificar_disponibilidad_dia(self):
        especialidad = Especialidad("Gastroenterología", ["Lunes", "Jueves"])
        medico = Medico("66666", "Dr. Carla Muñoz", especialidad)
        self.assertTrue(medico.obtener_especialidad_para_dia("Jueves", "Gastroenterología"))
        self.assertFalse(medico.obtener_especialidad_para_dia("sábado", "Gastroenterología"))

    def test_obtener_dias_disponibles(self):
        especialidad = Especialidad("Endocrinología", ["Viernes"])
        medico = Medico("88888", "Dr. Paola Herrera", especialidad)
        self.assertEqual(medico.obtener_especialidad_para_dia("Viernes", "Endocrinología"), "Endocrinología")
    
    def test_creacion_medico_matricula_vacia(self):
        with self.assertRaises(ValueError):
            Medico("", "Dr. Carlos Mendoza", Especialidad("Neurología"))  
        with self.assertRaises(ValueError):
            Medico("   ", "Dr. Ana Gómez", Especialidad("Cardiología"))  

    def test_creacion_medico_nombre_vacio(self):
        with self.assertRaises(ValueError):
            Medico("56789", "", Especialidad("Neurología"))  
        with self.assertRaises(ValueError):
            Medico("78901", "   ", Especialidad("Pediatría"))  

    def test_agregar_especialidad_duplicada(self):
        especialidad = Especialidad("Cardiología")
        medico = Medico("56789", "Dr. Carlos Mendoza", [especialidad])

        with self.assertRaises(ValueError):
            medico.agregar_especialidad(especialidad)
    
    def test_agregar_nueva_especialidad_exitosa(self):
        """Verifica que se pueda agregar una nueva especialidad correctamente"""
        especialidad1 = Especialidad("Cardiología", ["Lunes"])
        medico = Medico("12345", "Dr. Juan Pérez", especialidad1)
        
        # Agregar nueva especialidad diferente
        especialidad2 = Especialidad("Neurología", ["Martes"])
        medico.set_especialidad(especialidad2)
        
        # Verificar que ambas especialidades estén presentes
        self.assertTrue(medico.get_especialidad(especialidad1))
        self.assertTrue(medico.get_especialidad(especialidad2))
    
    def test_agregar_especialidad(self):
        especialidad1 = Especialidad("Cardiología", ["Lunes"])
        especialidad2 = Especialidad("Neurología", ["Martes"])
        medico = Medico("12345", "Dr. Juan Pérez", [especialidad1])
    
        medico.agregar_especialidad(especialidad2)
    
        self.assertIn(especialidad2, medico.__especialidades__)
        self.assertEqual(len(medico.__especialidades__), 2)

    def test_agregar_especialidad_duplicada(self):
        especialidad = Especialidad("Cardiología", ["Lunes"])
        medico = Medico("12345", "Dr. Juan Pérez", [especialidad])
    
        with self.assertRaises(ValueError) as context:
            medico.agregar_especialidad(especialidad)
    
        self.assertIn("ya está asignada", str(context.exception))

    def test_get_nombre(self):
        medico = Medico("12345", "Dr. Juan Pérez", [])
        resultado = medico.get_nombre()
        self.assertEqual(resultado, "El nombre del Médico es: Dr. Juan Pérez")

    def test_get_especialidad(self):
        especialidad = Especialidad("Cardiología", ["Lunes"])
        medico = Medico("12345", "Dr. Juan Pérez", [especialidad])
        resultado = medico.get_especialidad(especialidad)
        self.assertEqual(resultado, "La especialidad del Médico Dr. Juan Pérez es: Cardiología")

    def test_str_medico(self):
        especialidad = Especialidad("Cardiología", ["Lunes"])
        medico = Medico("12345", "Dr. Juan Pérez", [especialidad])
        resultado = str(medico)
        self.assertIn("Dr. Juan Pérez", resultado)
        self.assertIn("12345", resultado)

class TestTurno(unittest.TestCase):
    
    def test_creacion_instancia(self):
        paciente = Paciente("12345678", "Juan Pérez", "01/01/1980")
        especialidad = Especialidad("Cardiología", ["Lunes", "Martes", "Miércoles"])
        medico = Medico("98765", "Dr. María López", especialidad)
        fecha = datetime(2025, 6, 10, 14, 30)

        turno = Turno(paciente, medico, fecha, especialidad)
        
        self.assertEqual(turno.__paciente__.__nombre__, "Juan Pérez")
        self.assertEqual(turno.__medico__.__nombre__, "Dr. María López")
        self.assertEqual(turno.__fecha_hora__, fecha)

    def test_obtener_fecha_hora(self):
        fecha = datetime(2025, 6, 10, 14, 30)
        especialidad = Especialidad("Neurología", ["Martes"])
        turno = Turno(Paciente("87654321", "Ana Gómez", "01/01/1980"), Medico("56789", "Dr. Carlos Mendoza", especialidad), fecha, especialidad)

        self.assertEqual(turno.obtener_fecha_hora(), fecha)

    def test_evitar_turnos_duplicados(self):
    
        clinica = Clinica()
        paciente = Paciente("12345678", "Juan Pérez", "01/01/1980")
        clinica.agregar_paciente(paciente)

        especialidad = Especialidad("Cardiología", ["Lunes", "Martes", "Miércoles"])
        clinica.agregar_especialidad(especialidad)

        medico = Medico("98765", "Dr. María López", especialidad)
        clinica.agregar_medico(medico)

        fecha = datetime(2025, 12, 16, 14, 30)
    
        # Primer turno
        resultado1 = clinica.agendar_turno(fecha, "12345678", "98765", especialidad)
        self.assertIn("Turno para", resultado1)
        self.assertIn("agregado", resultado1)
    
        # Verificar que se agregó el turno
        print(f"Turnos en la clínica después del primer agendar: {len(clinica.__turnos__)}")
    
        # Segundo turno idéntico
        try:
            resultado2 = clinica.agendar_turno(fecha, "12345678", "98765", especialidad)
            # Si llegamos aquí, no se lanzó la excepción
            self.fail(f"Se esperaba TurnoDuplicadoError pero se obtuvo: {resultado2}")
        except TurnoDuplicadoError as e:
            # Esto es lo que esperamos
            error_message = str(e)
            self.assertIn("Ya existe un turno", error_message)
            self.assertIn("Dr. María López", error_message)
            self.assertIn("16/12/2025 14:30", error_message)
        except Exception as e:
            self.fail(f"Se esperaba TurnoDuplicadoError pero se obtuvo {type(e).__name__}: {e}")

    def test_error_si_paciente_o_medico_no_existen(self):
        fecha = datetime(2025, 6, 10, 14, 30)
        especialidad = Especialidad("Cardiología")

        # Caso paciente inexistente
        with self.assertRaises(ValueError):
            turno = Turno(None, Medico("98765", "Dr. María López", especialidad), fecha, especialidad)

        # Caso médico inexistente
        with self.assertRaises(ValueError):
            turno = Turno(Paciente("12345678", "Juan Pérez", "01/01/1980"), None, fecha, especialidad)

    def test_error_medico_no_atiende_especialidad_solicitada(self):
        paciente = Paciente("12345678", "Juan Pérez", "01/01/1980")
        especialidad = Especialidad("Neurología")  
        medico = Medico("98765", "Dr. María López", Especialidad("Cardiología", ["Lunes", "Miércoles"]))
        fecha = datetime(2025, 6, 10, 14, 30)

        with self.assertRaises(ValueError):
            Turno(paciente, medico, fecha, especialidad)

    def test_error_medico_no_trabaja_ese_dia(self):
        paciente = Paciente("12345678", "Juan Pérez", "01/01/1980")
        especialidad = Especialidad("Cardiología", ["Lunes", "Miércoles"])  # Días válidos
        medico = Medico("98765", "Dr. María López", especialidad)
        fecha_invalida = datetime(2025, 6, 12, 14, 30)  # Jueves (no trabaja este día)

        with self.assertRaises(ValueError):
            Turno(paciente, medico, fecha_invalida, especialidad)
    
    def test_obtener_medico(self):
        paciente = Paciente("12345678", "Ana Gómez", "10/6/1996")
        especialidad = Especialidad("Pediatría", ["martes"])
        medico = Medico("9876", "Dr. Sosa", [especialidad])
        fecha_hora = datetime(2025, 6, 17, 14, 30)  # Martes

        turno = Turno(paciente, medico, fecha_hora, especialidad)
        
        resultado = turno.obtener_medico()
        
        self.assertEqual(resultado, medico)
        self.assertEqual(resultado.__nombre__, "Dr. Sosa")
        self.assertEqual(resultado.__matricula__, "9876")
    
    def test_str_turno(self):
        paciente = Paciente("12345678", "Ana Gómez", "10/6/1996")  # Asegurate de que la clase exista
        especialidad = Especialidad("Pediatría", ["martes"])
        medico = Medico("9876", "Dr. Sosa", [especialidad])
        fecha_hora = datetime(2025, 6, 17, 14, 30)  # Esto cae un martes

        turno = Turno(paciente, medico, fecha_hora, especialidad)

        resultado = str(turno)
        self.assertIn("Paciente: Ana Gómez", resultado)
        self.assertIn("Médico: Dr. Sosa", resultado)
        self.assertIn("17/06/2025 14:30", resultado)
        self.assertIn("Especialidad: Pediatría", resultado)

class TestReceta(unittest.TestCase):
    
    def test_creacion_instancia(self):
        paciente = Paciente("11223344", "Carlos Gómez", "01/01/1980")
        especialidad = Especialidad("Cardiología")
        medico = Medico("A7890", "Dr. Valeria López", especialidad)
        medicamentos = ["Aspirina", "Ibuprofeno"]
        fecha = datetime(2025, 6, 10)

        receta = Receta(paciente, medico, medicamentos, fecha)

        self.assertEqual(receta.__paciente__.__nombre__, "Carlos Gómez")
        self.assertEqual(receta.__medico__.__nombre__, "Dr. Valeria López")
        self.assertEqual(receta.__medicamentos__, ["Aspirina", "Ibuprofeno"])
        self.assertEqual(receta.__fecha__, fecha)

    def test_creacion_instancia_sin_fecha(self):
        paciente = Paciente("55667788", "Laura Fernández", "01/01/1980")
        medico = Medico("B6543", "Dr. Juan Pérez", Especialidad("Neurología"))
        medicamentos = ["Paracetamol"]

        receta = Receta(paciente, medico, medicamentos)

        self.assertEqual(receta.__medicamentos__, ["Paracetamol"])
        self.assertIsInstance(receta.__fecha__, datetime)  # Verifica que la fecha se haya generado automáticamente

    def test_agregar_medicamentos(self):
        paciente = Paciente("99887766", "Ana Ramírez", "01/01/1980")
        medico = Medico("C1234", "Dr. Mariana Gómez", Especialidad("Dermatología"))
        receta = Receta(paciente, medico, ["Amoxicilina"])

        receta.agregar_medicamentos("Diclofenaco")

        self.assertIn("Diclofenaco", receta.__medicamentos__)
    
    def test_error_si_paciente_o_medico_no_existen(self):
        # Caso paciente inexistente
        with self.assertRaises(ValueError):
            Receta(None, Medico("A7890", "Dr. Valeria López", Especialidad("Cardiología")), ["Paracetamol"])

        # Caso médico inexistente
        with self.assertRaises(ValueError):
            Receta(Paciente("11223344", "Carlos Gómez", "01/01/1980"), None, ["Ibuprofeno"])

    def test_error_si_no_hay_medicamentos_listados(self):
        paciente = Paciente("22334455", "Miguel Rojas", "01/01/1980")
        medico = Medico("D5678", "Dr. Fernando López", Especialidad("Cardiología"))

        with self.assertRaises(ValueError):  # Asegura que se lanza un error
           Receta(paciente, medico, [])

    def test_verificar_str_receta(self):
        paciente = Paciente("44556677", "Gabriel Torres", "01/01/1980")
        medico = Medico("F8901", "Dr. Elena Suárez", Especialidad("Oftalmología"))
        receta = Receta(paciente, medico, ["Gotas para ojos"])

        resultado_str = str(receta)
        self.assertIn("Gotas para ojos", resultado_str)
        self.assertIn("Dr. Elena Suárez", resultado_str)
        self.assertIn("Gabriel Torres", resultado_str)

    def test_confirmar_medico_asignado(self):
        paciente = Paciente("55667788", "Laura Fernández", "01/01/1980")
        especialidad = Especialidad("Neurología", ["Lunes", "Martes"])
        medico = Medico("B6543", "Dr. Juan Pérez", especialidad)
        receta = Receta(paciente, medico, ["Paracetamol"])

        self.assertEqual(receta.__medico__, medico)

    def test_confirmar_medicamentos_guardados(self):
        paciente = Paciente("66778899", "Pedro Méndez", "01/01/1980")
        especialidad = Especialidad("Endocrinología", ["Miércoles"])
        medico = Medico("G9012", "Dr. Tomás López", especialidad)
        receta = Receta(paciente, medico, ["Insulina", "Metformina"])

        self.assertEqual(receta.__medicamentos__, ["Insulina", "Metformina"])
        receta.agregar_medicamentos("Levotiroxina")
        self.assertIn("Levotiroxina", receta.__medicamentos__)
    
    def test_str_receta(self):
        paciente = Paciente("12345678", "Ana Gómez", "01/01/1980")
        especialidad = Especialidad("Clínica Médica", ["lunes"])
        medico = Medico("9876", "Dr. Sosa", [especialidad])
        fecha = datetime(2025, 6, 16)  # lunes
        medicamentos = ["Paracetamol", "Ibuprofeno"]

        receta = Receta(paciente, medico, medicamentos, fecha)
        resultado = str(receta)

        self.assertIn("Receta [16/06/2025]", resultado)
        self.assertIn("Paracetamol", resultado)
        self.assertIn("Ibuprofeno", resultado)
        self.assertIn("Dr. Sosa", resultado)
        self.assertIn("Ana Gómez", resultado)

class TestHistoriaClinica(unittest.TestCase):

    def test_creacion_instancia(self):
        paciente = Paciente("11223344", "Carlos Gómez", "01/01/1980")
        historia = HistoriaClinica(paciente)

        self.assertEqual(historia.__paciente__.__nombre__, "Carlos Gómez")
        self.assertEqual(historia.__turnos__, [])
        self.assertEqual(historia.__recetas__, [])

    def test_agregar_turno(self):
        paciente = Paciente("44556677", "Ana Ramírez", "01/01/1980")
        historia = HistoriaClinica(paciente)
        especialidad = Especialidad("Dermatología", ["Viernes"])
        medico = Medico("C1234", "Dr. Mariana Gómez", [especialidad])
        fecha = datetime(2025, 6, 13, 10, 30)
        turno = Turno(paciente, medico, fecha, especialidad)

        historia.agregar_turno_a_lista(turno)
        self.assertIn(turno, historia.__turnos__)

    def test_agregar_receta(self):
        paciente = Paciente("99887766", "Roberto Díaz", "01/01/1980")
        especialidad = Especialidad("Pediatría", ["Jueves"])
        fecha = datetime(2025, 6, 12, 10, 30)
        medico = Medico("D7896", "Dr. Felipe Muñoz", especialidad)
        receta = Receta(paciente, medico, ["Ibuprofeno", "Omeprazol"])
        historia = HistoriaClinica(paciente)

        historia.agregar_receta_hist(receta)
        self.assertIn(receta, historia.__recetas__)

    def test_obtener_turnos(self):
        paciente = Paciente("55667788", "Laura Fernández", "01/01/1980")
        historia = HistoriaClinica(paciente)
        especialidad = Especialidad("Neurología", ["Viernes"])
        medico = Medico("B6543", "Dr. Juan Pérez", especialidad)
        fecha = datetime(2025, 6, 20, 15, 45)
        turno = Turno(paciente, medico, fecha, especialidad)
        historia.agregar_turno_a_lista(turno)

        self.assertIn(str(turno), historia.obtener_turnos())

    def test_obtener_receta(self):
        paciente = Paciente("11223344", "Carlos Pérez", "01/01/1980")
        historia = HistoriaClinica(paciente)
        medico = Medico("A1234", "Dr. Sofía Torres", Especialidad("Endocrinología"))
        receta = Receta(paciente, medico, ["Paracetamol"])
        historia.agregar_receta_hist(receta)

        self.assertIn(str(receta), historia.obtener_receta())
    
    def test_error_agregar_turno_paciente_no_existe(self):
        historia = HistoriaClinica(None)
        especialidad = Especialidad("Dermatología")
        medico = Medico("C1234", "Dr. Mariana Gómez", [especialidad])
        fecha = datetime(2025, 6, 15, 10, 30)

        with self.assertRaises(ValueError):
            turno = Turno(None, medico, fecha, especialidad)
            historia.agregar_turno_a_lista(turno)

    def test_error_agregar_receta_medico_no_existe(self):
        paciente = Paciente("66778899", "Pedro Méndez", "01/01/1980")
        historia = HistoriaClinica(paciente)

        with self.assertRaises(ValueError):
            receta = Receta(paciente, None, ["Insulina"])
            historia.agregar_receta_hist(receta)

    def test_formato_str_historia_clinica(self):
        paciente = Paciente("33445566", "Sofía Méndez", "01/01/1980")
        historia = HistoriaClinica(paciente)

        resultado_str = str(historia)
        self.assertIn("Historia Clínica de Sofía Méndez", resultado_str)
        self.assertIn("Sin turnos", resultado_str)
        self.assertIn("Sin recetas", resultado_str)

    def test_obtener_turnos_y_recetas_formato_correcto(self):
        paciente = Paciente("22334455", "Luis Sánchez", "01/01/1980")
        historia = HistoriaClinica(paciente)
        medico = Medico("D5678", "Dr. Fernando López", Especialidad("Cardiología"))
        receta = Receta(paciente, medico, ["Ibuprofeno"])
        historia.agregar_receta_hist(receta)
        resultado_recetas = historia.obtener_receta()

        self.assertIn("Las Recetas son:", resultado_recetas)
        self.assertIn("Ibuprofeno", resultado_recetas)
    
    def test_str_historia_clinica(self):
        paciente = Paciente("11223344", "Carlos Gómez", "01/01/1980")
        historia = HistoriaClinica(paciente)

        # Caso 1: sin turnos ni recetas
        self.assertEqual(str(historia), "Historia Clínica de Carlos Gómez - Sin turnos, Sin recetas")

        # Caso 2: con 1 turno y 1 receta
        especialidad = Especialidad("Cardiología")
        medico = Medico("A7890", "Dr. Valeria López", especialidad)
        especialidad = Especialidad("Dermatología", ["Martes"])
        turno = Turno(paciente, medico, datetime(2025, 6, 10, 14, 0), especialidad)
        receta = Receta(paciente, medico, ["Aspirina", "Ibuprofeno"], datetime(2025, 6, 10))

        historia.agregar_turno_a_lista(turno)
        historia.agregar_receta_hist(receta)

        self.assertEqual(str(historia), "Historia Clínica de Carlos Gómez - 1 turno(s), 1 receta(s)")

class TestClinica(unittest.TestCase):

    def test_creacion_instancia(self):
        clinica = Clinica()
        self.assertEqual(clinica.__pacientes__, {})
        self.assertEqual(clinica.__medicos__, {})
        self.assertEqual(clinica.__turnos__, [])
        self.assertEqual(clinica.__historias_clinicas__, {})
        self.assertEqual(clinica.__especialidades__, [])

    def test_agregar_paciente(self):
        clinica = Clinica()
        paciente = Paciente("12345678", "Juan Pérez", "01/01/1980")
        clinica.agregar_paciente(paciente)
        self.assertIn("12345678", clinica.__pacientes__)

    def test_agregar_paciente_duplicado(self):
        clinica = Clinica()
        paciente = Paciente("87654321", "Ana Gómez", "01/01/1980")
        clinica.agregar_paciente(paciente)
        with self.assertRaises(PacienteYaExisteError):
            clinica.agregar_paciente(paciente)

    def test_agregar_medico(self):
        clinica = Clinica()
        medico = Medico("56789", "Dr. Carlos Mendoza", Especialidad("Neurología"))
        clinica.agregar_medico(medico)
        self.assertIn("56789", clinica.__medicos__)

    def test_agregar_medico_duplicado(self):
        clinica = Clinica()
        medico = Medico("78901", "Dr. Laura Fernández", Especialidad("Pediatría"))
        clinica.agregar_medico(medico)
        with self.assertRaises(MedicoYaExisteError):
            clinica.agregar_medico(medico)

    def test_agendar_turno(self):
        clinica = Clinica()
        paciente = Paciente("44556677", "Roberto Díaz", "01/01/1980")
        clinica.agregar_paciente(paciente)
        especialidad = Especialidad("Cardiología", ["Viernes"])
        medico = Medico("22222", "Dr. Sofía Torres", especialidad)
        clinica.agregar_medico(medico)
        fecha_hora = datetime(2025, 6, 20, 10, 30)

        resultado = clinica.agendar_turno(fecha_hora, "44556677", "22222", especialidad)
        self.assertIn("Turno para", resultado)

    def test_agendar_turno_pasado(self):
        clinica = Clinica()
        paciente = Paciente("99887766", "Carlos Pérez", "01/01/1980")
        clinica.agregar_paciente(paciente)
        especialidad = Especialidad("Dermatología")
        medico = Medico("33333", "Dr. Mariana Gómez", especialidad)
        clinica.agregar_medico(medico)
        fecha_hora = datetime(2023, 6, 20, 10, 30)

        with self.assertRaises(ValueError):
            clinica.agendar_turno(fecha_hora, "99887766", "33333", especialidad)

    def test_emitir_receta(self):
        clinica = Clinica()
        paciente = Paciente("55667788", "Laura Fernández", "01/01/1980")
        clinica.agregar_paciente(paciente)
        medico = Medico("44444", "Dr. Juan Pérez", Especialidad("Neurología"))
        clinica.agregar_medico(medico)
        medicamentos = ["Paracetamol", "Ibuprofeno"]

        resultado = clinica.emitir_receta("55667788", "44444", medicamentos)
        self.assertIn("Receta emitida", resultado)
    
    def test_emitir_receta_medico_no_existe(self):
        clinica = Clinica()
        paciente = Paciente("55667788", "Laura Fernández", "01/01/1980")
        clinica.agregar_paciente(paciente)
        medicamentos = ["Paracetamol", "Ibuprofeno"]

        with self.assertRaises(MedicoNoExisteError) as context:
            clinica.emitir_receta("55667788", "44444", medicamentos)
    
        self.assertIn("44444", str(context.exception))
    
    def test_emitir_receta_invalida_medicamentos_vacios(self):
        clinica = Clinica()
        paciente = Paciente("55667788", "Laura Fernández", "01/01/1980")
        clinica.agregar_paciente(paciente)
        medico = Medico("44444", "Dr. Juan Pérez", Especialidad("Neurología"))
        clinica.agregar_medico(medico)
        medicamentos_vacios = []  

        with self.assertRaises(RecetaInvalidaError) as context:
            clinica.emitir_receta("55667788", "44444", medicamentos_vacios)
    
        self.assertIn("al menos un medicamento", str(context.exception))

    def test_obtener_historia_clinica(self):
        clinica = Clinica()
        paciente = Paciente("66778899", "Ricardo Gómez", "01/01/1980")
        clinica.agregar_paciente(paciente)

        historia = clinica.obtener_historia_clinica("66778899")
        self.assertIsInstance(historia, HistoriaClinica)
    
    def test_evitar_especialidades_duplicadas(self):
        clinica = Clinica()
    
        especialidad_1 = Especialidad("Cardiología", ["Lunes", "Miércoles"])
        especialidad_2 = Especialidad("Cardiología", ["Martes", "Jueves"])  # Misma especialidad con diferente capitalización

        clinica.agregar_especialidad(especialidad_1)  # Primer agregado

        with self.assertRaises(ValueError):  # Segundo intento debe fallar
            clinica.agregar_especialidad(especialidad_2)  

    def test_turno_agendado_dia_invalido(self):
        clinica = Clinica()
        paciente = Paciente("11122233", "Julia Rojas", "01/01/1985")
        clinica.agregar_paciente(paciente)
        especialidad = Especialidad("Ortopedia", ["Martes", "Jueves"])
        medico = Medico("55555", "Dr. Manuel Gómez", especialidad)
        clinica.agregar_medico(medico)
        fecha_hora = datetime(2025, 6, 21, 14, 00)  

        with self.assertRaises(ValueError):
            clinica.agendar_turno(fecha_hora, "11122233", "55555", especialidad)

    def test_verificar_formato_historia_clinica(self):
        clinica = Clinica()
        paciente = Paciente("22233344", "Esteban Morales", "01/01/1980")
        clinica.agregar_paciente(paciente)

        historia = clinica.obtener_historia_clinica("22233344")
        resultado_str = str(historia)
        self.assertIn("Historia Clínica de Esteban Morales", resultado_str)
        self.assertIn("Sin turnos", resultado_str)
        self.assertIn("Sin recetas", resultado_str)
    
    def test_agregar_especialidad(self):
        clinica = Clinica()

        especialidad1 = Especialidad("Pediatría")
        especialidad2 = Especialidad("pediatría")  # mismo nombre pero distinto casing

        # Caso feliz: se agrega una especialidad nueva
        clinica.agregar_especialidad(especialidad1)
        self.assertIn(especialidad1, clinica.__especialidades__)

        # Caso duplicado: se intenta agregar la misma especialidad con diferente casing/espacios
        with self.assertRaises(ValueError) as context:
            clinica.agregar_especialidad(especialidad2)
        self.assertIn("ya está registrada en la clínica", str(context.exception).lower())
    
    def test_obtener_medico_por_matricula(self):
        clinica = Clinica()
        medico = Medico("12345", "Dr. Test", Especialidad("Traumatología"))
        clinica.agregar_medico(medico)
        obtenido = clinica.obtener_medico_por_matricula("12345")
        self.assertEqual(obtenido, medico)
    
    def test_obtener_medico_por_matricula_inexistente(self):
        clinica = Clinica()
        with self.assertRaises(MedicoNoExisteError):
            clinica.obtener_medico_por_matricula("00000")
    
    def test_obtener_pacientes(self):
        clinica = Clinica()
        paciente = Paciente("12345678", "Paciente Test", "01/01/1980")
        clinica.agregar_paciente(paciente)
        pacientes = clinica.obtener_pacientes()
        self.assertIn(paciente, pacientes)

    def test_obtener_medicos(self):
        clinica = Clinica()
        medico = Medico("99999", "Dr. House", Especialidad("Diagnóstico"))
        clinica.agregar_medico(medico)
        medicos = clinica.obtener_medicos()
        self.assertIn(medico, medicos)
    
    def test_obtener_turnos(self):
        clinica = Clinica()
        paciente = Paciente("11111111", "Paciente Turno", "01/01/1980")
        especialidad = Especialidad("Neurología", ["Lunes"])
        medico = Medico("123456", "Dr. Cerebro", especialidad)
        clinica.agregar_paciente(paciente)
        clinica.agregar_medico(medico)
        fecha = datetime(2025, 6, 23, 9, 0)  # Lunes

        clinica.agendar_turno(fecha, "11111111", "123456", especialidad)
        turnos = clinica.obtener_turnos()
        self.assertIn("Turnos programados:", turnos)
    
    def test_validar_existencia_paciente(self):
        clinica = Clinica()
        paciente = Paciente("12312312", "Paciente Existente", "01/01/1980")
        clinica.agregar_paciente(paciente)
        self.assertTrue(clinica.validar_existencia_paciente("12312312"))
        self.assertFalse(clinica.validar_existencia_paciente("00000000"))
    
    def test_validar_existencia_medico(self):
        clinica = Clinica()
        medico = Medico("654321", "Dr. Presente", Especialidad("Clínica"))
        clinica.agregar_medico(medico)
        self.assertTrue(clinica.validar_existencia_medico("654321"))
        self.assertFalse(clinica.validar_existencia_medico("111111"))

    def test_validar_turno_no_duplicado(self):
        clinica = Clinica()
        paciente = Paciente("30303030", "Luis Miguel", "01/01/1990")
        clinica.agregar_paciente(paciente)
        especialidad = Especialidad("Oftalmología", ["Miércoles"])
        clinica.agregar_especialidad(especialidad)
        medico = Medico("202020", "Dra. Rosa", especialidad)
        clinica.agregar_medico(medico)
        fecha = datetime(2025, 6, 18, 10, 0)  # Miércoles

        # Agenda el turno
        clinica.agendar_turno(fecha, "30303030", "202020", especialidad)

        # Ahora sí valida que no hay turno duplicado (debería devolver False)
        self.assertFalse(clinica.validar_turno_no_duplicado("202020", fecha))

    def test_validar_especialidad_en_dia(self):
        clinica = Clinica()
        especialidad = Especialidad("Oncología", ["Miércoles"])
        medico = Medico("909090", "Dr. Tumor", especialidad)
        clinica.agregar_especialidad(especialidad)
        self.assertTrue(clinica.validar_especialidad_en_dia(medico, "Oncología", "Miércoles"))
        self.assertFalse(clinica.validar_especialidad_en_dia(medico, "Oncología", "Lunes"))

    def test_obtener_especialidad_disponible(self):
        clinica = Clinica()
        especialidad = Especialidad("Dermatología", ["Jueves"])
        clinica.agregar_especialidad(especialidad)

        medico = Medico("202020", "Dra. Rosa", especialidad)
        clinica.agregar_medico(medico)

        fecha = datetime(2025, 6, 19, 14, 0)  # Jueves
        dia_semana = clinica.obtener_dia_semana_en_espanol(fecha)

        respuesta = clinica.obtener_especialidad_disponible(medico.obtener_matricula(), dia_semana, especialidad)
        self.assertIn("está disponible el día Jueves", respuesta)

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.cli = CLI()

    @patch("builtins.input", side_effect=["12345678", "Juan Pérez", "10/05/1980"])
    @patch("builtins.print")
    def test_agregar_paciente(self, mock_print, mock_input):
        self.cli.agregar_paciente()
        self.assertIn("12345678", self.cli.clinica.__pacientes__)
        mock_print.assert_any_call("Paciente Juan Pérez agregado exitosamente")

    @patch("builtins.input", side_effect=["87654321", "Ana Gómez", "Neurología"])
    @patch("builtins.print")
    def test_agregar_medico(self, mock_print, mock_input):
        self.cli.agregar_medico()
        self.assertIn("87654321", self.cli.clinica.__medicos__)
        mock_print.assert_any_call("Dr. Ana Gómez agregado exitosamente")

    @patch("builtins.input", side_effect=["87654321", "Ana Gómez", "Neurología"])
    @patch("builtins.print")
    def test_agregar_medico_duplicado(self, mock_print, mock_input):
        self.cli.agregar_medico()
        with patch("builtins.input", side_effect=["87654321", "Ana Gómez", "Neurología"]):
            with patch("src.clinica.Clinica.agregar_medico", side_effect=MedicoYaExisteError("Médico duplicado")):
                self.cli.agregar_medico()
                mock_print.assert_any_call("Médico duplicado")
    
    @patch("builtins.input", side_effect=["87654321"])
    @patch("builtins.print")
    def test_mostrar_medico_por_matricula(self, mock_print, mock_input):
        with patch("src.clinica.Clinica.obtener_medico_por_matricula", return_value="Dr. Ana Gómez - Neurología"):
            self.cli.buscar_medico_por_matricula("87654321")
            mock_print.assert_any_call("\nMédico encontrado: Dr. Ana Gómez - Neurología")

    @patch("builtins.input", side_effect=["99999999", "33333", "10/07/2025 09:00"])
    @patch("builtins.print")
    def test_agendar_turno_paciente_no_existe(self, mock_print, mock_input):
        with patch("src.clinica.Clinica.agendar_turno", side_effect=PacienteNoExisteError("No existe paciente con DNI 99999999")):
            self.cli.agendar_turno()
            mock_print.assert_any_call("Error: No existe paciente con DNI 99999999")

    @patch("builtins.input", side_effect=["99", "0", "abc", "13", "12"])  
    @patch("builtins.print")
    def test_menu_opciones_invalidas(self, mock_print, mock_input):
        self.cli.ejecutar()
        mock_print.assert_any_call("Opción inválida. Por favor seleccione del 1 al 12.")

    @patch("builtins.input", side_effect=["55667788"])
    @patch("builtins.print")
    def test_ver_historia_clinica(self, mock_print, mock_input):
        with patch("src.clinica.Clinica.obtener_historia_clinica", return_value="Historia Clínica de Laura Fernández"):
            self.cli.ver_historia_clinica()
            mock_print.assert_any_call("Historia Clínica de Laura Fernández")

    @patch("builtins.input", side_effect=["12"])
    @patch("builtins.print")
    def test_cerrar_sistema(self, mock_print, mock_input):
        self.cli.ejecutar()
        mock_print.assert_any_call("¡Gracias por usar el sistema de la clínica!")

    @patch("builtins.input", side_effect=["12345678", "202020", "Paracetamol, Ibuprofeno"])
    @patch("builtins.print")
    def test_emitir_receta(self, mock_print, mock_input):
        with patch("src.clinica.Clinica.emitir_receta", return_value="Receta emitida correctamente"):
            self.cli.emitir_receta()
            mock_print.assert_any_call("Receta emitida exitosamente")
            mock_print.assert_any_call("Receta emitida correctamente")

    @patch("builtins.print")
    def test_ver_todos_los_turnos(self, mock_print):
        turnos_mock = ["Turno 1", "Turno 2"]
        with patch("src.clinica.Clinica.obtener_turnos", return_value=turnos_mock):
            self.cli.ver_todos_los_turnos()
            mock_print.assert_any_call("\n--- TODOS LOS TURNOS ---")
            mock_print.assert_any_call("1. Turno 1")
            mock_print.assert_any_call("2. Turno 2")

    @patch("builtins.print")
    def test_ver_todos_los_medicos(self, mock_print):
        medicos_mock = ["Dr. Ana Gómez", "Dr. Juan Pérez"]
        with patch("src.clinica.Clinica.obtener_medicos", return_value=medicos_mock):
            self.cli.ver_todos_los_medicos()
            mock_print.assert_any_call("\n--- TODOS LOS MÉDICOS ---")
            mock_print.assert_any_call("1. Dr. Ana Gómez")
            mock_print.assert_any_call("2. Dr. Juan Pérez")

    @patch("builtins.input", side_effect=["Cardiología", "Lunes", "Miércoles", ""])  # Termina con Enter vacío
    @patch("builtins.print")
    def test_agregar_especialidad(self, mock_print, mock_input):
        with patch("src.clinica.Clinica.agregar_especialidad") as mock_agregar:
            self.cli.agregar_especialidad()
            mock_agregar.assert_called()
            mock_print.assert_any_call("Especialidad Cardiología agregada exitosamente")
            mock_print.assert_any_call("Días disponibles: Lunes, Miércoles")

    @patch("builtins.input", side_effect=["202020", "Lunes"])
    @patch("builtins.print")
    def test_obtener_especialidad_disponible(self, mock_print, mock_input):
        # Simular que la matrícula existe en la clínica
        self.cli.clinica.__medicos__["202020"] = "Médico Mock"
        
        with patch("src.clinica.Clinica.obtener_especialidad_disponible", return_value="Especialidad disponible en Lunes"):
            self.cli.obtener_especialidad_disponible()
            mock_print.assert_any_call("Especialidad disponible en Lunes")

if __name__ == "__main__":
    unittest.main()