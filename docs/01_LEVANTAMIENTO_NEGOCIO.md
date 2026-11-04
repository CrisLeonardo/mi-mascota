# 1. Levantamiento de información del negocio

> **Transparencia sobre el origen de la información.** El proyecto se desarrolló sobre el caso que plantea el propio
> enunciado del curso: la **Veterinaria "Mi Mascota"**, cuyo problema (citas por llamadas telefónicas y agenda física)
> y solución (administrar clientes, mascotas, servicios, citas y expedientes) vienen descritos en el PDF del proyecto.
> **No se realizó una visita ni una entrevista a una veterinaria real**; los datos operativos de esta sección
> (personal, horario, volumen de clientes) son **supuestos razonables** para dimensionar el sistema, no cifras
> medidas. Todo es configurable desde variables de entorno (nombre, teléfono, dirección y horario), de modo que el
> sistema se puede adaptar a un negocio concreto sin tocar código.

## 1. Datos del negocio

| Dato | Valor |
|---|---|
| Nombre | Veterinaria "Mi Mascota" (caso del enunciado) |
| Giro | Clínica veterinaria de consulta general, vacunación y estética |
| Ubicación | Ciudad de Guatemala (supuesto) |
| Personal | 1 administrador/dueño, 1 recepcionista, 2 veterinarios (supuesto) |
| Horario | Lunes a sábado, 8:00 a 17:00 (supuesto) |
| Clientes atendidos | Aproximadamente 15 a 25 por día (supuesto) |

## 2. Escenario de trabajo (no es una entrevista real)

Las preguntas son las que se harían a la veterinaria; las respuestas son el **escenario descrito por el enunciado y
supuestos típicos del sector**, no declaraciones de una persona entrevistada.

| # | Pregunta | Escenario considerado |
|---|---|---|
| 1 | ¿Cómo registran hoy las citas? | Por llamada telefónica o WhatsApp, anotadas en una agenda de papel. |
| 2 | ¿Qué pasa cuando dos clientes piden la misma hora? | A veces se duplican citas y un veterinario queda con dos pacientes a la vez. |
| 3 | ¿Dónde guardan el historial de cada mascota? | En fichas de papel dentro de un archivero; algunas se pierden o están incompletas. |
| 4 | ¿Cómo saben cuándo toca el refuerzo de una vacuna? | Dependen de la memoria del veterinario o de que el cliente llame. |
| 5 | ¿Cómo saben cuánto vendieron en el mes? | Suman recibos a mano al final del mes. |
| 6 | ¿Quién debe poder ver o modificar qué? | El dueño todo; la recepción clientes y citas; los veterinarios el historial clínico. |

## 3. Problema actual

1. **Citas en agenda de papel**: se duplican, se pierden y no hay forma de saber qué horarios están libres sin revisar a mano.
2. **Expedientes clínicos dispersos**: el historial de una mascota (consultas, tratamientos, vacunas) está en papeles
   que se extravían, y el veterinario no puede consultar rápido qué se le hizo antes.
3. **Sin control de vacunas**: no hay recordatorio de refuerzos, lo que reduce la salud de las mascotas y las ventas de la clínica.
4. **Sin información para decidir**: el dueño no sabe cuántas citas hay, cuántas se cancelan ni cuánto ingresó.
5. **Sin control de acceso**: cualquiera con acceso a la agenda o al archivero puede ver o alterar todo.

## 4. Necesidad

Un sistema web accesible desde cualquier computadora o celular de la clínica que permita:

- Registrar clientes y sus mascotas una sola vez.
- Agendar citas sin choques de horario y ver la agenda del día.
- Guardar el expediente clínico digital de cada mascota (consultas y vacunas).
- Saber qué refuerzos de vacuna se acercan.
- Ver indicadores del negocio (citas, ingresos).
- Que cada empleado vea y haga solo lo que le corresponde.

## 5. Solución propuesta

Aplicación web **"Mi Mascota"** desarrollada con Django (Python), base de datos relacional PostgreSQL, interfaz
responsiva con Bootstrap 5 y una API REST para las operaciones dinámicas (horarios libres, cambio de estado,
gráficas). Funciona en computadora y celular, y está desplegada en Internet.

| Problema | Cómo lo resuelve el sistema |
|---|---|
| Citas duplicadas | El sistema **bloquea traslapes** por veterinario y por mascota, y solo ofrece horas libres. |
| Fichas de papel | **Expediente digital** por mascota con consultas, diagnóstico, tratamiento y vacunas. |
| Refuerzos olvidados | Listado y panel de **refuerzos de vacuna** de los próximos 30 días, con teléfono del dueño. |
| Falta de datos | **Panel** con citas del día, ingresos de los últimos 30 días y gráficas. |
| Acceso sin control | **Roles** (administrador, recepción, veterinario) con permisos distintos. |

## 6. Beneficios esperados

- Eliminar citas duplicadas.
- Reducir el tiempo de búsqueda de un historial de minutos a segundos.
- Aumentar la aplicación de refuerzos de vacunas.
- Contar con información para tomar decisiones.
