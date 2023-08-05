Cierre contable del ejercicio fiscal español
============================================

Reemplaza el asistente por defecto de OpenERP para el cierre contable (del
módulo *account*) por un asistente todo en uno más avanzado que permite:

 * Comprobar asientos descuadrados.
 * Comprobar fechas y periodos incorrectos de los apuntes.
 * Comprobar si hay asientos sin asentar en el ejercicio a cerrar.
 * Crear el asiento de pérdidas y ganancias.
 * Crear el asiento de pérdidas y ganancias de patrimonio neto.
 * Crear el asiento de cierre.
 * Crear el asiento de apertura.

Permite configurar todos los parámetros para la realización de los asientos,
aunque viene preconfigurado para el actual plan de cuentas español.

Para la creación de los asientos, se tiene en cuenta el método de cierre
definido en los tipos de cuenta (siempre que la cuenta no sea de tipo view):

 * Ninguno: No se realiza ningún cierre para esa cuenta.
 * Saldo: Crea un apunte para la cuenta con el saldo del ejercicio.
 * No conciliados: Crea un apunte por cada empresa con saldo para la cuenta.
 * Detalle: No soportado.

También conserva el estado del cierre, por lo que el usuario puede cancelar y
deshacer las operaciones fácilmente.


