from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UbicacionGeografica(Base):
    __tablename__ = "ubicacion_geografica"

    id = Column(Integer, primary_key=True)
    departamento = Column(String)
    municipio = Column(String)
    entidad = Column(String)
    correo = Column(String)
    direccion = Column(String)
    telefono = Column(String)

    def __repr__(self):
        return f"<Device from = {self.entidad} located in {self.municipio}, {self.departamento}>"


class InformacionGeneral(Base):
    __tablename__ = "informacion_general"

    id = Column(Integer, primary_key=True)
    equipo = Column(String)
    marca = Column(String)
    modelo = Column(String)
    serie = Column(String)
    activoFijo = Column(String)
    registroSanitario = Column(String)
    ubicacion = Column(String)
    proveedor = Column(String)


class RegistroHistorico(Base):
    __tablename__ = "registro_historico"

    id = Column(Integer, primary_key=True)
    equipo = Column(String)
    formaAdquisicion = Column(String)
    marca = Column(String)
    documento = Column(String)
    modelo = Column(String)
    añoFabricacion = Column(String)
    fechaCompra = Column(String)
    fechaInstalacion = Column(String)
    inicioOperacion = Column(String)
    vencimientoGarantia = Column(String)
    registroSanitario = Column(String)
    ubicacion = Column(String)
    proveedor = Column(String)
    fabricante = Column(String)


class RegistroTecnicoInstalacion(Base):
    __tablename__ = "registro_tecnico_instalacion"

    id = Column(Integer, primary_key=True)
    tension = Column(String)
    corriente = Column(String)
    peso = Column(String)
    potencia = Column(String)
    frecuencia = Column(String)
    velocidad = Column(String)
    presion = Column(String)
    rangoTemperatura = Column(String)
    tecnologiaPredominante = Column(String)


class RegistroTecnicoFuncionamiento(Base):
    __tablename__ = "registro_tecnico_funcionamiento"

    id = Column(Integer, primary_key=True)
    rangoVoltaje = Column(String)
    rangoPresion = Column(String)
    rangoHumedad = Column(String)
    rangoCorriente = Column(String)
    rangoFrecuencia = Column(String)
    diagnostico = Column(String)
    rehabilitacion = Column(String)
    prevencion = Column(String)
    tratamientoVida = Column(String)
    analisisLaboratorio = Column(String)


class ClasificacionBiomedica(Base):
    __tablename__ = "clasificacion_biomedica"

    id = Column(Integer, primary_key=True)
    rangoVoltaje = Column(String)
    diagnostico = Column(String)
    rehabilitacion = Column(String)
    prevencion = Column(String)
    tratamientoVida = Column(String)
    analisisLaboratorio = Column(String)


class ClasificacionNivelRiesgo(Base):
    __tablename__ = "clasificacion_nivel_riesgo"

    id = Column(Integer, primary_key=True)
    claseI = Column(Boolean)
    claseIA = Column(Boolean)
    claseIIB = Column(Boolean)
    claseIII = Column(Boolean)


class PeriodicidadMantenimiento(Base):
    __tablename__ = "periodicidad_mantenimiento"

    id = Column(Integer, primary_key=True)
    cadaTresMeses = Column(Boolean)
    anual = Column(Boolean)


class RequiereCalibracion(Base):
    __tablename__ = "requiere_calibracion"

    id = Column(Integer, primary_key=True)
    si = Column(Boolean)
    no = Column(Boolean)


class Accesorios(Base):
    __tablename__ = "accesorios"

    id = Column(Integer, primary_key=True)
    accesorio1 = Column(String)
    accesorio2 = Column(String)
    accesorio3 = Column(String)
    accesorio4 = Column(String)
    accesorio5 = Column(String)
    accesorio6 = Column(String)


class Observaciones(Base):
    __tablename__ = "observaciones"

    id = Column(Integer, primary_key=True)
    observacion1 = Column(String)
    observacion2 = Column(String)
    observacion3 = Column(String)
    observacion4 = Column(String)
    observacion5 = Column(String)


class DocumentosSoportes(Base):
    __tablename__ = "documentos_soportes"

    id = Column(Integer, primary_key=True)
    copiaRegistroSanitario = Column(String)
    copiaRegistroImportacion = Column(String)
    copiaFactura = Column(String)
    copiaIngresoAlmacen = Column(String)
    copiaActaReciboSatisfaccion = Column(String)
    guiaRapidaOperacion = Column(String)
    recomendacionUsoAccesorios = Column(String)
    recomendacionAseguramientoMetrologico = Column(String)
    estimativoCostoAccesorios = Column(String)
    recomendacionesLimpiezaDesinfeccion = Column(String)
    registroCapacitacion = Column(String)
